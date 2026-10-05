CREATE DATABASE IF NOT EXISTS soporte_ti
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE soporte_ti;

CREATE TABLE usuariosKL (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    departamento VARCHAR(100) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE detalle_usuarioKL (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL UNIQUE,
    telefono VARCHAR(30),
    extension VARCHAR(10),
    CONSTRAINT fk_detalle_usuarioKL
        FOREIGN KEY (usuario_id)
        REFERENCES usuariosKL(id_usuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE tecnicosKL (
    id_tecnico INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    nivel ENUM('Junior','Semi Senior','Senior')
        NOT NULL DEFAULT 'Junior',
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE especialidadesKL (
    id_especialidad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion VARCHAR(255)
);

CREATE TABLE tecnico_especialidadKL (
    tecnico_id INT NOT NULL,
    especialidad_id INT NOT NULL,
    fecha_asignacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (tecnico_id, especialidad_id),

    CONSTRAINT fk_tecnico_especialidad_tecnicoKL
        FOREIGN KEY (tecnico_id)
        REFERENCES tecnicosKL(id_tecnico)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_tecnico_especialidad_especialidadKL
        FOREIGN KEY (especialidad_id)
        REFERENCES especialidadesKL(id_especialidad)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE ticketsKL (
    id_ticket INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(180) NOT NULL,
    descripcion TEXT NOT NULL,
    prioridad ENUM('Baja','Media','Alta','Crítica')
        NOT NULL DEFAULT 'Media',
    estado ENUM('Abierto','En proceso','Resuelto','Cerrado')
        NOT NULL DEFAULT 'Abierto',
    usuario_id INT NOT NULL,
    tecnico_id INT NULL,
    especialidad_id INT NOT NULL,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    fecha_cierre DATETIME NULL,

    CONSTRAINT fk_ticket_usuarioKL
        FOREIGN KEY (usuario_id)
        REFERENCES usuariosKL(id_usuario)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,

    CONSTRAINT fk_ticket_tecnicoKL
        FOREIGN KEY (tecnico_id)
        REFERENCES tecnicosKL(id_tecnico)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    CONSTRAINT fk_ticket_especialidadKL
        FOREIGN KEY (especialidad_id)
        REFERENCES especialidadesKL(id_especialidad)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE historial_ticketKL (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id INT NOT NULL,
    tecnico_id INT NULL,
    estado_anterior VARCHAR(30),
    estado_nuevo VARCHAR(30) NOT NULL,
    comentario VARCHAR(500),
    fecha_cambio TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_historial_ticketKL
        FOREIGN KEY (ticket_id)
        REFERENCES ticketsKL(id_ticket)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_historial_tecnicoKL
        FOREIGN KEY (tecnico_id)
        REFERENCES tecnicosKL(id_tecnico)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
