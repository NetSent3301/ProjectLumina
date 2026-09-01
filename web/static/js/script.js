/* ==========================================================
   ProjectLumina — dashboard v0.1
   Reloj, navegación (hash), vistas, pestañas bots/webs y
   registro de actividad. Desde v0.1 consume la API REST:
     GET  /api/servicios                  listar con estado
     POST /api/servicios/{id}/{accion}    iniciar/detener/reiniciar
     GET  /api/servicios/{id}/logs        ver logs
     GET  /api/update                     chequeo de actualizaciones
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
  initServidores();
  initUpdateNotifications();
  loadServicios();
  loadMetricas();
  cargarConexion();
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

  ['f_servicio', 'f_check_url', 'f_nombre'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('input', updateSummary);
  });

  const form = document.getElementById('serviceForm');
  if (form) form.addEventListener('submit', conectarServicio);

  updateSummary();
}

function setModalTipo(tipo){
  modalTipo = tipo;
  document.querySelectorAll('.modal-tab').forEach(tab => {
    const isActive = tab.dataset.modalTipo === tipo;
    tab.classList.toggle('is-active', isActive);
    tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
  });

  const control = document.getElementById('controlWeb');
  if (control) control.classList.toggle('is-hidden', tipo !== 'web');

  const hint = document.getElementById('hintServicio');
  if (hint) {
    hint.innerHTML = tipo === 'bot'
      ? 'con unidad: podrás <strong>iniciar, detener, reiniciar y leer logs</strong>; sin unidad, el servicio solo queda registrado (se verá offline).'
      : 'si este servicio está bajo systemd también podrás <strong>iniciarlo, detenerlo y ver logs</strong>; sin unidad, solo se mostrará su estado por HTTP.';
  }

  updateSummary();
}

/* resumen en vivo: qué se podrá hacer con este servicio */
function updateSummary(){
  const servicio = (document.getElementById('f_servicio')?.value || '').trim();
  const check = (document.getElementById('f_check_url')?.value || '').trim();
  const tieneUnidad = !!servicio;
  const tieneCheck = !!check;

  let estado, acciones;
  if (modalTipo === 'bot'){
    estado = tieneUnidad
      ? 'en línea / offline según la unidad systemd'
      : 'offline · sin unidad que comprobar';
    acciones = tieneUnidad
      ? 'iniciar · detener · reiniciar · logs'
      : 'solo registro (sin acciones)';
  } else {
    estado = tieneCheck
      ? 'en línea si responde (HTTP < 400)'
      : 'offline · sin dirección que comprobar';
    acciones = tieneUnidad
      ? 'iniciar · detener · reiniciar · logs'
      : tieneCheck
        ? 'solo estado (por HTTP)'
        : 'solo registro (sin acciones)';
  }

  const e = document.getElementById('sumEstado');
  if (e) e.textContent = estado;
  const a = document.getElementById('sumAcciones');
  if (a) a.textContent = acciones;
}

function abrirModal(tipo = 'bot'){
  const modal = document.getElementById('serviceModal');
  if (!modal) return;

  ['f_nombre', 'f_servicio', 'f_check_url', 'f_comando', 'f_ruta'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = '';
  });
  ['f_auto_inicio', 'f_auto_reinicio'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.checked = false;
  });

  setModalTipo(tipo);
  ocultarError();
  updateSummary();

  modal.classList.add('is-open');
  modal.setAttribute('aria-hidden', 'false');
  const nombre = document.getElementById('f_nombre');
  if (nombre) setTimeout(() => nombre.focus(), 30);
}

