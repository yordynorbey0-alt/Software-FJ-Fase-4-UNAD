"""Demostración de Software FJ con operaciones válidas e inválidas."""
import logging
from pathlib import Path
from excepciones import ErrorSoftwareFJ
from gestor import GestorSoftwareFJ
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada


def configurar_logs():
    """Registra eventos y errores en un archivo; no guarda datos de clientes."""
    directorio = Path(__file__).resolve().parent / 'logs'
    directorio.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=directorio / 'eventos.log', level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        encoding='utf-8', force=True
    )


def ejecutar_operacion(numero, descripcion, funcion):
    """Una falla se registra sin impedir la siguiente operación.

    Incluye try/except/else/finally; la excepción original se conserva
    y se reporta con logging.exception (traza de depuración).
    """
    print(f'\n{numero:02d}. {descripcion}')
    try:
        resultado = funcion()
    except ErrorSoftwareFJ as exc:
        logging.exception('Error controlado en operación %s', numero)
        print(f'   ERROR CONTROLADO: {exc}')
    except Exception as exc:
        logging.exception('Falla inesperada en operación %s', numero)
        print(f'   ERROR INESPERADO: {type(exc).__name__}: {exc}')
    else:
        print(f'   CORRECTO: {resultado if resultado is not None else "Operación completada"}')
        logging.info('Operación %s correcta: %s', numero, descripcion)
    finally:
        logging.info('Finalizó la operación %s', numero)


def demostracion():
    configurar_logs()
    gestor = GestorSoftwareFJ()
    operaciones = [
        ('Registrar cliente válido', lambda: gestor.registrar_cliente('101', 'Ana López', 'ana@ejemplo.com')),
        ('Rechazar correo inválido', lambda: gestor.registrar_cliente('102', 'Luis Pérez', 'correo-invalido')),
        ('Registrar segundo cliente', lambda: gestor.registrar_cliente('103', 'Luis Pérez', 'luis@ejemplo.com')),
        ('Rechazar identificación duplicada', lambda: gestor.registrar_cliente('101', 'Otra Persona', 'otra@ejemplo.com')),
        ('Crear servicio de sala', lambda: gestor.registrar_servicio(ReservaSala('S1', 'Sala de reuniones', 50000))),
        ('Crear alquiler de equipos', lambda: gestor.registrar_servicio(AlquilerEquipo('E1', 'Proyector', 70000))),
        ('Crear asesoría', lambda: gestor.registrar_servicio(AsesoriaEspecializada('A1', 'Asesoría Python', 80000))),
        ('Rechazar servicio con tarifa negativa', lambda: gestor.registrar_servicio(ReservaSala('S2', 'Sala B', -100))),
        ('Crear reserva válida', lambda: gestor.crear_reserva('R1', '101', 'S1', 2)),
        ('Confirmar reserva', lambda: gestor.obtener_reserva('R1').confirmar()),
        ('Procesar con IVA 19 % y descuento 10 %', lambda: gestor.obtener_reserva('R1').procesar(impuesto=19, descuento=10)),
        ('Rechazar reserva de duración inválida', lambda: gestor.crear_reserva('R2', '103', 'E1', 40)),
        ('Crear reserva de equipo', lambda: gestor.crear_reserva('R3', '103', 'E1', 3)),
        ('Cancelar reserva', lambda: gestor.obtener_reserva('R3').cancelar()),
        ('Rechazar procesamiento de reserva cancelada', lambda: gestor.obtener_reserva('R3').procesar()),
        ('Crear reserva de asesoría', lambda: gestor.crear_reserva('R4', '101', 'A1', 1.5)),
        ('Confirmar asesoría', lambda: gestor.obtener_reserva('R4').confirmar()),
        ('Procesar asesoría', lambda: gestor.obtener_reserva('R4').procesar()),
    ]
    print('SOFTWARE FJ | FASE 4 | SIMULACIÓN SIN BASE DE DATOS')
    for numero, (descripcion, funcion) in enumerate(operaciones, 1):
        ejecutar_operacion(numero, descripcion, funcion)
    print('\nRESUMEN:', gestor.resumen())
    print('Registro de eventos: logs/eventos.log')


if __name__ == '__main__':
    demostracion()
