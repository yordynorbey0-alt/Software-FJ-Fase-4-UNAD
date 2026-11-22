"""Servicios especializados mediante herencia y polimorfismo."""
from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation
from entidades import Entidad
from excepciones import DatosInvalidosError, ServicioNoDisponibleError


def decimal_positivo(valor, nombre):
    """Convierte un valor a Decimal, rechazando cero, negativos y NaN."""
    try:
        numero = Decimal(str(valor))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise DatosInvalidosError(f'{nombre} debe ser un número válido.') from exc
    if not numero.is_finite() or numero <= 0:
        raise DatosInvalidosError(f'{nombre} debe ser mayor que cero.')
    return numero


class Servicio(Entidad, ABC):
    """Clase abstracta para los servicios ofrecidos por la empresa."""

    def __init__(self, identificador, nombre, tarifa, disponible=True):
        if not isinstance(identificador, str) or not identificador.strip():
            raise DatosInvalidosError('El código del servicio es obligatorio.')
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError('El nombre del servicio es obligatorio.')
        if not isinstance(disponible, bool):
            raise DatosInvalidosError('Disponibilidad debe ser True o False.')
        self.__identificador = identificador.strip()
        self.nombre = nombre.strip()
        self.tarifa = decimal_positivo(tarifa, 'La tarifa')
        self.disponible = disponible

    @property
    def identificador(self):
        return self.__identificador

    def validar_disponibilidad(self):
        if not self.disponible:
            raise ServicioNoDisponibleError(f'El servicio {self.nombre} no está disponible.')

    @abstractmethod
    def validar_parametros(self, duracion):
        """Comprueba las restricciones específicas del servicio."""

    @abstractmethod
    def calcular_costo(self, duracion):
        """Devuelve el costo base en pesos colombianos."""

    @abstractmethod
    def describir(self):
        """Describe brevemente el servicio."""

    def calcular_total(self, duracion, impuesto=0, descuento=0):
        """Variantes por parámetros opcionales: base, con impuesto o descuento.

        Por ejemplo: calcular_total(2), calcular_total(2, impuesto=19),
        calcular_total(2, impuesto=19, descuento=10).
        """
        costo = self.calcular_costo(duracion)
        try:
            iva = Decimal(str(impuesto))
            rebaja = Decimal(str(descuento))
        except (InvalidOperation, ValueError, TypeError) as exc:
            raise DatosInvalidosError('Impuesto y descuento deben ser numéricos.') from exc
        if (not iva.is_finite() or not rebaja.is_finite() or
                not (0 <= iva <= 100) or not (0 <= rebaja <= 100)):
            raise DatosInvalidosError('Impuesto y descuento deben estar entre 0 y 100.')
        return (costo * (Decimal('1') - rebaja / 100) *
                (Decimal('1') + iva / 100)).quantize(Decimal('0.01'))


class ReservaSala(Servicio):
    """Alquiler de salas: duración de 1 a 12 horas."""

    def validar_parametros(self, duracion):
        horas = decimal_positivo(duracion, 'La duración')
        if horas > 12:
            raise DatosInvalidosError('La sala se reserva por máximo 12 horas.')
        return horas

    def calcular_costo(self, duracion):
        return self.tarifa * self.validar_parametros(duracion)

    def describir(self):
        return f'Sala: {self.nombre}, tarifa por hora ${self.tarifa:,.0f} COP'


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: duración de 1 a 30 días."""

    def validar_parametros(self, duracion):
        dias = decimal_positivo(duracion, 'Los días')
        if dias != dias.to_integral_value() or dias > 30:
            raise DatosInvalidosError('Los equipos se alquilan de 1 a 30 días enteros.')
        return dias

    def calcular_costo(self, duracion):
        return self.tarifa * self.validar_parametros(duracion)

    def describir(self):
        return f'Equipo: {self.nombre}, tarifa por día ${self.tarifa:,.0f} COP'


class AsesoriaEspecializada(Servicio):
    """Asesorías: duración de hasta 8 horas."""

    def validar_parametros(self, duracion):
        horas = decimal_positivo(duracion, 'La duración')
        if horas > 8:
            raise DatosInvalidosError('La asesoría puede durar máximo 8 horas.')
        return horas

    def calcular_costo(self, duracion):
        return self.tarifa * self.validar_parametros(duracion)

    def describir(self):
        return f'Asesoría: {self.nombre}, tarifa por hora ${self.tarifa:,.0f} COP'