function cerrarModal(){
  const modal = document.getElementById('serviceModal');
  if (!modal) return;
  modal.classList.remove('is-open');
  modal.setAttribute('aria-hidden', 'true');
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

    // llévate al panel para ver la tarjeta recién creada
    window.location.hash = '#/servicios';
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

/* ==========================================================
   Conexión y servidores remotos (agentes Lumina)
   ========================================================== */

let conexionTimer = null;

async function cargarConexion(primera = true){
  const badge = document.getElementById('connState');
  if (primera && badge) badge.classList.add('conn--checking');

  try {
    const datos = await api('/api/conexion');
    renderIndicadorConexion(datos);
    renderVistaConexion(datos);
  } catch (error) {
    // Sin acceso al servidor principal no inventamos conexiones:
    // se marca el corte y los datos siguen donde quedaron.
    renderIndicadorConexion(null, error.message);
  }

  if (!conexionTimer) {
    conexionTimer = setInterval(() => cargarConexion(false), 15000);
  }
}

/* ---------- indicador global en la barra lateral ---------- */
function renderIndicadorConexion(datos, error){
  const badge = document.getElementById('connState');
  const texto = document.getElementById('connText');
  if (!badge || !texto) return;

  let clase, mensaje, titulo;

  if (!datos){
    clase = 'conn--off';
    mensaje = 'sin acceso al servidor principal';
    titulo = `no se pudo contactar la API local (${error || 'error desconocido'}). Sin conexión no hay datos en vivo.`;
  } else {
    const { total_remotos, conectado_a, sin_acceso_a } = datos;
    if (total_remotos === 0){
      clase = 'conn--ok';
      mensaje = 'conectado · este equipo';
      titulo = 'conexión establecida con el servidor principal. Aún no hay servidores remotos registrados.';
    } else if (sin_acceso_a === 0){
      clase = 'conn--ok';
      mensaje = `conectado a ${conectado_a + 1} servidores`;
      titulo = 'servidor principal y todos los remotos responden.';
    } else if (conectado_a === 0){
      clase = 'conn--off';
      mensaje = `sin acceso a ningún servidor remoto`;
      titulo = `el servidor principal responde, pero ${sin_acceso_a} remoto(s) no se alcanza(n).`;
    } else {
      clase = 'conn--warn';
      mensaje = `sin acceso a ${sin_acceso_a} servidor(es)`;
      titulo = `el principal y ${conectado_a} remoto(s) responden; ${sin_acceso_a} no se alcanza(n).`;
    }
  }

  badge.classList.remove('conn--checking', 'conn--ok', 'conn--warn', 'conn--off');
  badge.classList.add(clase);
  texto.textContent = mensaje;
  badge.setAttribute('title', titulo);
}

/* ---------- vista servidores ---------- */
function initServidores(){
  const form = document.getElementById('serverForm');
  if (form) form.addEventListener('submit', registrarServidor);

  const grid = document.getElementById('servidoresGrid');
  if (grid){
    grid.addEventListener('click', async (event) => {
      const btn = event.target.closest('[data-sop]');
      if (!btn) return;
      const card = btn.closest('.card[data-id]');
      if (!card) return;

      const id = card.dataset.id;
      const nombre = card.querySelector('h3')?.textContent?.trim() || 'servidor';
      try {
        await api(`/api/servidores/${id}`, { method: 'DELETE' });
        logEvent(`se dejó de gestionar <strong>${escapar(nombre)}</strong>`, 'ok');
        await cargarConexion(false);
      } catch (error) {
        logEvent(`error al quitar <strong>${escapar(nombre)}</strong>: ${escapar(error.message)}`, 'warn');
      }
    });
  }
}

async function registrarServidor(event){
  event.preventDefault();

  const nombre = document.getElementById('sv_nombre')?.value.trim() || '';
  const url = document.getElementById('sv_url')?.value.trim() || '';
  if (!nombre || !url) return;

  const submit = event.target.querySelector('[type="submit"]');
  if (submit){
    submit.disabled = true;
    const icon = submit.querySelector('.btn-icon');
    if (icon) icon.textContent = '…';
  }

  try {
    const creado = await api('/api/servidores', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        nombre,
        url,
        token: document.getElementById('sv_token')?.value.trim() || '',
      }),
    });

    logEvent(
      `servidor remoto <strong>${escapar(creado.nombre)}</strong> registrado · conexión: <strong>${creado.conexion ? 'alcanzable' : 'sin acceso'}</strong>`,
      creado.conexion ? 'ok' : 'warn'
    );

    ['sv_nombre', 'sv_url', 'sv_token'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.value = '';
    });
    await cargarConexion(false);
  } catch (error) {
    logEvent(`no se pudo registrar el servidor: ${escapar(error.message)}`, 'warn');
  } finally {
    if (submit){
      submit.disabled = false;
      const icon = submit.querySelector('.btn-icon');
      if (icon) icon.textContent = '+';
    }
  }
}

