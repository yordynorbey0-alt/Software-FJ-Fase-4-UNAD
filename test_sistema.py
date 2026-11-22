"""Pruebas automáticas con la biblioteca estándar unittest."""
import unittest
from decimal import Decimal
from entidades import Cliente
from excepciones import DatosInvalidosError, ReservaInvalidaError, ServicioNoDisponibleError
from gestor import GestorSoftwareFJ
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada


class PruebasSoftwareFJ(unittest.TestCase):
    def setUp(self):
        self.gestor = GestorSoftwareFJ()
        self.gestor.registrar_cliente('1', 'Ana Pérez', 'ana@ejemplo.com')
        self.gestor.registrar_servicio(ReservaSala('S1', 'Sala A', 50000))

    def test_cliente_invalido(self):
        with self.assertRaises(DatosInvalidosError):
            Cliente('2', 'A', 'sin-correo')

    def test_costo_sala_con_iva_descuento(self):
        sala = ReservaSala('X', 'Sala X', 50000)
        self.assertEqual(sala.calcular_total(2, impuesto=19, descuento=10), Decimal('107100.00'))

    def test_polimorfismo(self):
        servicios = [ReservaSala('S', 'Sala', 100), AlquilerEquipo('E', 'Equipo', 200),
                     AsesoriaEspecializada('A', 'Asesoría', 300)]
        self.assertEqual([s.calcular_costo(2) for s in servicios],
                         [Decimal(200), Decimal(400), Decimal(600)])

    def test_reserva_confirmada(self):
        r = self.gestor.crear_reserva('R1', '1', 'S1', 2)
        r.confirmar()
        self.assertEqual(r.procesar(), Decimal('100000.00'))

    def test_no_procesar_pendiente(self):
        r = self.gestor.crear_reserva('R1', '1', 'S1', 2)
        with self.assertRaises(ReservaInvalidaError):
            r.procesar()

    def test_cancelacion(self):
        r = self.gestor.crear_reserva('R1', '1', 'S1', 2)
        r.cancelar()
        with self.assertRaises(ReservaInvalidaError):
            r.confirmar()

    def test_servicio_no_disponible(self):
        sala = ReservaSala('X', 'Sala cerrada', 100, disponible=False)
        with self.assertRaises(ServicioNoDisponibleError):
            sala.validar_disponibilidad()

    def test_duracion_incorrecta(self):
        with self.assertRaises(DatosInvalidosError):
            self.gestor.crear_reserva('R1', '1', 'S1', -2)

    def test_numero_no_finito(self):
        with self.assertRaises(DatosInvalidosError):
            ReservaSala('X', 'Sala', 'NaN')

    def test_registro_duplicado(self):
        from excepciones import RegistroDuplicadoError
        with self.assertRaises(RegistroDuplicadoError):
            self.gestor.registrar_cliente('1', 'Ana Pérez', 'ana@ejemplo.com')


if __name__ == '__main__':
    unittest.main()
