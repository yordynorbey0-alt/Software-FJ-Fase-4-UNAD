"""Excepciones específicas del sistema Software FJ."""


class ErrorSoftwareFJ(Exception):
    """Excepción base de los errores de negocio."""


class DatosInvalidosError(ErrorSoftwareFJ):
    """Datos faltantes, mal formados o inconsistentes."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio solicitado no está disponible."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """La operación solicitada para la reserva no está permitida."""


class RegistroDuplicadoError(ErrorSoftwareFJ):
    """Un identificador ya está registrado."""
