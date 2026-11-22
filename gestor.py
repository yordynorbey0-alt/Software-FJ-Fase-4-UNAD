"""Gestor que mantiene clientes, servicios y reservas en memoria."""
import logging
from entidades import Cliente
from servicios import Servicio
from reservas import Reserva
from excepciones import DatosInvalidosError, RegistroDuplicadoError


class GestorSoftwareFJ:
    """Centraliza las listas internas y todas las operaciones del sistema."""

    def __init__(self):
        self._clientes = {}
        self._servicios = {}
        self._reservas = {}

    def registrar_cliente(self, identificador, nombre, correo):
        if identificador in self._clientes:
            raise RegistroDuplicadoError('Ya existe un cliente con esa identificación.')
        cliente = Cliente(identificador, nombre, correo)
        self._clientes[cliente.identificador] = cliente
        logging.info('Cliente registrado: %s', cliente.identificador)
        return cliente

    def registrar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError('El objeto no corresponde a un servicio.')
        if servicio.identificador in self._servicios:
            raise RegistroDuplicadoError('El código de servicio ya existe.')
        self._servicios[servicio.identificador] = servicio
        logging.info('Servicio registrado: %s', servicio.identificador)
        return servicio

    def crear_reserva(self, codigo, id_cliente, id_servicio, duracion):
        if codigo in self._reservas:
            raise RegistroDuplicadoError('El código de reserva ya existe.')
        if id_cliente not in self._clientes:
            raise DatosInvalidosError('El cliente indicado no está registrado.')
        if id_servicio not in self._servicios:
            raise DatosInvalidosError('El servicio indicado no está registrado.')
        reserva = Reserva(codigo, self._clientes[id_cliente],
                          self._servicios[id_servicio], duracion)
        self._reservas[reserva.codigo] = reserva
        logging.info('Reserva creada: %s', reserva.codigo)
        return reserva

    def obtener_reserva(self, codigo):
        if codigo not in self._reservas:
            raise DatosInvalidosError('No existe una reserva con ese código.')
        return self._reservas[codigo]

    def resumen(self):
        return (f'Clientes: {len(self._clientes)} | Servicios: '
                f'{len(self._servicios)} | Reservas: {len(self._reservas)}')
