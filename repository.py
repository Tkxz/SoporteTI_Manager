from mysql.connector import Error
from database import get_connection

class SoporteRepository:
    def _execute(self, query, params=None, fetchone=False, fetchall=False, commit=False):
        with get_connection() as conn:
            cur = conn.cursor(dictionary=True)
            cur.execute(query, params or ())
            result = None
            if fetchone:
                result = cur.fetchone()
            elif fetchall:
                result = cur.fetchall()
            if commit:
                conn.commit()
            cur.close()
            return result

    # ---------------- USUARIOS ----------------
    def listar_usuarios(self, filtro=""):
        q = """
            SELECT u.id_usuario, u.nombre, u.email, u.departamento, u.activo,
                   d.telefono, d.extension
            FROM usuarios u
            LEFT JOIN detalle_usuario d ON d.usuario_id = u.id_usuario
            WHERE u.nombre LIKE %s OR u.email LIKE %s OR u.departamento LIKE %s
            ORDER BY u.id_usuario DESC
        """
        f = f"%{filtro}%"
        return self._execute(q, (f, f, f), fetchall=True)

    def crear_usuario(self, nombre, email, departamento, telefono, extension):
        with get_connection() as conn:
            cur = conn.cursor()
            try:
                cur.execute(
                    "INSERT INTO usuarios(nombre,email,departamento) VALUES(%s,%s,%s)",
                    (nombre, email, departamento),
                )
                uid = cur.lastrowid
                cur.execute(
                    "INSERT INTO detalle_usuario(usuario_id,telefono,extension) VALUES(%s,%s,%s)",
                    (uid, telefono or None, extension or None),
                )
                conn.commit()
            except:
                conn.rollback()
                raise
            finally:
                cur.close()

    def actualizar_usuario(self, uid, nombre, email, departamento, telefono, extension):
        with get_connection() as conn:
            cur = conn.cursor()
            try:
                cur.execute(
                    """UPDATE usuarios
                       SET nombre=%s,email=%s,departamento=%s
                       WHERE id_usuario=%s""",
                    (nombre, email, departamento, uid),
                )
                cur.execute(
                    """INSERT INTO detalle_usuario(usuario_id,telefono,extension)
                       VALUES(%s,%s,%s)
                       ON DUPLICATE KEY UPDATE telefono=VALUES(telefono), extension=VALUES(extension)""",
                    (uid, telefono or None, extension or None),
                )
                conn.commit()
            except:
                conn.rollback()
                raise
            finally:
                cur.close()

    def eliminar_usuario(self, uid):
        self._execute("DELETE FROM usuarios WHERE id_usuario=%s", (uid,), commit=True)

    # ---------------- TÉCNICOS ----------------
    def listar_tecnicos(self):
        return self._execute(
            """SELECT id_tecnico,nombre,email,nivel,activo
               FROM tecnicos ORDER BY nombre""",
            fetchall=True,
        )

    def crear_tecnico(self, nombre, email, nivel):
        self._execute(
            "INSERT INTO tecnicos(nombre,email,nivel) VALUES(%s,%s,%s)",
            (nombre, email, nivel),
            commit=True,
        )

    def actualizar_tecnico(self, tid, nombre, email, nivel):
        self._execute(
            "UPDATE tecnicos SET nombre=%s,email=%s,nivel=%s WHERE id_tecnico=%s",
            (nombre, email, nivel, tid),
            commit=True,
        )

    def eliminar_tecnico(self, tid):
        self._execute("DELETE FROM tecnicos WHERE id_tecnico=%s", (tid,), commit=True)

    # ---------------- ESPECIALIDADES ----------------
    def listar_especialidades(self):
        return self._execute(
            "SELECT id_especialidad,nombre,descripcion FROM especialidades ORDER BY nombre",
            fetchall=True,
        )

    def crear_especialidad(self, nombre, descripcion):
        self._execute(
            "INSERT INTO especialidades(nombre,descripcion) VALUES(%s,%s)",
            (nombre, descripcion),
            commit=True,
        )

    def asignar_especialidad(self, tecnico_id, especialidad_id):
        self._execute(
            """INSERT IGNORE INTO tecnico_especialidad(tecnico_id,especialidad_id)
               VALUES(%s,%s)""",
            (tecnico_id, especialidad_id),
            commit=True,
        )

    def quitar_especialidad(self, tecnico_id, especialidad_id):
        self._execute(
            """DELETE FROM tecnico_especialidad
               WHERE tecnico_id=%s AND especialidad_id=%s""",
            (tecnico_id, especialidad_id),
            commit=True,
        )

    def listar_tecnico_especialidades(self):
        return self._execute(
            """SELECT te.tecnico_id, t.nombre AS tecnico,
                      te.especialidad_id, e.nombre AS especialidad
               FROM tecnico_especialidad te
               INNER JOIN tecnicos t ON t.id_tecnico=te.tecnico_id
               INNER JOIN especialidades e ON e.id_especialidad=te.especialidad_id
               ORDER BY t.nombre,e.nombre""",
            fetchall=True,
        )

    # ---------------- TICKETS ----------------
    def listar_tickets(self, filtro="", estado="Todos"):
        q = """
            SELECT tk.id_ticket, tk.titulo, tk.descripcion, tk.prioridad, tk.estado,
                   tk.fecha_creacion, tk.fecha_cierre,
                   u.nombre AS usuario, u.departamento,
                   COALESCE(t.nombre,'Sin asignar') AS tecnico,
                   e.nombre AS especialidad
            FROM tickets tk
            INNER JOIN usuarios u ON u.id_usuario=tk.usuario_id
            LEFT JOIN tecnicos t ON t.id_tecnico=tk.tecnico_id
            INNER JOIN especialidades e ON e.id_especialidad=tk.especialidad_id
            WHERE (tk.titulo LIKE %s OR tk.descripcion LIKE %s OR u.nombre LIKE %s)
        """
        params = [f"%{filtro}%", f"%{filtro}%", f"%{filtro}%"]
        if estado != "Todos":
            q += " AND tk.estado=%s"
            params.append(estado)
        q += " ORDER BY tk.fecha_creacion DESC"
        return self._execute(q, tuple(params), fetchall=True)

    def crear_ticket(self, titulo, descripcion, prioridad, usuario_id, tecnico_id, especialidad_id):
        self._execute(
            """INSERT INTO tickets(titulo,descripcion,prioridad,usuario_id,tecnico_id,especialidad_id)
               VALUES(%s,%s,%s,%s,%s,%s)""",
            (titulo, descripcion, prioridad, usuario_id, tecnico_id or None, especialidad_id),
            commit=True,
        )

    def actualizar_ticket(self, ticket_id, titulo, descripcion, prioridad, estado, tecnico_id, especialidad_id):
        self._execute(
            """UPDATE tickets
               SET titulo=%s,descripcion=%s,prioridad=%s,estado=%s,
                   tecnico_id=%s,especialidad_id=%s
               WHERE id_ticket=%s""",
            (titulo, descripcion, prioridad, estado, tecnico_id or None, especialidad_id, ticket_id),
            commit=True,
        )

    def eliminar_ticket(self, ticket_id):
        self._execute("DELETE FROM tickets WHERE id_ticket=%s", (ticket_id,), commit=True)

    def cerrar_ticket_sp(self, ticket_id, comentario):
        with get_connection() as conn:
            cur = conn.cursor()
            try:
                cur.callproc("sp_cerrar_ticket", (ticket_id, comentario))
                conn.commit()
            except:
                conn.rollback()
                raise
            finally:
                cur.close()

    # ---------------- HISTORIAL / RESUMEN ----------------
    def historial_ticket(self, ticket_id):
        return self._execute(
            """SELECT h.id_historial,h.estado_anterior,h.estado_nuevo,h.comentario,h.fecha_cambio,
                      COALESCE(t.nombre,'Sistema/usuario') tecnico
               FROM historial_ticket h
               LEFT JOIN tecnicos t ON t.id_tecnico=h.tecnico_id
               WHERE h.ticket_id=%s ORDER BY h.fecha_cambio DESC""",
            (ticket_id,),
            fetchall=True,
        )

    def resumen(self):
        return self._execute(
            """SELECT estado, COUNT(*) AS total
               FROM tickets
               GROUP BY estado
               ORDER BY total DESC""",
            fetchall=True,
        )
