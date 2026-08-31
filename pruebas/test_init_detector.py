"""Tests unitarios del detector de init system y de cada backend concreto.

Estos tests usan ``unittest.mock.patch`` para simular la presencia o ausencia
de binarios en PATH (``shutil.which``) y el resultado de subprocesos
(``subprocess.run``), sin necesidad de tener systemd, OpenRC, Runit o SysV
instalados en la máquina donde corren los tests.

Estructura de este archivo:
    * ``TestDetector``         — prueba que el detector elije el backend correcto.
    * ``TestSystemdBackend``   — prueba las operaciones del backend systemd.
    * ``TestOpenRCBackend``    — prueba las operaciones del backend OpenRC.
    * ``TestRunitBackend``     — prueba las operaciones del backend Runit.
    * ``TestSysVBackend``      — prueba las operaciones del backend SysV.
    * ``TestInitError``        — prueba los atributos de la excepción InitError.

Convención de naming:
    ``test_<método>_<condición>`` para que los nombres sean autoexplicativos
    sin necesidad de leer el cuerpo del test.
"""

from __future__ import annotations  # Anotaciones de tipo como strings.

import subprocess  # Para construir objetos CompletedProcess en los mocks.
from unittest.mock import MagicMock, patch  # Herramientas de mocking de la stdlib.

import pytest  # Framework de testing.

# Importamos el módulo completo del detector para poder resetear el caché.
from app.system import detector as detector_mod
from app.system import resetear_cache

# Importamos los backends concretos para testearlos directamente.
from app.system.base import InitError
from app.system.systemd import SystemdBackend
from app.system.openrc import OpenRCBackend
from app.system.runit import RunitBackend
from app.system.sysv import SysVBackend


# ─────────────────────────────────────────────────────────────────────────────
# Fixture: reset del caché antes de cada test
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def limpiar_cache():
    """Fixture que resetea el caché del detector antes y después de cada test.

    ``autouse=True`` significa que se aplica automáticamente a todos los tests
    de este módulo sin necesidad de declararlo explícitamente en cada función.

    Esto garantiza que los tests sean independientes entre sí: un test que
    llame a ``get_backend()`` no contamina el estado de los siguientes.
    """
    resetear_cache()   # Limpiamos antes del test.
    yield              # Aquí corre el test.
    resetear_cache()   # Limpiamos después del test (por si el test falla a mitad).


# ─────────────────────────────────────────────────────────────────────────────
# Helper: construir un CompletedProcess falso
# ─────────────────────────────────────────────────────────────────────────────

def _proc(stdout: str = "", stderr: str = "", returncode: int = 0) -> subprocess.CompletedProcess:
    """Crea un objeto ``CompletedProcess`` simulado para usar en mocks.

    Args:
        stdout:     Texto de salida estándar del proceso simulado.
        stderr:     Texto de error estándar del proceso simulado.
        returncode: Código de retorno del proceso simulado.

    Returns:
        Un ``CompletedProcess`` con los valores indicados.
    """
    # Usamos un objeto real de CompletedProcess para que los tests sean lo más
    # cercanos posible al comportamiento real de subprocess.run.
    result = subprocess.CompletedProcess(args=[], returncode=returncode)
    result.stdout = stdout
    result.stderr = stderr
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Tests: InitError
# ─────────────────────────────────────────────────────────────────────────────

class TestInitError:
    """Prueba los atributos y comportamiento de la excepción base InitError."""

    def test_mensaje_guardado(self):
        """El mensaje pasado al constructor se guarda en el atributo ``mensaje``."""
        error = InitError("algo salió mal")
        assert error.mensaje == "algo salió mal"

    def test_no_existe_por_defecto_es_false(self):
        """El flag ``no_existe`` es False por defecto."""
        error = InitError("cualquier error")
        assert error.no_existe is False

    def test_no_existe_se_puede_activar(self):
        """El flag ``no_existe`` se puede poner a True en el constructor."""
        error = InitError("servicio no encontrado", no_existe=True)
        assert error.no_existe is True

    def test_es_subclase_de_runtime_error(self):
        """InitError hereda de RuntimeError para compatibilidad con código existente."""
        error = InitError("test")
        assert isinstance(error, RuntimeError)

    def test_str_muestra_el_mensaje(self):
        """str(InitError) devuelve el mensaje (comportamiento de RuntimeError)."""
        error = InitError("mensaje de prueba")
        assert "mensaje de prueba" in str(error)


