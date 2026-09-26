#!/usr/bin/env python3
"""Burn a reviewed SRT into a vertical master using PNG overlays and FFmpeg.

The Mac's FFmpeg lacks libass, so each cue is drawn once with Pillow. The
source audio is copied without modification. This is for reviewed subtitles;
it does not transcribe or correct speech.
"""

import argparse
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFont


TIMESTAMP = re.compile(r"^(\d{2}):(\d{2}):(\d{2}),(\d{3})$")
FONT = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")


def seconds(value: str) -> float:
    match = TIMESTAMP.fullmatch(value)
    if not match:
        raise ValueError(f"invalid SRT timestamp: {value}")
    hours, minutes, secs, millis = map(int, match.groups())
    return hours * 3600 + minutes * 60 + secs + millis / 1000


def cues(path: Path) -> list[tuple[float, float, str]]:
    content = path.read_text(encoding="utf-8-sig").strip()
    result = []
    for block in re.split(r"\n\s*\n", content):
        lines = block.splitlines()
        if lines and lines[0].strip().isdigit():
            lines.pop(0)
        if len(lines) < 2 or " --> " not in lines[0]:
            raise ValueError(f"invalid SRT cue: {block[:60]}")
        start, end = map(seconds, lines[0].split(" --> "))
        if start < 0 or end <= start or (result and start < result[-1][1] - 0.001):
            raise ValueError(f"invalid or overlapping cue: {start}–{end}")
        result.append((start, end, "\n".join(lines[1:])))
    if not result:
        raise ValueError("SRT has no cues")
    return result


def probe(path: Path) -> tuple[int, int, float, str]:
    command = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
               "stream=width,height,color_transfer:format=duration", "-of", "default=nw=1", str(path)]
    values = dict(line.split("=", 1) for line in subprocess.check_output(command, text=True).splitlines())
    return (int(values["width"]), int(values["height"]), float(values["duration"]),
            values.get("color_transfer", "unknown"))


def draw_cue(text: str, width: int, path: Path) -> tuple[int, int]:
    lines = text.splitlines()
    scale = width / 1080
    fontsize = round(58 * scale)
    canvas_width = min(width - round(100 * scale), round(1000 * scale))
    while True:
        font = ImageFont.truetype(str(FONT), fontsize)
        probe_draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
        max_line_width = max(probe_draw.textbbox((0, 0), line, font=font, stroke_width=round(3 * scale))[2]
                             for line in lines)
        if max_line_width <= canvas_width - round(14 * scale) or fontsize <= round(42 * scale):
            break
        fontsize -= round(2 * scale)
    line_height = fontsize + round(13 * scale)
    height = len(lines) * line_height + round(16 * scale)
    image = Image.new("RGBA", (canvas_width, height), (0, 0, 0, 0))
    painter = ImageDraw.Draw(image)
    for index, line in enumerate(lines):
        box = painter.textbbox((0, 0), line, font=font, stroke_width=round(3 * scale))
        line_width = box[2] - box[0]
        x = (canvas_width - line_width) / 2 - box[0]
        y = round(8 * scale) + index * line_height - box[1]
        painter.text((x, y), line, font=font, fill=(255, 255, 255, 255),
                     stroke_width=round(3 * scale), stroke_fill=(0, 0, 0, 255))
    image.save(path)
    return canvas_width, height


