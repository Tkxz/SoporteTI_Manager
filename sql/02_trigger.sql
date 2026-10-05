USE soporte_ti;

DROP TRIGGER IF EXISTS trg_ticket_estado_historial;

DELIMITER $$

CREATE TRIGGER trg_ticket_estado_historial
AFTER UPDATE ON tickets
FOR EACH ROW
BEGIN
    IF OLD.estado <> NEW.estado THEN
        INSERT INTO historial_ticket(
            ticket_id,
            tecnico_id,
            estado_anterior,
            estado_nuevo,
            comentario
        )
        VALUES(
            NEW.id_ticket,
            NEW.tecnico_id,
            OLD.estado,
            NEW.estado,
            CONCAT('Cambio automático de estado: ', OLD.estado, ' -> ', NEW.estado)
        );
    END IF;
END$$

DELIMITER ;
