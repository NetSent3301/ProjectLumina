/* ==========================================================
   ProjectLumina — dashboard v0.1
   Reloj, navegación (hash), vistas, pestañas bots/webs y
   registro de actividad. Desde v0.1 consume la API REST:
     GET  /api/servicios                  listar con estado
     POST /api/servicios/{id}/{accion}    iniciar/detener/reiniciar
     GET  /api/servicios/{id}/logs        ver logs
   Solo se registra actividad real (no se inventan datos).
   ========================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initClock();
  initNav();
  initServiceActions();
  initRefreshButton();
  initEmptyCard();
  initServiceModal();
  initServiceTabs();
  initTerminal();
  loadServicios();
  loadMetricas();
});

/* ---------- reloj del servidor ---------- */
function initClock(){
  const el = document.getElementById('clock');
  if (!el) return;

  const tick = () => {
    const now = new Date();
    el.textContent = now.toLocaleTimeString('es-CO', { hour12: false });
  };
  tick();
  setInterval(tick, 1000);
}

/* ---------- navegación lateral (cambio de vista sin recargar) ---------- */
function initNav(){
  const items = document.querySelectorAll('.nav-item');
  const views = document.querySelectorAll('.view');

  const switchView = (view) => {
    const target = document.querySelector(`.view[data-view="${view}"]`);

    views.forEach(v => {
      const isActive = v === target;
      v.classList.toggle('is-active', isActive);
      v.setAttribute('aria-hidden', isActive ? 'false' : 'true');
    });

    items.forEach(item => {
      const isActive = item.dataset.view === view;
      item.classList.toggle('is-active', isActive);
      item.setAttribute('aria-current', isActive ? 'true' : 'false');
    });

    window.luminaView = view; // para pausar refrescos fuera de la vista activa
  };

  const applyHash = () => {
    const view = (location.hash || '').replace(/^#\/?/, '') || 'resumen';
    const exists = document.querySelector(`.view[data-view="${view}"]`);
    switchView(exists ? view : 'resumen');
  };

  // los enlaces <a href="#/vista"> cambian el hash; aquí reaccionamos.
  // también cubre el botón atrás/adelante y carga directa (p. ej. /#/servicios).
  window.addEventListener('hashchange', applyHash);
  applyHash();
}

/* ==========================================================
   API
   ========================================================== */

const estado = {
  servicios: [],               // lista cruda de /api/servicios
  token: localStorage.getItem('lumina_token') || '',
  async cargar(){
    estado.servicios = await api('/api/servicios');
  },
  porTipo(tipo){
    return estado.servicios.filter(s => s.tipo === tipo);
  },
  enLinea(tipo){
    return estado.porTipo(tipo).filter(s => s.estado === 'online').length;
  }
};

async function api(path, opciones = {}){
  const headers = { ...(opciones.headers || {}) };
  if (estado.token) headers['X-API-Key'] = estado.token;

  const res = await fetch(path, { ...opciones, headers });
  if (!res.ok) {
    let detalle = `HTTP ${res.status}`;
    try { detalle = (await res.json()).detail || detalle; } catch {}
    throw new Error(detalle);
  }
  if (res.status === 204) return null;
  return res.json();
}

/* ---------- carga y render del listado ---------- */
async function loadServicios(){
  mostrarSkeletonsServicios();
  try {
    await estado.cargar();
    ocultarSkeletonsServicios();
  } catch (error) {
    ocultarSkeletonsServicios();
    const sub = document.getElementById('resumenSub');
    if (sub) sub.textContent = 'sin servicios registrados';
    sinAPI(error.message);
    return;
  }
  renderServicios();
  poblarTerminalSelect();
}

function renderServicios(){
  renderCuerpo();
  renderVacios();
  renderContadores();
  renderResumen();
  renderMetricaServicios();
}

/* ---------- skeleton loader mientras conecta al backend ---------- */
function cardSkeleton(){
  const s = document.createElement('div');
  s.className = 'card-skeleton';
  s.innerHTML = `
    <span class="skel skel-line w60"></span>
    <span class="skel skel-line w80"></span>
    <span class="skel skel-line w40"></span>
  `;
  return s;
}

function mostrarSkeletonsServicios(){
  const grid = document.getElementById('servicesGrid');
  if (!grid || grid.querySelector('.card-skeleton')) return;
  for (let i = 0; i < 3; i++) grid.appendChild(cardSkeleton());
}

function ocultarSkeletonsServicios(){
  document.querySelectorAll('.card-skeleton').forEach(el => el.remove());
}

function renderCuerpo(){
  const grid = document.getElementById('servicesGrid');
  if (!grid) return;

  grid.querySelectorAll('.card[data-id]').forEach(c => c.remove());
  estado.servicios.forEach(s => grid.appendChild(tarjetaServicio(s)));
}

function renderVacios(){
  const total = estado.servicios.length;

  const vacioResumen = document.getElementById('emptyServiceCard');
  if (vacioResumen) vacioResumen.classList.toggle('is-visible', total === 0);

  // en resumen la sección "servicios" solo se muestra si aún no hay ninguno
  const secResumen = document.getElementById('resumenServicesSection');
  if (secResumen) secResumen.classList.toggle('is-hidden', total > 0);

  ['bot', 'web'].forEach(tipo => {
    const vacio = document.getElementById(tipo === 'bot' ? 'emptyBots' : 'emptyWebs');
    if (vacio) vacio.classList.toggle('is-visible', estado.porTipo(tipo).length === 0);
  });
}

function renderContadores(){
  const count = document.getElementById('tabCount');
  if (!count) return;
  const tipo = document.querySelector('.tab.is-active')?.dataset.type || 'bot';
  const enLinea = estado.enLinea(tipo);
  const total = estado.porTipo(tipo).length;
  count.textContent = `${total} ${tipo === 'bot' ? 'bots' : 'webs'} · ${enLinea} en línea`;
}

function renderResumen(){
  const total = estado.servicios.length;
  const enLinea = estado.servicios.filter(s => s.estado === 'online').length;

  const sub = document.querySelector('.view[data-view="resumen"] .topbar-sub');
  if (sub) sub.textContent = total === 0
    ? 'sin servicios registrados'
    : `${total} ${total === 1 ? 'servicio' : 'servicios'} · ${enLinea} en línea`;

  const subServicios = document.querySelector('.view[data-view="servicios"] .topbar-sub');
  if (subServicios) subServicios.textContent = total === 0
    ? 'aún no hay servicios conectados'
    : `${total} ${total === 1 ? 'servicio conectado' : 'servicios conectados'}`;
}

function sinAPI(mensaje){
  // Sin backend no inventamos datos: se quedan los estados vacíos.
  logEvent(`No se pudo contactar la API (${mensaje}). Cuando el backend esté disponible los estados se actualizarán solos.`, 'warn');
}

/* ==========================================================
   Métricas rápidas (resumen)
   ========================================================== */

let metricasTimer = null;
let metricasListas = false; // es true solo tras recibir una medición real

async function loadMetricas(inicial = true){
  const card = document.getElementById('metricCpuCard');
  if (inicial && card) card.classList.add('is-loading');

  try {
    const datos = await api('/api/servidor');
    renderMetricasServidor(datos);
    metricasListas = true;
  } catch {
    // sin datos reales nunca se muestran cifras; con datos previos se
    // conserva la última medición real en lugar de fabricar ceros.
    if (!metricasListas) setMetricaPendiente();
  } finally {
    if (inicial && card) card.classList.remove('is-loading');
  }

  // refresco ligero en tiempo real solo mientras esté visible el resumen
  if (!metricasTimer) {
    metricasTimer = setInterval(async () => {
      if (window.luminaView === 'resumen' && estado.token) await loadMetricas(false);
    }, 10000);
  }
}

function setMetricaPendiente(){
  ['metricCpu', 'metricRam', 'metricUptime', 'metricSvc'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.textContent = '—';
  });
}

