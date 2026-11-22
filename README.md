# Software FJ — UNAD, Programación 213023, Fase 4

Proyecto académico colaborativo de gestión de clientes, servicios y reservas en Python 3.10+ **sin bases de datos**. Utiliza objetos y diccionarios en memoria; solo escribe archivos para logs.

## Requisitos
Python 3.10 o superior. No se necesitan bibliotecas externas.

## Ejecución
Abre una terminal en esta carpeta y escribe:

```bash
python main.py
```

En Windows, si `python` no funciona, prueba `py main.py`.

## Pruebas

```bash
python -m unittest -v
```

## Archivos

- `entidades.py`: clase abstracta Entidad, clase Cliente y encapsulación.
- `servicios.py`: Servicio abstracto, tres servicios derivados, validaciones y costos.
- `reservas.py`: creación, confirmación, cancelación y procesamiento.
- `gestor.py`: registro y búsqueda en memoria; no utiliza base de datos.
- `excepciones.py`: excepciones propias del negocio.
- `main.py`: 18 operaciones correctas e incorrectas con `try/except/else/finally`.
- `test_sistema.py`: pruebas automatizadas.
- `logs/eventos.log`: se crea automáticamente al ejecutar; registra errores y eventos.

## Diseño y consideraciones

- Precios y reglas operativas son ejemplos académicos, no valores oficiales de Software FJ.
- El cálculo de costos soporta llamadas con duración, impuesto y/o descuento mediante **parámetros opcionales** (alternativa a la sobrecarga tradicional; Python no admite sobrecarga por firmas como Java).
- `decimal_positivo` muestra encadenamiento de excepciones (`raise ... from exc`).
- El sistema no almacena información de clientes o reservas de forma persistente. Al cerrarlo, se pierde el estado de memoria.
- Las reservas se manejan por estados PENDIENTE, CONFIRMADA y CANCELADA. No se aplica disponibilidad por calendario porque el anexo no establece horarios ni cupos.