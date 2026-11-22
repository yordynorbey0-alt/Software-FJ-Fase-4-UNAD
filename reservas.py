"""Reservas, transiciones de estado y procesamiento seguro."""
from decimal import Decimal
from entidades import Cliente
from servicios import Servicio, decimal_positivo
from excepciones import DatosInvalidosError, ReservaInvalidaError


class Reserva:
    """Una reserva pasa de PENDIENTE a CONFIRMADA o CANCELADA."""

    def __init__(self, codigo, cliente, servicio, duracion):
        if not isinstance(codigo, str) or not codigo.strip():
            raise DatosInvalidosError('El código de reserva es obligatorio.')
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise DatosInvalidosError('La reserva exige cliente y servicio válidos.')
        self.codigo = codigo.strip()
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = decimal_positivo(duracion, 'La duración')
        self.estado = 'PENDIENTE'
        self.total = Decimal('0.00')
        self.servicio.validar_parametros(self.duracion)

    def confirmar(self):
        if self.estado != 'PENDIENTE':
            raise ReservaInvalidaError('Solo se pueden confirmar reservas pendientes.')
        self.servicio.validar_disponibilidad()
        self.estado = 'CONFIRMADA'

    def cancelar(self):
        if self.estado == 'CANCELADA':
            raise ReservaInvalidaError('La reserva ya está cancelada.')
        self.estado = 'CANCELADA'

    def procesar(self, impuesto=0, descuento=0):
        if self.estado != 'CONFIRMADA':
            raise ReservaInvalidaError('Solo se pueden procesar reservas confirmadas.')
        self.servicio.validar_disponibilidad()
        self.total = self.servicio.calcular_total(self.duracion, impuesto, descuento)
        return self.total
