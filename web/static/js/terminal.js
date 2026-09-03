/* ==========================================================
   ProjectLumina — Terminal interactiva (Xterm.js + WebSocket)
   Conecta a /api/terminal (WebSocket) y pinta el shell en un
   terminal Xterm.js real, con redimensionado y reconexión.
   ========================================================== */

let terminalWS = null;
let termInstance = null;
let termFit = null;
let termEstadoLigadura = 'conectando';

document.addEventListener('DOMContentLoaded', () => {
  initTerminalInteractiva();

  // Reconectar al volver a la vista terminal.
  window.addEventListener('hashchange', () => {
    if ((window.location.hash || '').includes('terminal')) {
      if (!terminalWS || terminalWS.readyState > WebSocket.OPEN) {
        conectarTerminal();
      }
    }
  });
});

function initTerminalInteractiva(){
  const reconectar = document.getElementById('termReconnect');
  if (reconectar) reconectar.addEventListener('click', conectarTerminal);

  const cwdSel = document.getElementById('termCwdSelect');
  if (cwdSel) cwdSel.addEventListener('change', () => {
    // Cambiar cwd requiere reconexión (nuevo shell en esa ruta).
    desconectarTerminal();
    conectarTerminal();
  });
}

function poblarCwdSelect(){
  const sel = document.getElementById('termCwdSelect');
  if (!sel) return;
  // Poblamos con los servicios que tengan ruta (para iniciar el shell ahí).
  sel.innerHTML = '<option value="">~ (inicio del usuario)</option>';
  (estado.servicios || []).forEach(s => {
    if (s.ruta){
      const opt = document.createElement('option');
      opt.value = s.ruta;
      opt.textContent = `${s.nombre} · ${s.ruta}`;
      sel.appendChild(opt);
    }
  });
}

function crearInstancia(){
  const contenedor = document.getElementById('termInteractive');
  if (!contenedor) return null;
  if (window.Terminal) {
    contenedor.innerHTML = '';
    termInstance = new window.Terminal({
      cursorBlink: true,
      fontFamily: '"JetBrains Mono", monospace',
      fontSize: 13,
      theme: {
        background: '#0d1117',
        foreground: '#e6edf3',
        cursor: '#58a6ff',
        selectionBackground: '#264f78',
        black: '#0d1117', red: '#ff7b72', green: '#3fb950', yellow: '#d29922',
        blue: '#58a6ff', magenta: '#bc8cff', cyan: '#39c5cf', white: '#e6edf3',
        brightBlack: '#6e7681', brightRed: '#ffa198', brightGreen: '#56d364',
        brightYellow: '#e3b341', brightBlue: '#79c0ff', brightMagenta: '#d2a8ff',
        brightCyan: '#56d4dd', brightWhite: '#ffffff'
      }
    });
    termFit = new window.FitAddon.FitAddon();
    termInstance.loadAddon(termFit);
    const links = new window.WebLinksAddon.WebLinksAddon();
    termInstance.loadAddon(links);
    termInstance.open(contenedor);
    termFit.fit();
    return termInstance;
  }
  return null;
}

function desconectarTerminal(){
  if (terminalWS){
    try { terminalWS.close(); } catch (e) {}
    terminalWS = null;
  }
  setTermConn('off');
}

function setTermConn(estado){
  const pill = document.getElementById('termConnPill');
  const title = document.getElementById('termInteractiveTitle');
  if (!pill) return;
  pill.className = `status-pill status-pill--${estado === 'ok' ? 'online' : 'offline'}`;
  const txt = pill.querySelector('.pulse');
  if (txt) txt.textContent = estado === 'ok' ? ' conectado' : ' desconectado';
  if (title) title.textContent = estado === 'ok' ? 'lumina · bash (local)' : 'lumina · bash (offline)';
}

function conectarTerminal(){
  const contenedor = document.getElementById('termInteractive');
  if (!contenedor) return;

  poblarCwdSelect();

  const term = crearInstancia();
  if (!term){
    contenedor.innerHTML = '<div class="term-placeholder">no se pudo cargar Xterm.js</div>';
    return;
  }

  const cwd = document.getElementById('termCwdSelect')?.value || '';
  const token = (estado.token || localStorage.getItem('lumina_token') || '').trim();
  const qs = token ? `?token=${encodeURIComponent(token)}` : '';
  const cwdQs = cwd ? `${qs ? '&' : '?'}cwd=${encodeURIComponent(cwd)}` : '';

  const proto = location.protocol === 'https:' ? 'wss' : 'ws';
  terminalWS = new WebSocket(`${proto}://${location.host}/api/terminal${qs}${cwdQs}`);

  terminalWS.onopen = () => {
    setTermConn('ok');
    term.write('\x1b[1;32m● conexión establecida\x1b[0m · shell en este servidor\n');
    term.focus();
  };

  terminalWS.onmessage = (event) => {
    const msg = event.data;
    if (msg === 'bye'){
      term.write('\r\n\x1b[1;33m● el shell terminó\x1b[0m\n');
      terminalWS.close();
      setTermConn('off');
      return;
    }
    if (msg.startsWith('out:')){
      const data = msg.slice(4);
      const bytes = atob(data);
      // xterm acepta el texto UTF-8 decodificado.
      term.write(bytes);
    }
  };

  terminalWS.onclose = (e) => {
    setTermConn('off');
    term.write(`\r\n\x1b[1;31m● conexión cerrada${e.code === 4401 ? ' (sin autorización)' : ''}\x1b[0m\n`);
  };
  terminalWS.onerror = () => {
    term.write('\r\n\x1b[1;31m● error de conexión\x1b[0m\n');
  };

  // Teclado del usuario → WebSocket (base64).
  term.onData((data) => {
    if (terminalWS && terminalWS.readyState === WebSocket.OPEN){
      terminalWS.send('in:' + btoa(unescape(encodeURIComponent(data))));
    }
  });

  // Redimensionar línea/columna del terminal.
  const onResize = () => {
    try {
      termFit.fit();
      term.focus();
    } catch (e) {}
  };
  window.addEventListener('resize', onResize);
}

// Expone para reconectar manualmente desde la consola.
window.conectarTerminal = conectarTerminal;