# ─────────────────────────────────────────────────────────────────────────────
# Tests: Detector
# ─────────────────────────────────────────────────────────────────────────────

class TestDetector:
    """Prueba que el detector selecciona el backend correcto según el entorno."""

    @patch("shutil.which")
    def test_detecta_systemd_primero(self, mock_which):
        """Si systemctl está en PATH, el detector elige SystemdBackend."""
        # Configuramos el mock: ``which("systemctl")`` devuelve un path,
        # ``which`` para cualquier otro binario devuelve None.
        mock_which.side_effect = lambda cmd: "/usr/bin/systemctl" if cmd == "systemctl" else None

        backend = detector_mod.detectar()

        assert isinstance(backend, SystemdBackend)
        assert backend.nombre() == "systemd"

    @patch("shutil.which")
    def test_detecta_openrc_cuando_no_hay_systemd(self, mock_which):
        """Si no hay systemctl pero hay rc-service, elige OpenRCBackend."""
        def which_impl(cmd: str) -> str | None:
            # Simulamos un sistema Alpine: rc-service existe, systemctl no.
            return "/sbin/rc-service" if cmd == "rc-service" else None

        mock_which.side_effect = which_impl

        backend = detector_mod.detectar()

        assert isinstance(backend, OpenRCBackend)
        assert backend.nombre() == "openrc"

    @patch("shutil.which")
    def test_detecta_runit_cuando_no_hay_systemd_ni_openrc(self, mock_which):
        """Si hay sv pero no systemctl ni rc-service, elige RunitBackend."""
        def which_impl(cmd: str) -> str | None:
            # Simulamos un sistema Void Linux con runit.
            return "/usr/bin/sv" if cmd == "sv" else None

        mock_which.side_effect = which_impl

        backend = detector_mod.detectar()

        assert isinstance(backend, RunitBackend)
        assert backend.nombre() == "runit"

    @patch("shutil.which")
    def test_detecta_sysv_como_fallback(self, mock_which):
        """Si solo está ``service``, elige SysVBackend."""
        def which_impl(cmd: str) -> str | None:
            # Simulamos un sistema Devuan con SysV.
            return "/usr/sbin/service" if cmd == "service" else None

        mock_which.side_effect = which_impl

        backend = detector_mod.detectar()

        assert isinstance(backend, SysVBackend)
        assert backend.nombre() == "sysv"

    @patch("shutil.which", return_value=None)  # Ningún binario existe.
    @patch("pathlib.Path.exists", return_value=False)  # /etc/init.d/ tampoco.
    @patch("pathlib.Path.iterdir", return_value=iter([]))  # Directorio vacío.
    def test_lanza_error_si_no_hay_backend(self, _iter, _exists, _which):
        """Si ningún init system está disponible, lanza RuntimeError."""
        with pytest.raises(RuntimeError, match="No se detectó ningún init system"):
            detector_mod.detectar()

    @patch("shutil.which")
    def test_get_backend_cachea_el_resultado(self, mock_which):
        """``get_backend()`` devuelve el mismo objeto en llamadas sucesivas."""
        mock_which.side_effect = lambda cmd: "/usr/bin/systemctl" if cmd == "systemctl" else None

        backend1 = detector_mod.get_backend()
        backend2 = detector_mod.get_backend()

        # Deben ser exactamente el mismo objeto (identidad, no solo igualdad).
        assert backend1 is backend2

    @patch("shutil.which")
    def test_resetear_cache_fuerza_redeteccion(self, mock_which):
        """Después de ``resetear_cache()``, ``get_backend()`` re-detecta y devuelve
        el mismo backend (las instancias de ``_BACKENDS_ORDENADOS`` son singletons
        pre-creados, por lo que el objeto retornado es idéntico por tipo y referencia).

        Lo que verificamos es que el caché fue efectivamente limpiado y que tras
        la limpieza la detección produce un backend del mismo tipo.
        """
        mock_which.side_effect = lambda cmd: "/usr/bin/systemctl" if cmd == "systemctl" else None

        backend1 = detector_mod.get_backend()

        # Confirmamos que el caché está poblado.
        assert detector_mod._backend_cache is not None

        resetear_cache()  # Limpiamos el caché.

        # Después del reset el caché debe estar vacío.
        assert detector_mod._backend_cache is None

        backend2 = detector_mod.get_backend()  # Re-detección.

        # Tras la re-detección el tipo debe ser el mismo (systemd en ambos casos).
        assert type(backend1) is type(backend2)
        # El caché vuelve a estar poblado.
        assert detector_mod._backend_cache is not None


