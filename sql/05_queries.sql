USE soporte_ti;

-- JOIN
SELECT
    tk.id_ticket,
    tk.titulo,
    tk.estado,
    tk.prioridad,
    u.nombre AS usuario,
    u.departamento,
    COALESCE(t.nombre, 'Sin asignar') AS tecnico,
    e.nombre AS especialidad
FROM ticketsKL tk
INNER JOIN usuariosKL u
    ON u.id_usuario = tk.usuario_id
LEFT JOIN tecnicosKL t
    ON t.id_tecnico = tk.tecnico_id
INNER JOIN especialidadesKL e
    ON e.id_especialidad = tk.especialidad_id
ORDER BY tk.fecha_creacion DESC;

-- GROUP BY
SELECT
    estado,
    COUNT(*) AS cantidad_tickets
FROM ticketsKL
GROUP BY estado
ORDER BY cantidad_tickets DESC;

-- Tickets por técnico
SELECT
    COALESCE(t.nombre, 'Sin asignar') AS tecnico,
    COUNT(tk.id_ticket) AS total_tickets
FROM ticketsKL tk
LEFT JOIN tecnicosKL t
    ON t.id_tecnico = tk.tecnico_id
GROUP BY t.id_tecnico, t.nombre
ORDER BY total_tickets DESC;
