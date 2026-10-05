USE soporte_ti;

INSERT INTO usuarios(nombre,email,departamento) VALUES
('Ana Pérez','ana@empresa.cl','Administración'),
('Carlos Soto','carlos@empresa.cl','Ventas'),
('María López','maria@empresa.cl','Finanzas');

INSERT INTO detalle_usuario(usuario_id,telefono,extension) VALUES
(1,'+56 9 1111 1111','101'),
(2,'+56 9 2222 2222','102'),
(3,'+56 9 3333 3333','103');

INSERT INTO tecnicos(nombre,email,nivel) VALUES
('Diego Rojas','diego.soporte@empresa.cl','Senior'),
('Laura Díaz','laura.soporte@empresa.cl','Junior');

INSERT INTO especialidades(nombre,descripcion) VALUES
('Hardware','Problemas de equipos y periféricos'),
('Software','Errores de aplicaciones y sistemas'),
('Redes','Conectividad, Wi-Fi, LAN e Internet');

INSERT INTO tecnico_especialidad(tecnico_id,especialidad_id) VALUES
(1,1),(1,3),(2,2);

INSERT INTO tickets(titulo,descripcion,prioridad,usuario_id,tecnico_id,especialidad_id)
VALUES
('PC no enciende','El computador del área de ventas no inicia.','Alta',2,1,1),
('Error al abrir sistema contable','La aplicación muestra un error al iniciar.','Media',3,2,2),
('Sin conexión a Internet','El equipo pierde conexión de forma intermitente.','Crítica',1,1,3);
