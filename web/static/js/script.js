/* ==========================================================
   ProjectLumina — dashboard base
   Interacciones de la maqueta: reloj, navegación (hash),
   vistas, pestañas bots/webs y registro de actividad.
   Sin backend todavía: todo corre en memoria.
   Solo se registra actividad real (no se inventan datos).
   ========================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initClock();
  initNav();
  initServiceActions();
  initRefreshButton();
  initEmptyCard();
  initServiceTabs();
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

/* ---------- acciones sobre servicios (reiniciar / detener / logs) ---------- */
function initServiceActions(){
  document.querySelectorAll('.card[data-status]').forEach(card => {
    card.querySelectorAll('[data-action]').forEach(btn => {
      btn.addEventListener('click', () => {
        const action = btn.dataset.action;
        const name = card.querySelector('h3')?.textContent?.trim() || 'servicio';

        if (action === 'restart') {
          restartService(card, name);
        } else if (action === 'stop') {
          toggleServiceStatus(card, name);
        } else if (action === 'logs') {
          logEvent(`Consultando logs de <strong>${name}</strong>…`, 'ok');
        }
      });
    });
  });
}

function restartService(card, name){
  const pill = card.querySelector('.status-pill');
  const restartBtn = card.querySelector('[data-action="restart"]');
  if (!pill || !restartBtn) return;

  restartBtn.disabled = true;
  restartBtn.textContent = 'reiniciando…';
  pill.classList.remove('status-pill--online');
  pill.classList.add('status-pill--offline');
  pill.innerHTML = '<span class="pulse"></span> reiniciando';

  setTimeout(() => {
    pill.classList.remove('status-pill--offline');
    pill.classList.add('status-pill--online');
    pill.innerHTML = '<span class="pulse"></span> activo';
    restartBtn.disabled = false;
    restartBtn.textContent = 'reiniciar';
    logEvent(`<strong>${name}</strong> se reinició correctamente`, 'ok');
  }, 1400);
}

function toggleServiceStatus(card, name){
  const pill = card.querySelector('.status-pill');
  const stopBtn = card.querySelector('[data-action="stop"]');
  if (!pill || !stopBtn) return;

  const isOnline = card.dataset.status === 'online';

  if (isOnline) {
    card.dataset.status = 'offline';
    pill.classList.remove('status-pill--online');
    pill.classList.add('status-pill--offline');
    pill.innerHTML = '<span class="pulse"></span> detenido';
    stopBtn.textContent = 'iniciar';
    logEvent(`<strong>${name}</strong> se detuvo manualmente`, 'warn');
  } else {
    card.dataset.status = 'online';
    pill.classList.remove('status-pill--offline');
    pill.classList.add('status-pill--online');
    pill.innerHTML = '<span class="pulse"></span> activo';
    stopBtn.textContent = 'detener';
    logEvent(`<strong>${name}</strong> se inició manualmente`, 'ok');
  }
}

/* ---------- botón actualizar estado ---------- */
function initRefreshButton(){
  const btn = document.getElementById('refreshBtn');
  if (!btn) return;

  btn.addEventListener('click', () => {
    btn.classList.add('is-loading');
    btn.disabled = true;

    setTimeout(() => {
      btn.classList.remove('is-loading');
      btn.disabled = false;
      logEvent('Sin servicios registrados: no hay nada que comprobar todavía', 'warn');
    }, 700);
  });
}

/* ---------- tarjeta vacía: invita a conectar un servicio ---------- */
function initEmptyCard(){
  document.querySelectorAll('#emptyServiceCard, .card--empty').forEach(card => {
    card.addEventListener('click', () => {
      logEvent('Conectar un servicio estará disponible en la versión v0.1', 'warn');
    });
  });

  document.querySelectorAll('#addServiceLink, #addServiceBtn').forEach(btn => {
    btn.addEventListener('click', () => {
      logEvent('Conectar un servicio estará disponible en la versión v0.1', 'warn');
    });
  });
}

/* ---------- panel de servicios: selector bots / webs ---------- */
function initServiceTabs(){
  const tabs = document.querySelectorAll('.tab[data-type]');
  const count = document.getElementById('tabCount');
  if (!tabs.length) return;

  // conteo real de servicios registrados por tipo (0 mientras no haya backend)
  const totals = { bot: 0, web: 0 };

  const setActiveTab = (type) => {
    tabs.forEach(tab => {
      const isActive = tab.dataset.type === type;
      tab.classList.toggle('is-active', isActive);
      tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
    });

    document.querySelectorAll('[data-type-panel]').forEach(panel => {
      panel.classList.toggle('is-visible', panel.dataset.typePanel === type);
    });

    if (count) {
      const label = type === 'bot' ? 'bots' : 'webs';
      count.textContent = `${totals[type]} ${label}`;
    }
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