# ─────────────────────────────────────────────────────────────────────────────
# Tests: SystemdBackend
# ─────────────────────────────────────────────────────────────────────────────

class TestSystemdBackend:
    """Prueba el backend de systemd sin necesidad de tener systemd instalado."""

    def setup_method(self):
        """Crea una instancia fresca del backend para cada test."""
        self.backend = SystemdBackend()

    @patch("shutil.which", return_value="/usr/bin/systemctl")
    @patch("subprocess.run")
    def test_is_active_devuelve_true_cuando_activo(self, mock_run, _which):
        """``is_active`` devuelve True cuando systemctl reporta 'active'."""
        mock_run.return_value = _proc(stdout="active\n", returncode=0)

        assert self.backend.is_active("nginx.service") is True

    @patch("shutil.which", return_value="/usr/bin/systemctl")
    @patch("subprocess.run")
    def test_is_active_devuelve_false_cuando_inactivo(self, mock_run, _which):
        """``is_active`` devuelve False cuando systemctl reporta 'inactive'."""
        mock_run.return_value = _proc(stdout="inactive\n", returncode=1)

        assert self.backend.is_active("nginx.service") is False

    @patch("shutil.which", return_value=None)  # systemctl no existe.
    def test_is_active_devuelve_false_sin_systemctl(self, _which):
        """``is_active`` devuelve False silenciosamente si systemctl no está disponible."""
        # No debe lanzar InitError; solo devuelve False.
        assert self.backend.is_active("cualquier.service") is False

    @patch("shutil.which", return_value="/usr/bin/systemctl")
    @patch("subprocess.run")
    def test_iniciar_exitoso(self, mock_run, _which):
        """``iniciar`` no lanza excepciones cuando el comando tiene éxito."""
        mock_run.return_value = _proc(returncode=0)

        # No debe lanzar ninguna excepción.
        self.backend.iniciar("nginx.service")

    @patch("shutil.which", return_value="/usr/bin/systemctl")
    @patch("subprocess.run")
    def test_iniciar_lanza_init_error_si_falla(self, mock_run, _which):
        """``iniciar`` lanza InitError cuando systemctl devuelve exit != 0."""
        mock_run.return_value = _proc(stderr="Failed to start nginx.service", returncode=1)

        with pytest.raises(InitError):
            self.backend.iniciar("nginx.service")

    @patch("shutil.which", return_value="/usr/bin/systemctl")
    @patch("subprocess.run")
    def test_iniciar_marca_no_existe_correctamente(self, mock_run, _which):
        """``iniciar`` pone ``no_existe=True`` cuando systemd dice 'not found'."""
        mock_run.return_value = _proc(
            stderr="Unit nginx.service not found.", returncode=1
        )

        with pytest.raises(InitError) as exc_info:
            self.backend.iniciar("nginx.service")

        # Verificamos el flag no_existe para que la API devuelva 404.
        assert exc_info.value.no_existe is True

    @patch("shutil.which", return_value="/usr/bin/systemctl")
    @patch("subprocess.run")
    def test_servicios_activos_parsea_correctamente(self, mock_run, _which):
        """``servicios_activos`` parsea la salida de systemctl list-units."""
        salida = (
            "nginx.service          loaded active running NGINX server\n"
            "sshd.service           loaded active running OpenSSH Daemon\n"
        )
        mock_run.return_value = _proc(stdout=salida, returncode=0)

        resultado = self.backend.servicios_activos()

        # Deben haber exactamente 2 servicios.
        assert len(resultado) == 2
        # El primer servicio debe ser nginx.
        assert resultado[0]["unidad"] == "nginx.service"
        # El segundo servicio debe ser sshd.
        assert resultado[1]["unidad"] == "sshd.service"

    @patch("shutil.which", return_value="/usr/bin/systemctl")
    @patch("subprocess.run")
    def test_nombre_y_disponible(self, mock_run, mock_which):
        """``nombre()`` devuelve 'systemd' y ``disponible()`` es True si which funciona."""
        assert self.backend.nombre() == "systemd"
        assert self.backend.disponible() is True  # mock_which devuelve path no-None.


# ─────────────────────────────────────────────────────────────────────────────
# Tests: OpenRCBackend
# ─────────────────────────────────────────────────────────────────────────────

