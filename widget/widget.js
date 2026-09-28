(() => {
  const API = document.currentScript.dataset.api;
  const css = `
  #llf-btn{position:fixed;bottom:20px;right:20px;width:56px;height:56px;border-radius:50%;background:#182433;color:#F7F4EE;border:2px solid #B49763;font-size:24px;cursor:pointer;z-index:9999;box-shadow:0 4px 12px rgba(0,0,0,.25)}
  #llf-box{position:fixed;bottom:90px;right:20px;width:340px;max-width:calc(100vw - 32px);height:460px;max-height:calc(100vh - 120px);background:#F7F4EE;border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,.25);display:none;flex-direction:column;overflow:hidden;z-index:9999;font-family:system-ui,sans-serif}
  #llf-box.open{display:flex}
  #llf-head{background:#182433;color:#F7F4EE;padding:12px 16px;font-weight:600}
  #llf-msgs{flex:1;overflow-y:auto;padding:12px;display:flex;flex-direction:column;gap:8px}
  .llf-m{max-width:80%;padding:8px 12px;border-radius:12px;font-size:14px;line-height:1.4;white-space:pre-wrap}
  .llf-bot{background:#fff;color:#182433;align-self:flex-start;border:1px solid #A89B8B}
  .llf-user{background:#B49763;color:#fff;align-self:flex-end}
  #llf-form{display:flex;border-top:1px solid #A89B8B}
  #llf-in{flex:1;border:0;padding:12px;font-size:14px;outline:none;background:#fff}
  #llf-send{background:#182433;color:#F7F4EE;border:0;padding:0 16px;cursor:pointer}`;
  document.head.insertAdjacentHTML("beforeend", `<style>${css}</style>`);
  document.body.insertAdjacentHTML("beforeend", `
    <button id="llf-btn" aria-label="Chat">💬</button>
    <div id="llf-box">
      <div id="llf-head">Long Life Furnishers</div>
      <div id="llf-msgs"></div>
      <form id="llf-form"><input id="llf-in" maxlength="500" placeholder="Type your question..." autocomplete="off"><button id="llf-send">Send</button></form>
    </div>`);

  const $ = id => document.getElementById(id);
  const msgs = $("llf-msgs"), input = $("llf-in");
  const add = (text, who) => {
    const d = document.createElement("div");
    d.className = `llf-m llf-${who}`;
    d.textContent = text;
    msgs.appendChild(d);
    msgs.scrollTop = msgs.scrollHeight;
    return d;
  };

  $("llf-btn").onclick = () => {
    $("llf-box").classList.toggle("open");
    if (!msgs.children.length) add("Assalam o Alaikum! How can I help you today?", "bot");
    input.focus();
  };

  $("llf-form").onsubmit = async e => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    add(text, "user");
    input.value = "";
    input.disabled = true;
    const typing = add("Typing...", "bot");
    try {
      const r = await fetch(`${API}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text }),
      });
      if (!r.ok) throw new Error(r.status);
      typing.textContent = (await r.json()).reply;
    } catch {
      typing.textContent = "Sorry, something went wrong. Please try again or contact us on WhatsApp.";
    }
    input.disabled = false;
    input.focus();
  };
})();