function renderMetricasServidor(d){
  const cpu = document.getElementById('metricCpu');
  if (cpu) cpu.innerHTML = `${Math.round(d.cpu || 0)}<small>%</small>`;
  setBarra('metricCpuBar', d.cpu || 0, 'metricCpuBarWrap');
  const sub = document.getElementById('metricCpuSub');
  if (sub) sub.textContent = 'promedio de uso del sistema';

  const ram = document.getElementById('metricRam');
  if (ram) ram.innerHTML = `${formatGB(d.ram?.usado)}<small> GB</small>`;
  setBarra('metricRamBar', d.ram?.porcentaje || 0, 'metricRamBarWrap');
  const subRam = document.getElementById('metricRamSub');
  if (subRam) subRam.textContent = `de ${formatGB(d.ram?.total)} GB usados`;

  const uptime = document.getElementById('metricUptime');
  if (uptime) uptime.textContent = formatearUptime(d.uptime_seg);
}

function renderMetricaServicios(){
  const total = estado.servicios.length;
  const enLinea = estado.servicios.filter(s => s.estado === 'online').length;

  const value = document.getElementById('metricSvc');
  if (value) value.textContent = total === 0 ? '—' : `${enLinea}/${total}`;
  setBarra('metricSvcBar', total ? (enLinea / total) * 100 : 0, 'metricSvcBarWrap', enLinea === total && total > 0 ? 'ok' : '');
  const sub = document.getElementById('metricSvcSub');
  if (sub) sub.textContent = total === 0 ? 'sin servicios registrados' : `${enLinea} de ${total} en línea`;
}