class TestOpenRCBackend:
    """Prueba el backend de OpenRC simulando el entorno Alpine Linux."""

    def setup_method(self):
        """Crea una instancia fresca del backend para cada test."""
        self.backend = OpenRCBackend()

    @patch("shutil.which", return_value="/sbin/rc-service")
    def test_nombre_y_disponible(self, _which):
        """``nombre()`` devuelve 'openrc' y ``disponible()`` es True si rc-service existe."""
        assert self.backend.nombre() == "openrc"
        assert self.backend.disponible() is True

    @patch("shutil.which", return_value=None)
    def test_disponible_false_sin_rc_service(self, _which):
        """``disponible()`` es False si rc-service no está en PATH."""
        assert self.backend.disponible() is False

    @patch("shutil.which", return_value="/sbin/rc-service")
    @patch("subprocess.run")
    def test_is_active_devuelve_true_con_exit_0(self, mock_run, _which):
        """``is_active`` devuelve True cuando rc-service status devuelve exit 0."""
        mock_run.return_value = _proc(stdout=" * status: started\n", returncode=0)

        assert self.backend.is_active("nginx") is True

    @patch("shutil.which", return_value="/sbin/rc-service")
    @patch("subprocess.run")
    def test_is_active_devuelve_false_con_exit_1(self, mock_run, _which):
        """``is_active`` devuelve False cuando rc-service status devuelve exit != 0."""
        mock_run.return_value = _proc(stdout=" * status: stopped\n", returncode=1)

        assert self.backend.is_active("nginx") is False

    @patch("shutil.which", return_value="/sbin/rc-service")
    @patch("subprocess.run")
    def test_iniciar_exitoso(self, mock_run, _which):
        """``iniciar`` no lanza si rc-service start tiene éxito."""
        mock_run.return_value = _proc(returncode=0)

        self.backend.iniciar("nginx")  # No debe lanzar.

    @patch("shutil.which", return_value="/sbin/rc-service")
    @patch("subprocess.run")
    def test_iniciar_lanza_init_error_con_no_existe(self, mock_run, _which):
        """``iniciar`` lanza InitError con no_existe=True si OpenRC dice 'does not exist'."""
        mock_run.return_value = _proc(
            stderr="Service nginx does not exist", returncode=1
        )

        with pytest.raises(InitError) as exc_info:
            self.backend.iniciar("nginx")

        assert exc_info.value.no_existe is True

    @patch("shutil.which", return_value="/sbin/rc-service")
    @patch("subprocess.run")
    def test_servicios_activos_parsea_rc_status(self, mock_run, _which):
        """``servicios_activos`` parsea la salida de rc-status --all --nocolor."""
        salida = (
            "Runlevel: default\n"
            " * nginx                              [ started ]\n"
            " * sshd                               [ started ]\n"
            " * crond                              [ stopped ]\n"
        )
        mock_run.return_value = _proc(stdout=salida, returncode=0)

        resultado = self.backend.servicios_activos()

        # Solo los servicios "started" deben aparecer.
        assert len(resultado) == 2
        nombres = [s["unidad"] for s in resultado]
        assert "nginx" in nombres
        assert "sshd" in nombres
        assert "crond" not in nombres  # crond está stopped, no debe aparecer.


# ─────────────────────────────────────────────────────────────────────────────
# Tests: RunitBackend
# ─────────────────────────────────────────────────────────────────────────────

