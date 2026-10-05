USE soporte_ti;

-- JOIN: muestra información relacionada de tickets, usuarios, técnicos y especialidades
SELECT
    tk.id_ticket,
    tk.titulo,
    tk.estado,
    tk.prioridad,
    u.nombre AS usuario,
    u.departamento,
    COALESCE(t.nombre, 'Sin asignar') AS tecnico,
    e.nombre AS especialidad
FROM tickets tk
INNER JOIN usuarios u ON u.id_usuario = tk.usuario_id
LEFT JOIN tecnicos t ON t.id_tecnico = tk.tecnico_id
INNER JOIN especialidades e ON e.id_especialidad = tk.especialidad_id
ORDER BY tk.fecha_creacion DESC;

-- Agrupación/resumen
SELECT estado, COUNT(*) AS cantidad_tickets
FROM tickets
GROUP BY estado
ORDER BY cantidad_tickets DESC;

-- Resumen por técnico
SELECT
    COALESCE(t.nombre, 'Sin asignar') AS tecnico,
    COUNT(tk.id_ticket) AS total_tickets
FROM tickets tk
LEFT JOIN tecnicos t ON t.id_tecnico = tk.tecnico_id
GROUP BY t.id_tecnico, t.nombre
ORDER BY total_tickets DESC;
