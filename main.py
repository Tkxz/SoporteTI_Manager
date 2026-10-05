import flet as ft
from mysql.connector import Error
from Sistema import SoporteRepository

repo = SoporteRepository()

def main(page: ft.Page):
    page.title = "SoporteTI Manager"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.window_width = 1250
    page.window_height = 800

    def snackbar(msg, error=False):
        page.snack_bar = ft.SnackBar(
            ft.Text(msg),
            bgcolor=ft.Colors.RED_700 if error else ft.Colors.GREEN_700,
        )
        page.snack_bar.open = True
        page.update()

    def confirm_delete(texto, action):
        def cerrar(e):
            dialog.open = False
            page.update()

        def aceptar(e):
            dialog.open = False
            page.update()
            action()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(texto),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar),
                ft.ElevatedButton("Eliminar", on_click=aceptar),
            ],
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    title = ft.Text("SoporteTI Manager", size=30, weight=ft.FontWeight.BOLD)
    subtitle = ft.Text("Gestión de solicitudes de soporte técnico")

    content = ft.Container(expand=True)

    # ---------------- DASHBOARD ----------------
    def dashboard_view():
        try:
            data = repo.resumen()
            cards = []
            for item in data:
                cards.append(
                    ft.Card(
                        ft.Container(
                            ft.Column([
                                ft.Text(item["estado"], size=16),
                                ft.Text(str(item["total"]), size=30, weight=ft.FontWeight.BOLD),
                            ]),
                            padding=20,
                            width=200,
                        )
                    )
                )
            if not cards:
                cards = [ft.Text("Aún no hay tickets registrados.")]
            content.content = ft.Column([
                ft.Text("Resumen de tickets", size=24, weight=ft.FontWeight.BOLD),
                ft.Row(cards, wrap=True),
                ft.Text(
                    "El resumen utiliza una consulta GROUP BY sobre la tabla tickets.",
                    italic=True,
                ),
            ])
        except Exception as ex:
            content.content = ft.Text(f"Error al cargar el resumen: {ex}")
        page.update()

    # ---------------- USUARIOS ----------------
    def usuarios_view():
        nombre = ft.TextField(label="Nombre", width=240)
        email = ft.TextField(label="Correo", width=240)
        dep = ft.TextField(label="Departamento", width=220)
        tel = ft.TextField(label="Teléfono", width=180)
        ext = ft.TextField(label="Extensión", width=120)
        buscar = ft.TextField(label="Buscar", prefix_icon=ft.Icons.SEARCH, width=320)
        tabla = ft.DataTable(columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Correo")),
            ft.DataColumn(ft.Text("Departamento")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Acciones")),
        ])
        editing = {"id": None}

        def limpiar():
            editing["id"] = None
            for c in [nombre,email,dep,tel,ext]:
                c.value = ""

        def cargar(f=""):
            try:
                rows = repo.listar_usuarios(f)
                tabla.rows = []
                for r in rows:
                    def edit_factory(row):
                        def editar(e):
                            editing["id"] = row["id_usuario"]
                            nombre.value = row["nombre"]
                            email.value = row["email"]
                            dep.value = row["departamento"]
                            tel.value = row["telefono"] or ""
                            ext.value = row["extension"] or ""
                            page.update()
                        return editar

                    def delete_factory(uid):
                        return lambda e: confirm_delete(
                            "¿Eliminar este usuario? También se eliminarán sus datos dependientes.",
                            lambda: eliminar(uid),
                        )

                    tabla.rows.append(ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(r["id_usuario"]))),
                        ft.DataCell(ft.Text(r["nombre"])),
                        ft.DataCell(ft.Text(r["email"])),
                        ft.DataCell(ft.Text(r["departamento"])),
                        ft.DataCell(ft.Text(r["telefono"] or "-")),
                        ft.DataCell(ft.Row([
                            ft.IconButton(ft.Icons.EDIT, on_click=edit_factory(r)),
                            ft.IconButton(ft.Icons.DELETE, on_click=delete_factory(r["id_usuario"])),
                        ])),
                    ]))
                page.update()
            except Exception as ex:
                snackbar(f"Error al consultar usuarios: {ex}", True)

        def eliminar(uid):
            try:
                repo.eliminar_usuario(uid)
                snackbar("Usuario eliminado.")
                cargar(buscar.value or "")
            except Exception as ex:
                snackbar(f"No se pudo eliminar: {ex}", True)

        def guardar(e):
            if not nombre.value or not email.value or not dep.value:
                snackbar("Nombre, correo y departamento son obligatorios.", True)
                return
            try:
                if editing["id"]:
                    repo.actualizar_usuario(editing["id"], nombre.value, email.value, dep.value, tel.value, ext.value)
                    snackbar("Usuario actualizado.")
                else:
                    repo.crear_usuario(nombre.value, email.value, dep.value, tel.value, ext.value)
                    snackbar("Usuario registrado.")
                limpiar()
                cargar()
                page.update()
            except Exception as ex:
                snackbar(f"Error al guardar usuario: {ex}", True)

        buscar.on_change = lambda e: cargar(buscar.value or "")
        content.content = ft.Column([
            ft.Text("Usuarios", size=24, weight=ft.FontWeight.BOLD),
            ft.Row([nombre,email,dep], wrap=True),
            ft.Row([tel,ext,ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=guardar)], wrap=True),
            buscar,
            ft.Container(ft.Column([tabla], scroll=ft.ScrollMode.AUTO), expand=True),
        ], expand=True)
        cargar()

    # ---------------- TÉCNICOS / ESPECIALIDADES ----------------
    def tecnicos_view():
        t_nombre = ft.TextField(label="Nombre técnico", width=220)
        t_email = ft.TextField(label="Correo", width=240)
        t_nivel = ft.Dropdown(label="Nivel", width=160, value="Junior", options=[
            ft.dropdown.Option("Junior"), ft.dropdown.Option("Semi Senior"), ft.dropdown.Option("Senior")
        ])
        e_nombre = ft.TextField(label="Especialidad", width=220)
        e_desc = ft.TextField(label="Descripción", width=300)
        tec_dd = ft.Dropdown(label="Técnico", width=250)
        esp_dd = ft.Dropdown(label="Especialidad", width=250)
        tabla = ft.DataTable(columns=[
            ft.DataColumn(ft.Text("Técnico")),
            ft.DataColumn(ft.Text("Especialidad")),
            ft.DataColumn(ft.Text("Acción")),
        ])

        def refrescar():
            try:
                tecs = repo.listar_tecnicos()
                esps = repo.listar_especialidades()
                tec_dd.options = [ft.dropdown.Option(str(x["id_tecnico"]), x["nombre"]) for x in tecs]
                esp_dd.options = [ft.dropdown.Option(str(x["id_especialidad"]), x["nombre"]) for x in esps]
                tabla.rows = []
                for x in repo.listar_tecnico_especialidades():
                    tabla.rows.append(ft.DataRow(cells=[
                        ft.DataCell(ft.Text(x["tecnico"])),
                        ft.DataCell(ft.Text(x["especialidad"])),
                        ft.DataCell(ft.IconButton(
                            ft.Icons.DELETE,
                            on_click=lambda e, t=x["tecnico_id"], s=x["especialidad_id"]: quitar(t,s)
                        )),
                    ]))
                page.update()
            except Exception as ex:
                snackbar(f"Error al cargar técnicos/especialidades: {ex}", True)

        def crear_tec(e):
            if not t_nombre.value or not t_email.value:
                snackbar("Nombre y correo del técnico son obligatorios.", True)
                return
            try:
                repo.crear_tecnico(t_nombre.value, t_email.value, t_nivel.value)
                t_nombre.value = t_email.value = ""
                snackbar("Técnico registrado.")
                refrescar()
            except Exception as ex:
                snackbar(f"Error: {ex}", True)

        def crear_esp(e):
            if not e_nombre.value:
                snackbar("El nombre de la especialidad es obligatorio.", True)
                return
            try:
                repo.crear_especialidad(e_nombre.value, e_desc.value)
                e_nombre.value = e_desc.value = ""
                snackbar("Especialidad registrada.")
                refrescar()
            except Exception as ex:
                snackbar(f"Error: {ex}", True)

        def asignar(e):
            if not tec_dd.value or not esp_dd.value:
                snackbar("Selecciona técnico y especialidad.", True)
                return
            try:
                repo.asignar_especialidad(int(tec_dd.value), int(esp_dd.value))
                snackbar("Especialidad asignada al técnico.")
                refrescar()
            except Exception as ex:
                snackbar(f"Error: {ex}", True)

        def quitar(tid, eid):
            try:
                repo.quitar_especialidad(tid, eid)
                snackbar("Asignación eliminada.")
                refrescar()
            except Exception as ex:
                snackbar(f"Error: {ex}", True)

        content.content = ft.Column([
            ft.Text("Técnicos y especialidades", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Registrar técnico", weight=ft.FontWeight.BOLD),
            ft.Row([t_nombre,t_email,t_nivel,ft.ElevatedButton("Agregar", on_click=crear_tec)], wrap=True),
            ft.Divider(),
            ft.Text("Registrar especialidad", weight=ft.FontWeight.BOLD),
            ft.Row([e_nombre,e_desc,ft.ElevatedButton("Agregar", on_click=crear_esp)], wrap=True),
            ft.Divider(),
            ft.Text("Relación N:M técnico ↔ especialidad", weight=ft.FontWeight.BOLD),
            ft.Row([tec_dd,esp_dd,ft.ElevatedButton("Asignar", on_click=asignar)], wrap=True),
            ft.Container(ft.Column([tabla], scroll=ft.ScrollMode.AUTO), expand=True),
        ], expand=True)
        refrescar()

    # ---------------- TICKETS ----------------
    def tickets_view():
        titulo = ft.TextField(label="Título", width=300)
        descripcion = ft.TextField(label="Descripción", width=420, multiline=True, min_lines=2, max_lines=3)
        prioridad = ft.Dropdown(label="Prioridad", width=150, value="Media", options=[
            ft.dropdown.Option("Baja"), ft.dropdown.Option("Media"), ft.dropdown.Option("Alta"), ft.dropdown.Option("Crítica")
        ])
        estado = ft.Dropdown(label="Estado", width=160, value="Abierto", options=[
            ft.dropdown.Option("Abierto"), ft.dropdown.Option("En proceso"),
            ft.dropdown.Option("Resuelto"), ft.dropdown.Option("Cerrado")
        ])
        usuario = ft.Dropdown(label="Usuario", width=250)
        tecnico = ft.Dropdown(label="Técnico", width=250)
        especialidad = ft.Dropdown(label="Especialidad", width=250)
        buscar = ft.TextField(label="Buscar ticket/usuario", prefix_icon=ft.Icons.SEARCH, width=300)
        filtro_estado = ft.Dropdown(label="Estado", width=180, value="Todos", options=[
            ft.dropdown.Option("Todos"), ft.dropdown.Option("Abierto"), ft.dropdown.Option("En proceso"),
            ft.dropdown.Option("Resuelto"), ft.dropdown.Option("Cerrado")
        ])
        tabla = ft.DataTable(columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Título")),
            ft.DataColumn(ft.Text("Usuario")),
            ft.DataColumn(ft.Text("Técnico")),
            ft.DataColumn(ft.Text("Especialidad")),
            ft.DataColumn(ft.Text("Prioridad")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Acciones")),
        ])
        editing = {"id": None, "usuario_id": None}

        def cargar_combos():
            usuarios = repo.listar_usuarios()
            tecnicos = repo.listar_tecnicos()
            especialidades = repo.listar_especialidades()
            usuario.options = [ft.dropdown.Option(str(x["id_usuario"]), x["nombre"]) for x in usuarios]
            tecnico.options = [ft.dropdown.Option("", "Sin asignar")] + [
                ft.dropdown.Option(str(x["id_tecnico"]), x["nombre"]) for x in tecnicos
            ]
            especialidad.options = [
                ft.dropdown.Option(str(x["id_especialidad"]), x["nombre"]) for x in especialidades
            ]

        def limpiar():
            editing["id"] = None
            editing["usuario_id"] = None
            titulo.value = ""
            descripcion.value = ""
            prioridad.value = "Media"
            estado.value = "Abierto"
            usuario.value = None
            tecnico.value = ""
            especialidad.value = None
            usuario.disabled = False

        def cargar():
            try:
                rows = repo.listar_tickets(buscar.value or "", filtro_estado.value or "Todos")
                tabla.rows = []
                for r in rows:
                    def edit_factory(row):
                        def editar(e):
                            editing["id"] = row["id_ticket"]
                            titulo.value = row["titulo"]
                            descripcion.value = row["descripcion"]
                            prioridad.value = row["prioridad"]
                            estado.value = row["estado"]
                            tecnico.value = next(
                                (o.key for o in tecnico.options if o.text == row["tecnico"]), ""
                            )
                            especialidad.value = next(
                                (o.key for o in especialidad.options if o.text == row["especialidad"]), None
                            )
                            usuario.value = next(
                                (o.key for o in usuario.options if o.text == row["usuario"]), None
                            )
                            usuario.disabled = True
                            page.update()
                        return editar

                    def delete_factory(tid):
                        return lambda e: confirm_delete(
                            "¿Eliminar este ticket y su historial?",
                            lambda: eliminar(tid)
                        )

                    tabla.rows.append(ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(r["id_ticket"]))),
                        ft.DataCell(ft.Text(r["titulo"])),
                        ft.DataCell(ft.Text(r["usuario"])),
                        ft.DataCell(ft.Text(r["tecnico"])),
                        ft.DataCell(ft.Text(r["especialidad"])),
                        ft.DataCell(ft.Text(r["prioridad"])),
                        ft.DataCell(ft.Text(r["estado"])),
                        ft.DataCell(ft.Row([
                            ft.IconButton(ft.Icons.EDIT, on_click=edit_factory(r)),
                            ft.IconButton(ft.Icons.CHECK_CIRCLE, tooltip="Cerrar con procedimiento almacenado",
                                          on_click=lambda e, tid=r["id_ticket"]: cerrar_sp(tid)),
                            ft.IconButton(ft.Icons.DELETE, on_click=delete_factory(r["id_ticket"])),
                        ])),
                    ]))
                page.update()
            except Exception as ex:
                snackbar(f"Error al consultar tickets: {ex}", True)

        def guardar(e):
            if not titulo.value or not descripcion.value or not especialidad.value:
                snackbar("Título, descripción y especialidad son obligatorios.", True)
                return
            try:
                tid = int(tecnico.value) if tecnico.value else None
                eid = int(especialidad.value)
                if editing["id"]:
                    repo.actualizar_ticket(
                        editing["id"], titulo.value, descripcion.value, prioridad.value,
                        estado.value, tid, eid
                    )
                    snackbar("Ticket actualizado.")
                else:
                    if not usuario.value:
                        snackbar("Selecciona un usuario.", True)
                        return
                    repo.crear_ticket(
                        titulo.value, descripcion.value, prioridad.value,
                        int(usuario.value), tid, eid
                    )
                    snackbar("Ticket registrado.")
                limpiar()
                cargar()
                page.update()
            except Exception as ex:
                snackbar(f"Error al guardar ticket: {ex}", True)

        def eliminar(tid):
            try:
                repo.eliminar_ticket(tid)
                snackbar("Ticket eliminado.")
                cargar()
            except Exception as ex:
                snackbar(f"No se pudo eliminar: {ex}", True)

        def cerrar_sp(tid):
            try:
                repo.cerrar_ticket_sp(tid, "Cierre ejecutado desde la aplicación Flet.")
                snackbar("Ticket cerrado mediante procedimiento almacenado.")
                cargar()
            except Exception as ex:
                snackbar(f"No se pudo cerrar el ticket: {ex}", True)

        buscar.on_change = lambda e: cargar()
        filtro_estado.on_change = lambda e: cargar()

        try:
            cargar_combos()
        except Exception as ex:
            snackbar(f"Error cargando relaciones: {ex}", True)

        content.content = ft.Column([
            ft.Text("Tickets", size=24, weight=ft.FontWeight.BOLD),
            ft.Row([titulo,prioridad,estado], wrap=True),
            descripcion,
            ft.Row([usuario,tecnico,especialidad], wrap=True),
            ft.Row([ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=guardar),
                    ft.OutlinedButton("Limpiar", on_click=lambda e: (limpiar(), page.update()))]),
            ft.Row([buscar,filtro_estado], wrap=True),
            ft.Container(ft.Column([tabla], scroll=ft.ScrollMode.AUTO), expand=True),
        ], expand=True)
        cargar()

    def nav_change(e):
        idx = e.control.selected_index
        if idx == 0:
            dashboard_view()
        elif idx == 1:
            tickets_view()
        elif idx == 2:
            usuarios_view()
        else:
            tecnicos_view()

    nav = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=90,
        min_extended_width=210,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD, label="Inicio"),
            ft.NavigationRailDestination(icon=ft.Icons.CONFIRMATION_NUMBER, label="Tickets"),
            ft.NavigationRailDestination(icon=ft.Icons.PEOPLE, label="Usuarios"),
            ft.NavigationRailDestination(icon=ft.Icons.BUILD, label="Técnicos"),
        ],
        on_change=nav_change,
    )

    page.add(
        ft.Column([
            title,
            subtitle,
            ft.Divider(),
            ft.Row([
                nav,
                ft.VerticalDivider(width=1),
                content
            ], expand=True),
        ], expand=True)
    )
    dashboard_view()

if __name__ == "__main__":
    ft.app(target=main)