class TestRunitBackend:
    """Prueba el backend de Runit simulando el entorno Void Linux."""

    def setup_method(self):
        """Crea una instancia fresca del backend para cada test."""
        self.backend = RunitBackend()

    @patch("shutil.which", return_value="/usr/bin/sv")
    def test_nombre_y_disponible(self, _which):
        """``nombre()`` devuelve 'runit' y ``disponible()`` es True si sv existe."""
        assert self.backend.nombre() == "runit"
        assert self.backend.disponible() is True

    @patch("shutil.which", return_value="/usr/bin/sv")
    @patch("subprocess.run")
    def test_is_active_detecta_run_en_stdout(self, mock_run, _which):
        """``is_active`` devuelve True cuando sv status imprime 'run:' en stdout."""
        mock_run.return_value = _proc(
            stdout="run: nginx: (pid 1234) 300s\n", returncode=0
        )

        assert self.backend.is_active("nginx") is True

    @patch("shutil.which", return_value="/usr/bin/sv")
    @patch("subprocess.run")
    def test_is_active_devuelve_false_cuando_down(self, mock_run, _which):
        """``is_active`` devuelve False cuando sv status imprime 'down:'."""
        mock_run.return_value = _proc(
            stdout="down: nginx: 42s, normally up\n", returncode=1
        )

        assert self.backend.is_active("nginx") is False

    @patch("shutil.which", return_value="/usr/bin/sv")
    @patch("subprocess.run")
    def test_iniciar_usa_sv_up(self, mock_run, _which):
        """``iniciar`` llama a 'sv up <nombre>' (no 'sv start')."""
        mock_run.return_value = _proc(returncode=0)

        self.backend.iniciar("nginx")

        # Verificamos que el comando fue el correcto.
        args_llamada = mock_run.call_args[0][0]  # Primer argumento posicional de run.
        assert args_llamada == ["sv", "up", "nginx"]

    @patch("shutil.which", return_value="/usr/bin/sv")
    @patch("subprocess.run")
    def test_detener_usa_sv_down(self, mock_run, _which):
        """``detener`` llama a 'sv down <nombre>'."""
        mock_run.return_value = _proc(returncode=0)

        self.backend.detener("nginx")

        args_llamada = mock_run.call_args[0][0]
        assert args_llamada == ["sv", "down", "nginx"]

    @patch("shutil.which", return_value="/usr/bin/sv")
    @patch("subprocess.run")
    def test_iniciar_lanza_init_error_con_no_existe(self, mock_run, _which):
        """``iniciar`` lanza InitError con no_existe=True si runit dice 'unknown'."""
        mock_run.return_value = _proc(
            stderr="sv: warning: /var/service/nginx: unable to open", returncode=1
        )

        with pytest.raises(InitError) as exc_info:
            self.backend.iniciar("nginx")

        assert exc_info.value.no_existe is True


# ─────────────────────────────────────────────────────────────────────────────
# Tests: SysVBackend
# ─────────────────────────────────────────────────────────────────────────────

class TestSysVBackend:
    """Prueba el backend SysV (experimental) simulando el entorno Devuan."""

    def setup_method(self):
        """Crea una instancia fresca del backend para cada test."""
        self.backend = SysVBackend()

    @patch("shutil.which", return_value="/usr/sbin/service")
    def test_nombre_y_disponible(self, _which):
        """``nombre()`` devuelve 'sysv' y ``disponible()`` es True si service existe."""
        assert self.backend.nombre() == "sysv"
        assert self.backend.disponible() is True

    @patch("shutil.which", return_value="/usr/sbin/service")
    @patch("subprocess.run")
    def test_is_active_devuelve_true_con_exit_0(self, mock_run, _which):
        """``is_active`` devuelve True cuando service status devuelve exit 0."""
        mock_run.return_value = _proc(stdout="nginx is running.\n", returncode=0)

        assert self.backend.is_active("nginx") is True

    @patch("shutil.which", return_value="/usr/sbin/service")
    @patch("subprocess.run")
    def test_is_active_devuelve_false_con_exit_3(self, mock_run, _which):
        """``is_active`` devuelve False con exit 3 (convención SysV = parado)."""
        mock_run.return_value = _proc(stdout="nginx is not running.\n", returncode=3)

        assert self.backend.is_active("nginx") is False

    @patch("shutil.which", return_value="/usr/sbin/service")
    @patch("subprocess.run")
    def test_servicios_activos_parsea_status_all(self, mock_run, _which):
        """``servicios_activos`` parsea la salida de 'service --status-all'."""
        salida = (
            " [ + ]  nginx\n"
            " [ + ]  ssh\n"
            " [ - ]  apache2\n"
            " [ ? ]  ufw\n"
        )
        mock_run.return_value = _proc(stdout=salida, returncode=0)

        resultado = self.backend.servicios_activos()

        # Solo los servicios con "[ + ]" deben aparecer.
        assert len(resultado) == 2
        nombres = [s["unidad"] for s in resultado]
        assert "nginx" in nombres
        assert "ssh" in nombres
        assert "apache2" not in nombres  # Parado → no incluir.
        assert "ufw" not in nombres      # Desconocido → no incluir.

    def test_info_contiene_experimental_true(self):
        """``info()`` incluye el flag ``experimental: True`` para SysV."""
        with patch("shutil.which", return_value="/usr/sbin/service"):
            resultado = self.backend.info()

        # SysV siempre debe marcarse como experimental en los metadatos.
        assert resultado.get("experimental") is True
        assert resultado["backend"] == "sysv"
