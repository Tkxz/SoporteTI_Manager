USE soporte_ti;

DROP PROCEDURE IF EXISTS sp_cerrar_ticket;

DELIMITER $$

CREATE PROCEDURE sp_cerrar_ticket(
    IN p_ticket_id INT,
    IN p_comentario VARCHAR(500)
)
BEGIN
    DECLARE v_estado VARCHAR(30);
    DECLARE v_tecnico INT;

    SELECT estado, tecnico_id
    INTO v_estado, v_tecnico
    FROM tickets
    WHERE id_ticket = p_ticket_id;

    IF v_estado IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El ticket no existe.';
    ELSEIF v_estado = 'Cerrado' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El ticket ya está cerrado.';
    ELSEIF v_tecnico IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se puede cerrar un ticket sin técnico asignado.';
    ELSE
        UPDATE tickets
        SET estado = 'Cerrado',
            fecha_cierre = NOW()
        WHERE id_ticket = p_ticket_id;

        UPDATE historial_ticket
        SET comentario = COALESCE(NULLIF(p_comentario, ''), 'Ticket cerrado mediante procedimiento almacenado.')
        WHERE id_historial = (
            SELECT id_historial FROM (
                SELECT MAX(id_historial) AS id_historial
                FROM historial_ticket
                WHERE ticket_id = p_ticket_id
                  AND estado_nuevo = 'Cerrado'
            ) AS ultimo
        );
    END IF;
END$$

DELIMITER ;