def draw_edl_text(spec: dict, frame_width: int, path: Path) -> int:
    lines = spec["lines"]
    scale = frame_width / 1080
    size = round(int(spec.get("size", 38)) * scale)
    pad = round(int(spec.get("pad", 12)) * scale)
    font = ImageFont.truetype(str(FONT), size)
    measure = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    line_widths = [measure.textbbox((0, 0), line, font=font, stroke_width=1)[2]
                   for line in lines]
    width = min(frame_width - round(80 * scale), max(line_widths) + 2 * pad + round(16 * scale))
    line_height = size + round(12 * scale)
    height = line_height * len(lines) + 2 * pad
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    painter = ImageDraw.Draw(image)
    box = spec.get("boxcolor", "black@0.65")
    color_name, _, opacity = box.partition("@")
    box_rgba = (*ImageColor.getrgb(color_name), round(float(opacity or 1) * 255))
    painter.rounded_rectangle((0, 0, width - 1, height - 1), radius=round(10 * scale), fill=box_rgba)
    foreground = (*ImageColor.getrgb(spec.get("color", "white")), 255)
    for index, line in enumerate(lines):
        box = painter.textbbox((0, 0), line, font=font, stroke_width=1)
        x = (width - (box[2] - box[0])) / 2 - box[0]
        y = pad + index * line_height - box[1]
        painter.text((x, y), line, font=font, fill=foreground,
                     stroke_width=1, stroke_fill=(0, 0, 0, 255))
    image.save(path)
    return round(int(spec.get("y", 110)) * scale)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("srt", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--edl-texts", type=Path,
                        help="Render title and AI disclosure overlays from an EDL JSON")
    parser.add_argument("--asset-root", type=Path,
                        help="Use title PNG overlays from this root when the EDL defines them")
    parser.add_argument("--film-finish", action="store_true",
                        help="Add subtle grain and vignette before text overlays")
    parser.add_argument("--source-is-tonemapped-sdr", action="store_true",
                        help="Source pixels are already SDR despite inherited HLG/PQ metadata")
    parser.add_argument("--limit-seconds", type=float, default=None,
                        help="Render a short sample for visual QA")
    args = parser.parse_args()
    if args.source.resolve() == args.output.resolve():
        parser.error("output must differ from source")
    width, height, duration, transfer = probe(args.source)
    if (width, height) not in ((1080, 1920), (2160, 3840)):
        parser.error(f"expected 1080×1920 or 2160×3840 source, got {width}×{height}")
    if transfer in ("arib-std-b67", "smpte2084") and not args.source_is_tonemapped_sdr:
        parser.error("source is tagged HDR; tonemap first or confirm pregraded SDR pixels with "
                     "--source-is-tonemapped-sdr")
    subtitles = cues(args.srt)
    if subtitles[-1][1] > duration + 0.1:
        parser.error("last cue extends past the source")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="caption-overlays-", dir=args.output.parent) as temp:
        tempdir = Path(temp)
        pngs = []
        filters = []
        previous = "0:v"
        if args.film_finish:
            filters.append("[0:v]noise=alls=3:allf=t,vignette=angle=PI/5[base]")
            previous = "base"
        overlays = []
        if args.edl_texts:
            edl = json.loads(args.edl_texts.read_text())
            for index, spec in enumerate(edl.get("texts", []), 1):
                png = tempdir / f"edl_{index:02d}.png"
                y = draw_edl_text(spec, width, png)
                overlays.append((float(spec["start"]), float(spec["end"]), png, y, 0.0, 0.0))
            if args.asset_root:
                for spec in edl.get("overlays", []):
                    asset = args.asset_root / spec["png"]
                    if width == 2160:
                        doubled = asset.with_name(asset.stem + "@2x" + asset.suffix)
                        if doubled.exists():
                            asset = doubled
                        else:
                            raise FileNotFoundError(f"4K title overlay missing: {doubled}")
                    if not asset.is_file():
                        raise FileNotFoundError(asset)
                    overlays.append((float(spec.get("start", 0)), float(spec.get("end", duration)),
                                     asset, round(float(spec.get("y", 250)) * (width / 1080)),
                                     float(spec.get("fade_in", 0.25)),
                                     float(spec.get("fade_out", 0.25))))
        for index, (start, end, caption) in enumerate(subtitles, 1):
            png = tempdir / f"{index:02d}.png"
            _, cue_height = draw_cue(caption, width, png)
            y = max(0, int(height * 0.84) - cue_height)
            overlays.append((start, end, png, y, 0.0, 0.0))
        for index, (start, end, png, y, fade_in, fade_out) in enumerate(overlays, 1):
            pngs.append((png, bool(fade_in or fade_out)))
            label = f"v{index}"
            overlay_input = f"{index}:v"
            if fade_in or fade_out:
                pieces = [f"[{index}:v]format=rgba"]
                if fade_in:
                    pieces.append(f"fade=t=in:st={start:.3f}:d={fade_in:.3f}:alpha=1")
                if fade_out:
                    pieces.append(f"fade=t=out:st={max(start, end-fade_out):.3f}:d={fade_out:.3f}:alpha=1")
                filters.append(",".join(pieces) + f"[f{index}]")
                overlay_input = f"f{index}"
            filters.append(f"[{previous}][{overlay_input}]overlay=x=(W-w)/2:y={y}:"
                           f"enable='gte(t,{start:.3f})*lt(t,{end:.3f})':"
                           f"repeatlast=1:shortest=1[{label}]")
            previous = label
        filters.append(f"[{previous}]format=yuv420p[vout]")
        graph = ";".join(filters)

        command = ["/opt/homebrew/bin/ffmpeg", "-v", "error", "-y", "-i", str(args.source)]
        for png, animated in pngs:
            command += ["-loop", "1", "-framerate", "30" if animated else "1", "-i", str(png)]
        bitrate, maxrate, bufsize = (("28000k", "36000k", "72000k") if width == 2160
                                     else ("7000k", "8500k", "17000k"))
        command += ["-filter_complex", graph, "-map", "[vout]", "-map", "0:a?",
                    "-c:v", "h264_videotoolbox", "-b:v", bitrate, "-maxrate", maxrate,
                    "-bufsize", bufsize, "-pix_fmt", "yuv420p", "-r", "30",
                    "-bsf:v", "h264_metadata=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                    "-c:a", "copy", "-movflags", "+faststart",
                    "-t", str(min(args.limit_seconds or duration, duration))]
        staged = tempdir / "render.part.mp4"
        command += [str(staged)]
        subprocess.run(command, check=True)
        os.replace(staged, args.output)
    print(f"wrote {args.output} with {len(subtitles)} cues")


if __name__ == "__main__":
    main()
