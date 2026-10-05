# SoporteTI Manager

Sistema de gestión de tickets de soporte técnico desarrollado con Python, Flet y MySQL.

## Tablas

Todas las tablas terminan en `KL`:

- `usuariosKL`
- `detalle_usuarioKL`
- `tecnicosKL`
- `especialidadesKL`
- `tecnico_especialidadKL`
- `ticketsKL`
- `historial_ticketKL`

## Relaciones

- 1:1: `usuariosKL` -> `detalle_usuarioKL`
- 1:N: `usuariosKL` -> `ticketsKL`
- 1:N: `tecnicosKL` -> `ticketsKL`
- 1:N: `especialidadesKL` -> `ticketsKL`
- N:M: `tecnicosKL` <-> `especialidadesKL`, mediante `tecnico_especialidadKL`
- 1:N: `ticketsKL` -> `historial_ticketKL`

## Trigger

`trg_ticket_estado_historialKL`

Registra automáticamente los cambios de estado de un ticket en `historial_ticketKL`.

## Procedimiento almacenado

`sp_cerrar_ticketKL`

Valida que el ticket exista, que no esté cerrado y que tenga un técnico asignado antes de cerrarlo.

## Ejecutar SQL

Ejecuta en este orden:

1. `sql/01_schema.sql`
2. `sql/02_trigger.sql`
3. `sql/03_procedure.sql`
4. `sql/04_seed.sql`

## Instalar dependencias

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Variables de entorno

Copia `.env.example` a `.env`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=soporte_ti
```

## Ejecutar

```bash
python main.py
```

## Autor

Benjamín Domínguez Arellano