function setBarra(id, porcentaje, wrapId, grado = ''){
  const bar = document.getElementById(id);
  if (bar) bar.style.width = `${Math.max(0, Math.min(100, porcentaje))}%`;

  const wrap = document.getElementById(wrapId);
  if (wrap) wrap.classList.toggle('metric-bar--warn', grado === 'warn' || porcentaje > 75);
  if (wrap) wrap.classList.toggle('metric-bar--danger', porcentaje >= 92);
  if (wrap) wrap.classList.toggle('metric-bar--ok', grado === 'ok');
}

function formatGB(bytes){
  if (bytes == null) return '—';
  return (bytes / 1073741824).toFixed(1);
}

function formatearUptime(seg){
  if (seg == null) return '—';
  const d = Math.floor(seg / 86400);
  const h = Math.floor((seg % 86400) / 3600);
  const m = Math.floor((seg % 3600) / 60);
  const partes = [];
  if (d) partes.push(`${d}d`);
  if (h) partes.push(`${h}h`);
  partes.push(`${m}m`);
  return partes.join(' ');
}

/* ---------- tarjeta de un servicio real ---------- */
function tarjetaServicio(s){
  const card = document.createElement('article');
  card.className = 'card';
  card.dataset.id = s.id;
  card.dataset.tipo = s.tipo;
  card.dataset.status = s.estado;

  const icono = s.tipo === 'bot' ? '🤖' : '🌐';
  const enLinea = s.estado === 'online';
  const detalle = s.servicio || s.ruta || s.comando || 'sin unidad systemd';

  card.innerHTML = `
    <div class="card-top">
      <div class="card-title">
        <span class="card-icon">${icono}</span>
        <div>
          <h3>${escapar(s.nombre)}</h3>
          <p class="card-sub">${escapar(detalle)}</p>
        </div>
      </div>
      <span class="status-pill status-pill--${enLinea ? 'online' : 'offline'}">
        <span class="pulse"></span> ${enLinea ? 'en línea' : s.estado || 'sin estado'}
      </span>
    </div>
    <dl class="card-stats">
      <div><dt>tipo</dt><dd>${s.tipo}</dd></div>
      <div><dt>comando</dt><dd>${escapar(s.comando || '—')}</dd></div>
      <div><dt>auto-inicio</dt><dd>${s.auto_inicio ? 'sí' : 'no'}</dd></div>
    </dl>
    <div class="card-actions">
      <button class="btn-ghost" data-op="iniciar">iniciar</button>
      <button class="btn-ghost" data-op="detener">detener</button>
      <button class="btn-ghost" data-op="reiniciar">reiniciar</button>
      <button class="btn-ghost" data-op="logs">logs</button>
    </div>
  `;
  return card;
}

function escaper(valor){
  return String(valor).replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}

/* ---------- acciones sobre servicios (llaman a la API) ---------- */
function initServiceActions(){
  const grid = document.getElementById('servicesGrid');
  if (!grid) return;

  // delegación de eventos: las tarjetas se re-renderizan con cada carga.
  grid.addEventListener('click', async (event) => {
    const btn = event.target.closest('[data-op]');
    if (!btn) return;
    const card = btn.closest('.card[data-id]');
    if (!card) return;

    const id = card.dataset.id;
    const op = btn.dataset.op;
    const nombre = card.querySelector('h3')?.textContent?.trim() || 'servicio';

    if (op === 'logs') {
      await verLogs(id, nombre);
      return;
    }

    // iniciar / detener / reiniciar
    try {
      const original = btn.textContent;
      btn.disabled = true;
      btn.textContent = op === 'reiniciar' ? 'reiniciando…' : 'enviando…';

      const servicio = await api(`/api/servicios/${id}/${op}`, { method: 'POST' });
      logEvent(`<strong>${escapar(nombre)}</strong> ${op === 'iniciar' ? 'se inició' : op === 'detener' ? 'se detuvo' : 'se reinició'} · ahora: <strong>${servicio.estado}</strong>`, 'ok');

      renderServicios();
    } catch (error) {
      logEvent(`error al ${op} <strong>${escapar(nombre)}</strong>: ${escapar(error.message)}`, 'warn');
      renderServicios();
    }
  });
}

