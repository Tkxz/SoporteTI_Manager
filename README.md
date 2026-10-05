# SoporteTI Manager

Sistema de gestión de tickets de soporte técnico desarrollado con **Python, Flet y MySQL**.

## Descripción

SoporteTI Manager permite registrar y administrar solicitudes de soporte técnico dentro de una organización. El sistema relaciona usuarios, técnicos, especialidades y tickets, permitiendo asignar responsables y consultar el estado de cada solicitud.

## Problema que busca resolver

En una organización, las solicitudes de soporte pueden perderse si se gestionan por mensajes, llamadas o anotaciones. Este sistema centraliza las solicitudes, permite saber quién reportó el problema, qué técnico está asignado, cuál es la especialidad necesaria y en qué estado se encuentra cada ticket.

## Funciones principales

- Registrar, consultar, modificar y eliminar usuarios.
- Registrar técnicos y especialidades.
- Asignar varias especialidades a un técnico.
- Crear, editar, eliminar y filtrar tickets.
- Visualizar datos relacionados mediante JOIN.
- Filtrar tickets por texto y estado.
- Mostrar resumen de tickets por estado.
- Cerrar tickets mediante un procedimiento almacenado.
- Registrar automáticamente cambios de estado mediante trigger.
- Manejo de errores y mensajes de éxito o advertencia.

## Tecnologías utilizadas

- Python 3
- Flet
- MySQL
- mysql-connector-python
- python-dotenv
- Git y GitHub

## Modelo de datos

El sistema incluye las siguientes tablas:

1. `usuarios`
2. `detalle_usuario`
3. `tecnicos`
4. `especialidades`
5. `tecnico_especialidad`
6. `tickets`
7. `historial_ticket`

### Relaciones

- **1:1:** `usuarios` → `detalle_usuario`
- **1:N:** `usuarios` → `tickets`
- **1:N:** `tecnicos` → `tickets`
- **1:N:** `especialidades` → `tickets`
- **N:M:** `tecnicos` ↔ `especialidades`, resuelta por `tecnico_especialidad`
- **1:N:** `tickets` → `historial_ticket`

## Trigger

`trg_ticket_estado_historial`

Su función es registrar automáticamente en `historial_ticket` cada cambio de estado realizado sobre un ticket. Esto permite mantener trazabilidad real de la solicitud.

## Procedimiento almacenado

`sp_cerrar_ticket`

Su función es cerrar un ticket de forma controlada. Valida que:

- el ticket exista;
- el ticket todavía no esté cerrado;
- exista un técnico asignado.

Luego establece el estado como `Cerrado`, guarda la fecha de cierre y registra el cambio en el historial.

## Instalación

### 1. Clonar el repositorio

```bash
git clone URL_DE_TU_REPOSITORIO
cd SoporteTI_Manager
```

### 2. Crear entorno virtual

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Crear la base de datos

Ejecutar los archivos SQL en este orden:

```text
sql/01_schema.sql
sql/02_trigger.sql
sql/03_procedure.sql
sql/04_seed.sql
```

El archivo `sql/05_queries.sql` contiene consultas JOIN y de agrupación solicitadas en la actividad.

### 5. Configurar variables de entorno

Copiar:

```text
.env.example
```

como:

```text
.env
```

y completar las credenciales reales de MySQL.

Ejemplo:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=soporte_ti
```

### 6. Ejecutar la aplicación

```bash
python main.py
```

## Captura de la aplicación

Agregar una captura dentro de:

```text
screenshots/app.png
```

Luego se puede mostrar aquí con:

```md
![Aplicación funcionando](screenshots/app.png)
```

## Autor

**Benjamín Domínguez Arellano**
