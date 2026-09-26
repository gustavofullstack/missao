#!/bin/bash
# gradetest.sh — mesmos 6 quadros em cada look, lado a lado
cd /root/reels; mkdir -p tests/g
TM="zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=pc,format=gbrp16le"
declare -A G
G[base]="null"
G[noite]="vibrance=intensity=0.18,curves=master='0/0 0.07/0.045 0.5/0.5 0.88/0.9 1/1',colorbalance=bs=0.035:bm=0.01:rh=0.025:bh=-0.015"
G[fogo]="vibrance=intensity=0.22,curves=master='0/0 0.1/0.06 0.5/0.53 1/1',colorbalance=rs=-0.02:bs=0.05:rh=0.06:gh=0.015:bh=-0.04"
G[suave]="vibrance=intensity=0.12,curves=master='0/0.035 0.5/0.52 1/0.97',colorbalance=bs=0.02:rh=0.02"
FR="IMG_8443:3 IMG_8453:36 IMG_8444:26 IMG_8460:15 IMG_8448:4 IMG_8468:10"
for g in base noite fogo suave; do
  ins=(); k=0
  for x in $FR; do s=${x%%:*}; t=${x##*:}; k=$((k+1))
    ffmpeg -v error -y -ss $t -i src/$s.MOV -frames:v 1 -vf "scale=360:640:flags=area,$TM,${G[$g]},scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,drawtext=fontfile=/usr/share/fonts/opentype/inter/Inter-Bold.otf:text=$g:x=8:y=8:fontsize=26:fontcolor=yellow:box=1:boxcolor=black" tests/g/${g}_$k.png
    ins+=(-i tests/g/${g}_$k.png); done
  ffmpeg -v error -y "${ins[@]}" -filter_complex "hstack=inputs=6" tests/g/row_$g.jpg
done
ffmpeg -v error -y -i tests/g/row_base.jpg -i tests/g/row_noite.jpg -i tests/g/row_fogo.jpg -i tests/g/row_suave.jpg -filter_complex vstack=inputs=4 tests/grades.jpg && echo ok