async function verLogs(id, nombre){
  try {
    const datos = await api(`/api/servicios/${id}/logs?lines=100`);
    const contenido = (datos.log || '').trim() || 'log vacío';
    logEvent(`logs de <strong>${escapar(nombre)}</strong> (${datos.lines} líneas)`, 'ok');
    logEvent(`<span class="log-pre">${escapar(contenido.slice(-600))}</span>`, 'ok');
  } catch (error) {
    logEvent(`error al leer logs de <strong>${escapar(nombre)}</strong>: ${escapar(error.message)}`, 'warn');
  }
}

/* ---------- botón actualizar estado ---------- */
function initRefreshButton(){
  const btn = document.getElementById('refreshBtn');
  if (!btn) return;

  btn.addEventListener('click', async () => {
    btn.classList.add('is-loading');
    btn.disabled = true;

    await loadServicios();
    await loadMetricas();

    btn.classList.remove('is-loading');
    btn.disabled = false;
    const total = estado.servicios.length;
    logEvent(total === 0
      ? 'Sin servicios registrados: no hay nada que comprobar todavía'
      : `Estado actualizado: ${total} ${total === 1 ? 'servicio' : 'servicios'} · ${estado.servicios.filter(s => s.estado === 'online').length} en línea`, 'ok');
  });
}

/* ---------- abrir el modal de conexión desde tarjetas y botones ---------- */
function initEmptyCard(){
  [document.getElementById('emptyServiceCard'), document.getElementById('addServiceLink')].forEach(el => {
    if (el) el.addEventListener('click', () => abrirModal('bot'));
  });

  const bots = document.getElementById('emptyBots');
  if (bots) bots.addEventListener('click', () => abrirModal('bot'));
  const webs = document.getElementById('emptyWebs');
  if (webs) webs.addEventListener('click', () => abrirModal('web'));

  // el botón de la vista servicios usa la pestaña activa
  const addBtn = document.getElementById('addServiceBtn');
  if (addBtn) addBtn.addEventListener('click', () => {
    abrirModal(document.querySelector('.tab.is-active')?.dataset.type || 'bot');
  });
}

/* ==========================================================
   Modal: conectar un servicio
   ========================================================== */
let modalTipo = 'bot';

function initServiceModal(){
  const modal = document.getElementById('serviceModal');
  if (!modal) return;

  const close = document.getElementById('modalClose');
  if (close) close.addEventListener('click', cerrarModal);
  const cancel = document.getElementById('modalCancel');
  if (cancel) cancel.addEventListener('click', cerrarModal);

  modal.addEventListener('click', (e) => {
    if (e.target === modal) cerrarModal();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('is-open')) cerrarModal();
  });

  document.querySelectorAll('.modal-tab').forEach(tab => {
    tab.addEventListener('click', () => setModalTipo(tab.dataset.modalTipo));
  });

  const form = document.getElementById('serviceForm');
  if (form) form.addEventListener('submit', conectarServicio);
}

function abrirModal(tipo = 'bot'){
  const modal = document.getElementById('serviceModal');
  if (!modal) return;
  setModalTipo(tipo);
  ocultarError();
  modal.classList.add('is-open');
  modal.setAttribute('aria-hidden', 'false');
  const nombre = document.getElementById('f_nombre');
  if (nombre) {
    nombre.value = '';
    setTimeout(() => nombre.focus(), 30);
  }
}

function cerrarModal(){
  const modal = document.getElementById('serviceModal');
  if (!modal) return;
  modal.classList.remove('is-open');
  modal.setAttribute('aria-hidden', 'true');
}

function setModalTipo(tipo){
  modalTipo = tipo;
  document.querySelectorAll('.modal-tab').forEach(tab => {
    const isActive = tab.dataset.modalTipo === tipo;
    tab.classList.toggle('is-active', isActive);
    tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
  });

  const urlField = document.getElementById('f_checkUrlField');
  if (urlField) urlField.classList.toggle('is-hidden', tipo !== 'web');
}

