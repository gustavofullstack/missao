// cdpd.mjs — ponte PERSISTENTE para o Chrome do Gustavo (depuração remota na 9222).
// Por que existe: cada conexão nova ao 9222 faz o Chrome perguntar "Permitir a depuração remota?".
// O servidor abre UMA conexão (um "Permitir" por sessão do Chrome) e recebe comandos em 127.0.0.1:9333,
// com token num arquivo 600 para que outro processo local não herde essa permissão sem pedir.
//   node cdpd.mjs serve              (fica de pé até `node cdpd.mjs stop` ou o Chrome fechar)
//   node cdpd.mjs list | activate P | eval P JS | shot P OUT [escala] | click P X Y | clicktext P TEXTO [SEL] |
//                 type P TEXTO | key P TECLA | upload P SELETOR ARQUIVO... | stop
import fs from "node:fs";
import http from "node:http";
import crypto from "node:crypto";

const TOKEN_FILE = new URL(".cdpd_token", import.meta.url).pathname;
const [cmd, ...argv] = process.argv.slice(2);

if (cmd !== "serve") {
  const token = fs.readFileSync(TOKEN_FILE, "utf8").trim();
  const r = await fetch("http://127.0.0.1:9333", { method: "POST", headers: { "x-token": token }, body: JSON.stringify({ cmd, args: argv }) });
  const j = await r.json();
  if (!j.ok) { console.error("falhou:", j.erro); process.exit(1); }
  console.log(typeof j.out === "string" ? j.out : JSON.stringify(j.out, null, 1));
  process.exit(0);
}

const TOKEN = crypto.randomBytes(16).toString("hex");
fs.rmSync(TOKEN_FILE, { force: true });
fs.writeFileSync(TOKEN_FILE, TOKEN, { mode: 0o600 });

const ws = new WebSocket("ws://127.0.0.1:9222/devtools/browser");
let seq = 0;
const pending = new Map();
const sessions = new Map(); // targetId -> sessionId (anexa uma vez por aba)
const send = (method, params = {}, sessionId) => new Promise((res, rej) => {
  const id = ++seq;
  pending.set(id, { res, rej });
  ws.send(JSON.stringify({ id, method, params, ...(sessionId && { sessionId }) }));
  setTimeout(() => { if (pending.delete(id)) rej(new Error(`${method}: sem resposta em 90 s`)); }, 90000);
});
ws.onmessage = (ev) => {
  const m = JSON.parse(ev.data);
  if (m.method === "Target.detachedFromTarget")
    for (const [t, s] of sessions) if (s === m.params.sessionId) sessions.delete(t);
  const p = m.id && pending.get(m.id);
  if (!p) return;
  pending.delete(m.id);
  m.error ? p.rej(new Error(JSON.stringify(m.error))) : p.res(m.result);
};
ws.onerror = (e) => { console.error("erro de conexão:", e.message || e.type); process.exit(1); };
ws.onclose = () => { console.error("conexão com o Chrome fechou; saindo"); fs.rmSync(TOKEN_FILE, { force: true }); process.exit(3); };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function target(prefix) {
  const { targetInfos } = await send("Target.getTargets");
  const t = targetInfos.find((x) => x.type === "page" && x.targetId.startsWith(prefix));
  if (!t) throw new Error(`aba ${prefix} não encontrada`);
  let sessionId = sessions.get(t.targetId);
  if (!sessionId) {
    ({ sessionId } = await send("Target.attachToTarget", { targetId: t.targetId, flatten: true }));
    sessions.set(t.targetId, sessionId);
  }
  return { t, sessionId };
}
const evaluate = async (sessionId, expression) => {
  const r = await send("Runtime.evaluate", { expression, awaitPromise: true, returnByValue: true, userGesture: true }, sessionId);
  if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text);
  return r.result.value;
};
async function mouseClick(sessionId, x, y) {
  for (const type of ["mouseMoved", "mousePressed", "mouseReleased"])
    await send("Input.dispatchMouseEvent", { type, x, y, button: "left", clickCount: 1 }, sessionId);
}
const KEYS = { Enter: 13, Tab: 9, Escape: 27, Backspace: 8, ArrowDown: 40, ArrowUp: 38, Space: 32 };

