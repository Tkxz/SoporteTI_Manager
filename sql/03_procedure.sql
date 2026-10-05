USE soporte_ti;

DROP PROCEDURE IF EXISTS sp_cerrar_ticketKL;

DELIMITER $$

CREATE PROCEDURE sp_cerrar_ticketKL(
    IN p_ticket_id INT,
    IN p_comentario VARCHAR(500)
)
BEGIN
    DECLARE v_estado VARCHAR(30);
    DECLARE v_tecnico INT;
    DECLARE v_existe INT DEFAULT 0;

    SELECT COUNT(*)
    INTO v_existe
    FROM ticketsKL
    WHERE id_ticket = p_ticket_id;

    IF v_existe = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El ticket no existe.';
    ELSE
        SELECT estado, tecnico_id
        INTO v_estado, v_tecnico
        FROM ticketsKL
        WHERE id_ticket = p_ticket_id;

        IF v_estado = 'Cerrado' THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'El ticket ya está cerrado.';
        ELSEIF v_tecnico IS NULL THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'No se puede cerrar un ticket sin técnico asignado.';
        ELSE
            UPDATE ticketsKL
            SET estado = 'Cerrado',
                fecha_cierre = NOW()
            WHERE id_ticket = p_ticket_id;

            INSERT INTO historial_ticketKL(
                ticket_id,
                tecnico_id,
                estado_anterior,
                estado_nuevo,
                comentario
            )
            VALUES(
                p_ticket_id,
                v_tecnico,
                v_estado,
                'Cerrado',
                COALESCE(
                    NULLIF(p_comentario, ''),
                    'Ticket cerrado mediante procedimiento almacenado.'
                )
            );
        END IF;
    END IF;
END$$

DELIMITER ;