function renderVistaConexion(datos){
  // tarjetas de conexión (principal + remotos)
  const conex = document.getElementById('conexionGrid');
  if (conex){
    conex.innerHTML = '';
    conex.appendChild(tarjetaPrincipal());

    if (datos.servidores.length){
      datos.servidores.forEach(s => conex.appendChild(tarjetaConexion(s)));
    } else {
      conex.appendChild(tarjetaVacia(
        'no hay servidores remotos',
        'registra uno arriba y Lumina lo comprobará cada 15 segundos.'
      ));
    }
  }

  // resumen compacto
  const resumen = document.getElementById('connResumen');
  if (resumen){
    const { total_remotos, conectado_a, sin_acceso_a } = datos;
    resumen.textContent = total_remotos === 0
      ? 'solo este equipo'
      : sin_acceso_a === 0
        ? `${total_remotos} ${total_remotos === 1 ? 'remoto' : 'remotos'} conectados`
        : `${conectado_a} conectados · ${sin_acceso_a} sin acceso`;
  }

  // lista de registrados con sus acciones
  const grid = document.getElementById('servidoresGrid');
  if (grid){
    grid.innerHTML = '';
    if (datos.servidores.length){
      datos.servidores.forEach(s => grid.appendChild(tarjetaRegistrado(s)));
    } else {
      grid.appendChild(tarjetaVacia(
        'sin servidores registrados',
        'las tarjetas de arriba muestran la conexión; aquí aparecen los que puedas quitar.'
      ));
    }
  }
}

function tarjetaPrincipal(){
  const card = document.createElement('article');
  card.className = 'card';
  card.innerHTML = `
    <div class="card-top">
      <div class="card-title">
        <span class="card-icon">🖥️</span>
        <div>
          <h3>servidor principal</h3>
          <p class="card-sub">este equipo · el panel se sirve aquí</p>
        </div>
      </div>
      <span class="status-pill status-pill--online"><span class="pulse"></span> conectado</span>
    </div>
    <dl class="card-stats">
      <div><dt>acceso</dt><dd>directo · su propia API</dd></div>
      <div><dt>servicios</dt><dd>los de este equipo</dd></div>
    </dl>
  `;
  return card;
}

function tarjetaConexion(s){
  const ok = s.conexion;
  const card = document.createElement('article');
  card.className = 'card';
  card.innerHTML = `
    <div class="card-top">
      <div class="card-title">
        <span class="card-icon">🌍</span>
        <div>
          <h3>${escapar(s.nombre)}</h3>
          <p class="card-sub">${escapar(s.url)}</p>
        </div>
      </div>
      <span class="status-pill status-pill--${ok ? 'online' : 'offline'}">
        <span class="pulse"></span> ${ok ? 'conectado' : 'sin acceso'}
      </span>
    </div>
    <dl class="card-stats">
      <div><dt>estado</dt><dd>${escapar(s.detalle)}</dd></div>
      <div><dt>comprobado</dt><dd>${formatearHora(s.ultimo_check)}</dd></div>
    </dl>
  `;
  return card;
}

function tarjetaRegistrado(s){
  const card = document.createElement('article');
  card.className = 'card';
  card.dataset.id = s.id;
  card.innerHTML = `
    <div class="card-top">
      <div class="card-title">
        <span class="card-icon">🌍</span>
        <div>
          <h3>${escapar(s.nombre)}</h3>
          <p class="card-sub">${escapar(s.url)}</p>
        </div>
      </div>
      <span class="status-pill status-pill--${s.conexion ? 'online' : 'offline'}">
        <span class="pulse"></span> ${s.conexion ? 'alcanzable' : 'sin acceso'}
      </span>
    </div>
    <div class="card-actions">
      <button class="btn-ghost is-danger" data-sop="eliminar">quitar</button>
    </div>
  `;
  return card;
}

function tarjetaVacia(titulo, sub){
  const vacio = document.createElement('article');
  vacio.className = 'card card--empty is-visible';
  vacio.innerHTML = `
    <p class="card-empty-title">${titulo}</p>
    <p class="card-empty-sub">${sub}</p>
  `;
  return vacio;
}

function formatearHora(iso){
  if (!iso) return '—';
  const fecha = new Date(iso);
  return isNaN(fecha) ? '—' : fecha.toLocaleTimeString('es-CO', { hour12: false });
}