async function run(cmd, a) {
  if (cmd === "list") {
    const { targetInfos } = await send("Target.getTargets");
    return targetInfos.filter((x) => x.type === "page").map((t) => `${t.targetId.slice(0, 8)} | ${t.title.slice(0, 60)} | ${t.url.slice(0, 90)}`).join("\n");
  }
  const { t, sessionId } = await target(a[0]);
  if (cmd === "activate") { await send("Target.activateTarget", { targetId: t.targetId }); return "ativa " + t.title.slice(0, 60); }
  if (cmd === "eval") return await evaluate(sessionId, a[1]);
  if (cmd === "shot") {
    await send("Target.activateTarget", { targetId: t.targetId }); // aba em segundo plano não pinta
    const scale = Number(a[2] || 1), params = { format: "png" };
    if (scale !== 1) {
      const v = (await send("Page.getLayoutMetrics", {}, sessionId)).cssVisualViewport;
      params.clip = { x: v.pageX, y: v.pageY, width: v.clientWidth, height: v.clientHeight, scale };
    }
    fs.writeFileSync(a[1], Buffer.from((await send("Page.captureScreenshot", params, sessionId)).data, "base64"));
    return "ok " + a[1];
  }
  if (cmd === "click") { await mouseClick(sessionId, Number(a[1]), Number(a[2])); return `clique ${a[1]} ${a[2]}`; }
  if (cmd === "clicktext") {
    const sel = a[2] || "button,[role=button],[role=menuitem],[role=option],[role=tab],[role=switch],a,label,div[tabindex],span";
    const box = await evaluate(sessionId, `(() => {
      const want = ${JSON.stringify(a[1])}.toLowerCase();
      const els = [...document.querySelectorAll(${JSON.stringify(sel)})].filter((e) => {
        const r = e.getBoundingClientRect();
        if (!r.width || !r.height) return false;
        const al = (e.getAttribute("aria-label") || "").toLowerCase();
        const tx = (e.innerText || "").trim().toLowerCase();
        return tx === want || al === want || tx.split("\\n").some((l) => l.trim() === want);
      });
      if (!els.length) return null;
      const e = els.sort((x, y) => (x.innerText || "").length - (y.innerText || "").length)[0];
      e.scrollIntoView({ block: "center" });
      const r = e.getBoundingClientRect();
      return { x: r.x + r.width / 2, y: r.y + r.height / 2, n: els.length, tag: e.tagName };
    })()`);
    if (!box) throw new Error(`nada com o texto "${a[1]}"`);
    await sleep(150);
    await mouseClick(sessionId, box.x, box.y);
    return box;
  }
  if (cmd === "type") { await send("Input.insertText", { text: a[1] }, sessionId); return `digitou ${a[1].length}`; }
  if (cmd === "key") {
    const code = KEYS[a[1]];
    if (!code) throw new Error(`tecla desconhecida ${a[1]}`);
    const base = { key: a[1] === "Space" ? " " : a[1], code: a[1], windowsVirtualKeyCode: code, nativeVirtualKeyCode: code };
    await send("Input.dispatchKeyEvent", { type: "keyDown", ...base, ...(a[1] === "Enter" && { text: "\r" }) }, sessionId);
    await send("Input.dispatchKeyEvent", { type: "keyUp", ...base }, sessionId);
    return "tecla " + a[1];
  }
  if (cmd === "upload") {
    const [, selector, ...files] = a;
    for (const f of files) if (!fs.existsSync(f)) throw new Error(`arquivo não existe: ${f}`);
    const { root } = await send("DOM.getDocument", { depth: -1, pierce: true }, sessionId);
    const { nodeIds } = await send("DOM.querySelectorAll", { nodeId: root.nodeId, selector }, sessionId);
    if (!nodeIds.length) throw new Error(`nenhum elemento para ${selector}`);
    await send("DOM.setFileInputFiles", { files, nodeId: nodeIds[nodeIds.length - 1] }, sessionId);
    return `${files.length} arquivo(s) em ${selector} (${nodeIds.length} candidato(s), usei o último)`;
  }
  throw new Error("comando desconhecido " + cmd);
}

ws.onopen = () => {
  console.log(new Date().toISOString(), "conectado ao Chrome (uma vez); ouvindo 127.0.0.1:9333");
  http.createServer((req, res) => {
    let body = "";
    req.on("data", (c) => (body += c));
    req.on("end", async () => {
      if (req.headers["x-token"] !== TOKEN) { res.statusCode = 403; return res.end(JSON.stringify({ ok: false, erro: "token" })); }
      try {
        const { cmd, args = [] } = JSON.parse(body || "{}");
        if (cmd === "stop") { res.end(JSON.stringify({ ok: true, out: "parando" })); return ws.close(); }
        res.end(JSON.stringify({ ok: true, out: await run(cmd, args) }));
      } catch (e) { res.end(JSON.stringify({ ok: false, erro: e.message })); }
    });
  }).listen(9333, "127.0.0.1");
};