function mostrarError(mensaje){
  const el = document.getElementById('modalError');
  if (!el) return;
  el.textContent = mensaje;
  el.classList.remove('is-hidden');
}

function ocultarError(){
  const el = document.getElementById('modalError');
  if (el) el.classList.add('is-hidden');
}

async function conectarServicio(event){
  event.preventDefault();

  const nombre = document.getElementById('f_nombre').value.trim();
  if (!nombre) return;

  const payload = {
    tipo: modalTipo,
    nombre,
    ruta: document.getElementById('f_ruta').value.trim(),
    comando: document.getElementById('f_comando').value.trim(),
    servicio: document.getElementById('f_servicio').value.trim(),
    check_url: modalTipo === 'web' ? (document.getElementById('f_check_url').value.trim() || null) : null,
    auto_inicio: document.getElementById('f_auto_inicio').checked,
    auto_reinicio: document.getElementById('f_auto_reinicio').checked,
  };

  const submit = document.getElementById('modalSubmit');
  if (submit) {
    submit.disabled = true;
    const icon = submit.querySelector('.btn-icon');
    if (icon) icon.textContent = '…';
  }

  try {
    const s = await api('/api/servicios', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    cerrarModal();
    logEvent(
      `servicio <strong>${escaper(s.nombre)}</strong> conectado · estado: <strong>${s.estado}</strong>` +
      (s.tipo === 'web' && s.check_url ? ' · verificado por HTTP' : ''),
      'ok'
    );

    await estado.cargar();
    renderServicios();
    poblarTerminalSelect();
  } catch (error) {
    mostrarError(`no se pudo conectar el servicio: ${error.message}`);
  } finally {
    if (submit) {
      submit.disabled = false;
      const icon = submit.querySelector('.btn-icon');
      if (icon) icon.textContent = '+';
    }
  }
}

/* ---------- panel de servicios: selector bots / webs ---------- */
function initServiceTabs(){
  const tabs = document.querySelectorAll('.tab[data-type]');
  if (!tabs.length) return;

  const setActiveTab = (type) => {
    tabs.forEach(tab => {
      const isActive = tab.dataset.type === type;
      tab.classList.toggle('is-active', isActive);
      tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
    });

    document.querySelectorAll('[data-type-panel]').forEach(panel => {
      panel.classList.toggle('is-visible', panel.dataset.typePanel === type);
    });

    renderContadores();
  };

  tabs.forEach(tab => {
    tab.addEventListener('click', () => setActiveTab(tab.dataset.type));
  });

  const initial = document.querySelector('.tab.is-active')?.dataset.type || 'bot';
  setActiveTab(initial);
}

/* ---------- helper: insertar entrada en el registro de actividad ---------- */
function logEvent(html, level = 'ok'){
  const list = document.getElementById('logList');
  if (!list) return;

  // al primer evento real, quitar el estado vacío del registro
  const empty = document.getElementById('logEmpty');
  if (empty) empty.remove();

  const now = new Date();
  const time = now.toLocaleTimeString('es-CO', { hour12: false, hour: '2-digit', minute: '2-digit' });

  const li = document.createElement('li');
  li.className = 'log-item';
  li.innerHTML = `
    <span class="log-time">${time}</span>
    <span class="log-dot log-dot--${level}"></span>
    <span class="log-text">${html}</span>
  `;

  list.prepend(li);

  // mantener el registro con un tamaño razonable
  const items = list.querySelectorAll('.log-item');
  if (items.length > 8) {
    items[items.length - 1].remove();
  }
}

/* ==========================================================
   Terminal de logs (vista registro)
   ========================================================== */
const termEstado = { id: null, live: false };

function initTerminal(){
  const sel = document.getElementById('termSelect');
  const refresh = document.getElementById('termRefresh');
  const live = document.getElementById('termLive');
  if (!sel || !refresh || !live) return;

  sel.addEventListener('change', () => {
    if (termEstado.live) setTermLive(false);
    const id = sel.value ? Number(sel.value) : null;
    termEstado.id = id;
    refresh.disabled = !id;
    live.disabled = !id;
    if (id) cargarTerminal(id);
    else escribirTerminal('// elige un servicio del panel para ver sus logs de systemd.\n// requiere que el servicio tenga una unidad systemd configurada.');
  });

  refresh.addEventListener('click', () => {
    if (termEstado.id) cargarTerminal(termEstado.id);
  });

  live.addEventListener('click', () => setTermLive(!termEstado.live));

  // cola en vivo: solo mientras la vista registro esté activa
  setInterval(() => {
    if (termEstado.live && termEstado.id && window.luminaView === 'registro') {
      cargarTerminal(termEstado.id, true);
    }
  }, 4000);
}

function setTermLive(on){
  termEstado.live = on;
  const live = document.getElementById('termLive');
  if (!live) return;
  live.classList.toggle('is-active', on);
  live.textContent = on ? 'live ●' : 'live';
}

function poblarTerminalSelect(){
  const sel = document.getElementById('termSelect');
  if (!sel) return;

  const conUnidad = estado.servicios.filter(s => s.servicio);
  sel.innerHTML = '';

  const refresh = document.getElementById('termRefresh');
  const live = document.getElementById('termLive');

  if (!conUnidad.length){
    const opt = document.createElement('option');
    opt.value = '';
    opt.textContent = 'sin servicios con unidad systemd';
    sel.appendChild(opt);
    sel.disabled = true;
    if (refresh) refresh.disabled = true;
    if (live) live.disabled = true;
    escribirTerminal('// aún no hay servicios con unidad systemd configurada.\n// cuando registres bots o webs con unidad, sus logs aparecerán aquí.');
    return;
  }

  sel.disabled = false;
  const def = document.createElement('option');
  def.value = '';
  def.textContent = 'elige un servicio…';
  sel.appendChild(def);

  conUnidad.forEach(s => {
    const opt = document.createElement('option');
    opt.value = s.id;
    opt.textContent = `${s.nombre} · ${s.servicio}`;
    sel.appendChild(opt);
  });
}

async function cargarTerminal(id, silencioso = false){
  const body = document.getElementById('termBody');
  const title = document.getElementById('termTitle');
  const servicio = estado.servicios.find(s => s.id === id);

  if (title && servicio) title.textContent = `lumina · journalctl -u ${servicio.servicio} -n 300`;
  if (!silencioso) escribirTerminal('cargando logs…');

  try {
    const datos = await api(`/api/servicios/${id}/logs?lines=300`);
    const contenido = (datos.log || '').trim();
    const lineas = contenido ? contenido.split('\n') : ['// log vacío'];
    if (body) {
      body.innerHTML = lineas.map(linea => {
        const esc = escaper(linea);
        return `<div>${resaltarLog(esc) || '&nbsp;'}</div>`;
      }).join('');
    }
    scrollTerminal();
  } catch (error) {
    escribirTerminal(`// error al leer logs: ${error.message}\n// comprueba que la unidad existe y que systemd responde.`);
  }
}

function resaltarLog(esc){
  // el texto ya viene escapado (sin < >): solo coloreamos patrones conocidos.
  const re = new RegExp(
    [
      /(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?|\d{1,2}:\d{2}:\d{2})/,      // marca de tiempo
      /(?:ERROR|SEVERE|FATAL|PANIC|CRITICAL|FAILED|\bfailed\b|not found|Traceback)/i, // errores
      /(?:WARNING?|\bdeprecated\b)/i,                                                 // avisos
      /(?:INFO|NOTICE|Started|Stopped|Listening|Running on|startup)/i,                // estados ok
      /https?:\/\/[^\s"&<>]+/,                                                         // urls
      /(?:\d{1,3}\.){3}\d{1,3}(?::\d+)?/                                               // direcciones ip
    ].map(r => r.source).join('|'),
    'g'
  );

  const partes = [];
  let last = 0, m;
  while ((m = re.exec(esc))){
    if (m.index > last) partes.push(esc.slice(last, m.index));
    const cls = m[1] ? 'tok-time' : m[2] ? 'tok-err' : m[3] ? 'tok-warn'
              : m[4] ? 'tok-ok' : m[5] ? 'tok-url' : 'tok-ip';
    partes.push(`<span class="${cls}">${m[0]}</span>`);
    last = re.lastIndex;
  }
  if (last < esc.length) partes.push(esc.slice(last));
  return partes.join('');
}

function escribirTerminal(texto){
  const body = document.getElementById('termBody');
  if (!body) return;
  body.innerHTML = `<div class="term-placeholder">${escaper(texto)}</div>`;
  scrollTerminal();
}

function scrollTerminal(){
  const body = document.getElementById('termBody');
  if (body) body.scrollTop = body.scrollHeight;
}