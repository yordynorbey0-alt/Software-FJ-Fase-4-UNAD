"""Entidades base y cliente con encapsulación de sus datos."""
from abc import ABC, abstractmethod
from excepciones import DatosInvalidosError


class Entidad(ABC):
    """Contrato común para entidades identificables."""

    @property
    @abstractmethod
    def identificador(self):
        """Identificador único de la entidad."""


class Cliente(Entidad):
    """Almacena datos de un cliente y valida sus atributos."""

    def __init__(self, identificador, nombre, correo):
        if not isinstance(identificador, str) or not identificador.strip():
            raise DatosInvalidosError('La identificación del cliente es obligatoria.')
        self.__identificador = identificador.strip()
        self.nombre = nombre
        self.correo = correo

    @property
    def identificador(self):
        return self.__identificador

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatosInvalidosError('El nombre debe tener al menos 3 caracteres.')
        self.__nombre = valor.strip()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if (not isinstance(valor, str) or valor.count('@') != 1 or
                '.' not in valor.split('@')[-1] or ' ' in valor or
                not valor.split('@')[0]):
            raise DatosInvalidosError('El correo electrónico no es válido.')
        self.__correo = valor.strip()

    def __str__(self):
        return f'{self.nombre} ({self.identificador})'