/* ==========================================================
   Notificaciones de Actualización (GitHub Releases)
   ========================================================== */

let updateTimer = null;
let updateDismissed = false;

async function initUpdateNotifications(){
  // Verificar si el usuario ya dismissó la notificación actual
  const dismissed = localStorage.getItem('lumina_update_dismissed');
  if (dismissed){
    try {
      const data = JSON.parse(dismissed);
      if (data.version && data.hasta && new Date(data.hasta) > new Date()){
        updateDismissed = true;
        return;
      }
    } catch {}
  }

  // Chequeo inicial
  await chequearActualizacion();

  // Programar chequeos periódicos (cada 30 min en frontend como respaldo)
  if (!updateTimer){
    updateTimer = setInterval(async () => {
      if (!updateDismissed) await chequearActualizacion();
    }, 30 * 60 * 1000); // 30 min
  }
}

async function chequearActualizacion(forzar = false){
  try {
    const res = await fetch('/api/update' + (forzar ? '?forzar=true' : ''));
    if (!res.ok) return;
    const data = await res.json();

    if (data.hay_actualizacion && !updateDismissed){
      mostrarNotificacionActualizacion(data);
    }
  } catch (e) {
    // Silencioso: no molestar si falla el chequeo
    console.debug('Update check failed:', e);
  }
}

function mostrarNotificacionActualizacion(data){
  // Crear contenedor de notificaciones si no existe
  let container = document.getElementById('updateNotifications');
  if (!container){
    container = document.createElement('div');
    container.id = 'updateNotifications';
    container.className = 'update-notifications';
    document.body.appendChild(container);
  }

  // Evitar duplicados
  if (container.querySelector(`[data-version="${data.version_nueva}"]`)) return;

  const notif = document.createElement('div');
  notif.className = 'update-notification update-notification--new';
  notif.dataset.version = data.version_nueva;
  notif.innerHTML = `
    <div class="update-notification__icon">🔔</div>
    <div class="update-notification__content">
      <h4>Nueva versión disponible: v${data.version_nueva}</h4>
      <p>Estás en v${data.version_actual}. <a href="${data.release_url}" target="_blank" rel="noopener">Ver cambios en GitHub</a></p>
      ${data.release_notes ? `<details class="update-notification__changelog"><summary>Notas de la versión</summary><div>${escapeHtml(data.release_notes.slice(0, 500))}${data.release_notes.length > 500 ? '…' : ''}</div></details>` : ''}
    </div>
    <div class="update-notification__actions">
      <button class="btn-ghost" data-action="dismiss" title="No volver a avisar 24h">✕</button>
      <button class="btn-primary" data-action="refresh">Actualizar ahora</button>
    </div>
  `;

  // Eventos
  notif.querySelector('[data-action="dismiss"]').addEventListener('click', () => {
    dismissUpdateNotification(data.version_nueva, 24);
    notif.remove();
  });
  notif.querySelector('[data-action="refresh"]').addEventListener('click', async () => {
    notif.querySelector('[data-action="refresh"]').disabled = true;
    notif.querySelector('[data-action="refresh"]').textContent = 'Comprobando…';
    await chequearActualizacion(true);
    notif.remove();
  });

  container.appendChild(notif);

  // Auto-remove after 30 seconds if not interacted
  setTimeout(() => {
    if (notif.parentNode) notif.classList.add('update-notification--fade');
    setTimeout(() => notif.remove(), 500);
  }, 30000);
}

async function dismissUpdateNotification(version, horas){
  updateDismissed = true;
  const hasta = new Date(Date.now() + horas * 3600 * 1000).toISOString();
  localStorage.setItem('lumina_update_dismissed', JSON.stringify({ version, hasta }));

  // Notificar al backend (requiere token)
  const token = localStorage.getItem('lumina_token');
  if (token){
    try {
      await fetch('/api/update/dismiss', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-API-Key': token },
        body: JSON.stringify({ version, horas })
      });
    } catch {}
  }

  // Re-activar chequeos después del tiempo de dismiss
  setTimeout(() => {
    updateDismissed = false;
    localStorage.removeItem('lumina_update_dismissed');
    chequearActualizacion();
  }, horas * 3600 * 1000);
}

function escapeHtml(text){
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}