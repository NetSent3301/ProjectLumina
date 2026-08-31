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
  initServiceTabs();
  loadServicios();
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
  try {
    await estado.cargar();
  } catch (error) {
    sinAPI(error.message);
    return;
  }
  renderServicios();
}

function renderServicios(){
  renderCuerpo();
  renderVacios();
  renderContadores();
  renderResumen();
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

    btn.classList.remove('is-loading');
    btn.disabled = false;
    const total = estado.servicios.length;
    logEvent(total === 0
      ? 'Sin servicios registrados: no hay nada que comprobar todavía'
      : `Estado actualizado: ${total} ${total === 1 ? 'servicio' : 'servicios'} · ${estado.servicios.filter(s => s.estado === 'online').length} en línea`, 'ok');
  });
}

/* ---------- tarjeta vacía: futuro conectar un servicio ---------- */
function initEmptyCard(){
  [document.getElementById('emptyServiceCard'), document.querySelector('.card--empty')].forEach(card => {
    if (card) card.addEventListener('click', () => {
      logEvent('La interfaz para añadir servicios llegará en una próxima iteración de v0.1', 'warn');
    });
  });

  document.querySelectorAll('#addServiceLink, #addServiceBtn').forEach(btn => {
    btn.addEventListener('click', () => {
      logEvent('La interfaz para añadir servicios llegará en una próxima iteración de v0.1', 'warn');
    });
  });
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