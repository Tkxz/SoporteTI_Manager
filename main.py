import flet as ft
from repository import SoporteRepository

repo = SoporteRepository()

def main(page: ft.Page):
    page.title = "SoporteTI Manager"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    def snackbar(msg, error=False):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(msg),
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
                ft.TextButton(content="Cancelar", on_click=cerrar),
                ft.Button(content="Eliminar", on_click=aceptar),
            ],
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    title = ft.Text("SoporteTI Manager", size=30, weight=ft.FontWeight.BOLD)
    subtitle = ft.Text("Gestión de tickets de soporte TI")
    content = ft.Container(expand=True)

    def dashboard_view():
        try:
            data = repo.resumen()
            cards = []
            for item in data:
                cards.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text(item["estado"], size=16),
                                ft.Text(
                                    str(item["total"]),
                                    size=30,
                                    weight=ft.FontWeight.BOLD
                                ),
                            ]),
                            padding=20,
                            width=200,
                        )
                    )
                )

            if not cards:
                cards = [ft.Text("No hay tickets registrados.")]

            content.content = ft.Column([
                ft.Text("Resumen de tickets", size=24, weight=ft.FontWeight.BOLD),
                ft.Row(cards, wrap=True),
                ft.Text("Resumen generado con GROUP BY sobre ticketsKL."),
            ])
        except Exception as ex:
            content.content = ft.Text(f"Error al cargar el resumen: {ex}")
        page.update()

    def usuarios_view():
        nombre = ft.TextField(label="Nombre", width=220)
        email = ft.TextField(label="Correo", width=240)
        dep = ft.TextField(label="Departamento", width=200)
        tel = ft.TextField(label="Teléfono", width=180)
        ext = ft.TextField(label="Extensión", width=120)
        buscar = ft.TextField(
            label="Buscar",
            prefix_icon=ft.Icons.SEARCH,
            width=300
        )

        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nombre")),
                ft.DataColumn(ft.Text("Correo")),
                ft.DataColumn(ft.Text("Departamento")),
                ft.DataColumn(ft.Text("Teléfono")),
                ft.DataColumn(ft.Text("Acciones")),
            ]
        )

        editing = {"id": None}

        def limpiar():
            editing["id"] = None
            for campo in [nombre, email, dep, tel, ext]:
                campo.value = ""

        def eliminar(uid):
            try:
                repo.eliminar_usuario(uid)
                snackbar("Usuario eliminado correctamente.")
                cargar(buscar.value or "")
            except Exception as ex:
                snackbar(f"No se pudo eliminar: {ex}", True)

        def cargar(f=""):
            try:
                rows = repo.listar_usuarios(f)
                tabla.rows = []

                for r in rows:
                    def editar_factory(row):
                        def editar(e):
                            editing["id"] = row["id_usuario"]
                            nombre.value = row["nombre"]
                            email.value = row["email"]
                            dep.value = row["departamento"]
                            tel.value = row["telefono"] or ""
                            ext.value = row["extension"] or ""
                            page.update()
                        return editar

                    def eliminar_factory(uid):
                        return lambda e: confirm_delete(
                            "¿Deseas eliminar este usuario?",
                            lambda: eliminar(uid)
                        )

                    tabla.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(r["id_usuario"]))),
                                ft.DataCell(ft.Text(r["nombre"])),
                                ft.DataCell(ft.Text(r["email"])),
                                ft.DataCell(ft.Text(r["departamento"])),
                                ft.DataCell(ft.Text(r["telefono"] or "-")),
                                ft.DataCell(
                                    ft.Row([
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            on_click=editar_factory(r)
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            on_click=eliminar_factory(r["id_usuario"])
                                        ),
                                    ])
                                ),
                            ]
                        )
                    )
                page.update()
            except Exception as ex:
                snackbar(f"Error al consultar usuarios: {ex}", True)

        def guardar(e):
            if not nombre.value or not email.value or not dep.value:
                snackbar(
                    "Nombre, correo y departamento son obligatorios.",
                    True
                )
                return

            try:
                if editing["id"]:
                    repo.actualizar_usuario(
                        editing["id"],
                        nombre.value,
                        email.value,
                        dep.value,
                        tel.value,
                        ext.value
                    )
                    snackbar("Usuario actualizado.")
                else:
                    repo.crear_usuario(
                        nombre.value,
                        email.value,
                        dep.value,
                        tel.value,
                        ext.value
                    )
                    snackbar("Usuario registrado.")

                limpiar()
                cargar()
                page.update()

            except Exception as ex:
                snackbar(f"Error al guardar usuario: {ex}", True)

        buscar.on_change = lambda e: cargar(buscar.value or "")

        content.content = ft.Column([
            ft.Text("Usuarios", size=24, weight=ft.FontWeight.BOLD),
            ft.Row([nombre, email, dep], wrap=True),
            ft.Row([
                tel,
                ext,
                ft.Button(content="Guardar",
                    icon=ft.Icons.SAVE,
                    on_click=guardar
                )
            ], wrap=True),
            buscar,
            ft.Container(
                content=ft.Column(
                    [tabla],
                    scroll=ft.ScrollMode.AUTO
                ),
                expand=True
            ),
        ], expand=True)

        cargar()

    def tecnicos_view():
        t_nombre = ft.TextField(label="Nombre técnico", width=220)
        t_email = ft.TextField(label="Correo", width=240)
        t_nivel = ft.Dropdown(
            label="Nivel",
            width=170,
            value="Junior",
            options=[
                ft.DropdownOption(key="Junior", text="Junior"),
                ft.DropdownOption(key="Semi Senior", text="Semi Senior"),
                ft.DropdownOption(key="Senior", text="Senior"),
            ]
        )

        e_nombre = ft.TextField(label="Especialidad", width=220)
        e_desc = ft.TextField(label="Descripción", width=300)
        tec_dd = ft.Dropdown(label="Técnico", width=250)
        esp_dd = ft.Dropdown(label="Especialidad", width=250)

        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Técnico")),
                ft.DataColumn(ft.Text("Especialidad")),
                ft.DataColumn(ft.Text("Acción")),
            ]
        )

        def quitar(tid, eid):
            try:
                repo.quitar_especialidad(tid, eid)
                snackbar("Asignación eliminada.")
                refrescar()
            except Exception as ex:
                snackbar(f"Error: {ex}", True)

        def refrescar():
            try:
                tecs = repo.listar_tecnicos()
                esps = repo.listar_especialidades()

                tec_dd.options = [
                    ft.DropdownOption(
                        key=str(x["id_tecnico"]),
                        text=x["nombre"]
                    )
                    for x in tecs
                ]

                esp_dd.options = [
                    ft.DropdownOption(
                        key=str(x["id_especialidad"]),
                        text=x["nombre"]
                    )
                    for x in esps
                ]

                tabla.rows = []

                for x in repo.listar_tecnico_especialidades():
                    tabla.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(x["tecnico"])),
                                ft.DataCell(ft.Text(x["especialidad"])),
                                ft.DataCell(
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        on_click=lambda e,
                                        t=x["tecnico_id"],
                                        s=x["especialidad_id"]: quitar(t, s)
                                    )
                                )
                            ]
                        )
                    )
                page.update()

            except Exception as ex:
                snackbar(
                    f"Error al cargar técnicos/especialidades: {ex}",
                    True
                )

        def crear_tec(e):
            if not t_nombre.value or not t_email.value:
                snackbar("Nombre y correo son obligatorios.", True)
                return

            try:
                repo.crear_tecnico(
                    t_nombre.value,
                    t_email.value,
                    t_nivel.value
                )
                t_nombre.value = ""
                t_email.value = ""
                snackbar("Técnico registrado.")
                refrescar()
            except Exception as ex:
                snackbar(f"Error: {ex}", True)

        def crear_esp(e):
            if not e_nombre.value:
                snackbar(
                    "El nombre de la especialidad es obligatorio.",
                    True
                )
                return

            try:
                repo.crear_especialidad(
                    e_nombre.value,
                    e_desc.value
                )
                e_nombre.value = ""
                e_desc.value = ""
                snackbar("Especialidad registrada.")
                refrescar()
            except Exception as ex:
                snackbar(f"Error: {ex}", True)

        def asignar(e):
            if not tec_dd.value or not esp_dd.value:
                snackbar("Selecciona técnico y especialidad.", True)
                return

            try:
                repo.asignar_especialidad(
                    int(tec_dd.value),
                    int(esp_dd.value)
                )
                snackbar("Especialidad asignada.")
                refrescar()
            except Exception as ex:
                snackbar(f"Error: {ex}", True)

        content.content = ft.Column([
            ft.Text(
                "Técnicos y especialidades",
                size=24,
                weight=ft.FontWeight.BOLD
            ),
            ft.Text("Registrar técnico", weight=ft.FontWeight.BOLD),
            ft.Row([
                t_nombre,
                t_email,
                t_nivel,
                ft.Button(content="Agregar", on_click=crear_tec)
            ], wrap=True),
            ft.Divider(),
            ft.Text("Registrar especialidad", weight=ft.FontWeight.BOLD),
            ft.Row([
                e_nombre,
                e_desc,
                ft.Button(content="Agregar", on_click=crear_esp)
            ], wrap=True),
            ft.Divider(),
            ft.Text(
                "Relación N:M técnicosKL ↔ especialidadesKL",
                weight=ft.FontWeight.BOLD
            ),
            ft.Row([
                tec_dd,
                esp_dd,
                ft.Button(content="Asignar", on_click=asignar)
            ], wrap=True),
            ft.Container(
                content=ft.Column(
                    [tabla],
                    scroll=ft.ScrollMode.AUTO
                ),
                expand=True
            ),
        ], expand=True)

        refrescar()

    def tickets_view():
        titulo = ft.TextField(label="Título", width=300)
        descripcion = ft.TextField(
            label="Descripción",
            width=420,
            multiline=True,
            min_lines=2,
            max_lines=3
        )
        prioridad = ft.Dropdown(
            label="Prioridad",
            width=150,
            value="Media",
            options=[
                ft.DropdownOption(key="Baja", text="Baja"),
                ft.DropdownOption(key="Media", text="Media"),
                ft.DropdownOption(key="Alta", text="Alta"),
                ft.DropdownOption(key="Crítica", text="Crítica"),
            ]
        )
        estado = ft.Dropdown(
            label="Estado",
            width=160,
            value="Abierto",
            options=[
                ft.DropdownOption(key="Abierto", text="Abierto"),
                ft.DropdownOption(key="En proceso", text="En proceso"),
                ft.DropdownOption(key="Resuelto", text="Resuelto"),
                ft.DropdownOption(key="Cerrado", text="Cerrado"),
            ]
        )

        usuario = ft.Dropdown(label="Usuario", width=250)
        tecnico = ft.Dropdown(label="Técnico", width=250)
        especialidad = ft.Dropdown(label="Especialidad", width=250)

        buscar = ft.TextField(
            label="Buscar ticket/usuario",
            prefix_icon=ft.Icons.SEARCH,
            width=300
        )

        filtro_estado = ft.Dropdown(
            label="Estado",
            width=180,
            value="Todos",
            options=[
                ft.DropdownOption(key="Todos", text="Todos"),
                ft.DropdownOption(key="Abierto", text="Abierto"),
                ft.DropdownOption(key="En proceso", text="En proceso"),
                ft.DropdownOption(key="Resuelto", text="Resuelto"),
                ft.DropdownOption(key="Cerrado", text="Cerrado"),
            ]
        )

        tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Título")),
                ft.DataColumn(ft.Text("Usuario")),
                ft.DataColumn(ft.Text("Técnico")),
                ft.DataColumn(ft.Text("Especialidad")),
                ft.DataColumn(ft.Text("Prioridad")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Acciones")),
            ]
        )

        editing = {"id": None}

        def cargar_combos():
            usuarios = repo.listar_usuarios()
            tecnicos = repo.listar_tecnicos()
            especialidades = repo.listar_especialidades()

            usuario.options = [
                ft.DropdownOption(
                    key=str(x["id_usuario"]),
                    text=x["nombre"]
                )
                for x in usuarios
            ]

            tecnico.options = [
                ft.DropdownOption(key="", text="Sin asignar")
            ] + [
                ft.DropdownOption(
                    key=str(x["id_tecnico"]),
                    text=x["nombre"]
                )
                for x in tecnicos
            ]

            especialidad.options = [
                ft.DropdownOption(
                    key=str(x["id_especialidad"]),
                    text=x["nombre"]
                )
                for x in especialidades
            ]

        def limpiar():
            editing["id"] = None
            titulo.value = ""
            descripcion.value = ""
            prioridad.value = "Media"
            estado.value = "Abierto"
            usuario.value = None
            tecnico.value = ""
            especialidad.value = None
            usuario.disabled = False

        def eliminar(tid):
            try:
                repo.eliminar_ticket(tid)
                snackbar("Ticket eliminado.")
                cargar()
            except Exception as ex:
                snackbar(f"No se pudo eliminar: {ex}", True)

        def cerrar_sp(tid):
            try:
                repo.cerrar_ticket_sp(
                    tid,
                    "Cierre realizado desde la aplicación Flet."
                )
                snackbar(
                    "Ticket cerrado mediante procedimiento almacenado."
                )
                cargar()
            except Exception as ex:
                snackbar(
                    f"No se pudo cerrar el ticket: {ex}",
                    True
                )

        def cargar():
            try:
                rows = repo.listar_tickets(
                    buscar.value or "",
                    filtro_estado.value or "Todos"
                )
                tabla.rows = []

                for r in rows:
                    def editar_factory(row):
                        def editar(e):
                            editing["id"] = row["id_ticket"]
                            titulo.value = row["titulo"]
                            descripcion.value = row["descripcion"]
                            prioridad.value = row["prioridad"]
                            estado.value = row["estado"]

                            tecnico.value = next(
                                (
                                    o.key
                                    for o in tecnico.options
                                    if o.text == row["tecnico"]
                                ),
                                ""
                            )

                            especialidad.value = next(
                                (
                                    o.key
                                    for o in especialidad.options
                                    if o.text == row["especialidad"]
                                ),
                                None
                            )

                            usuario.value = next(
                                (
                                    o.key
                                    for o in usuario.options
                                    if o.text == row["usuario"]
                                ),
                                None
                            )

                            usuario.disabled = True
                            page.update()

                        return editar

                    def eliminar_factory(tid):
                        return lambda e: confirm_delete(
                            "¿Deseas eliminar este ticket?",
                            lambda: eliminar(tid)
                        )

                    tabla.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(r["id_ticket"]))),
                                ft.DataCell(ft.Text(r["titulo"])),
                                ft.DataCell(ft.Text(r["usuario"])),
                                ft.DataCell(ft.Text(r["tecnico"])),
                                ft.DataCell(ft.Text(r["especialidad"])),
                                ft.DataCell(ft.Text(r["prioridad"])),
                                ft.DataCell(ft.Text(r["estado"])),
                                ft.DataCell(
                                    ft.Row([
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            on_click=editar_factory(r)
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.CHECK_CIRCLE,
                                            tooltip="Cerrar ticket",
                                            on_click=lambda e,
                                            tid=r["id_ticket"]: cerrar_sp(tid)
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            on_click=eliminar_factory(
                                                r["id_ticket"]
                                            )
                                        ),
                                    ])
                                ),
                            ]
                        )
                    )

                page.update()

            except Exception as ex:
                snackbar(
                    f"Error al consultar tickets: {ex}",
                    True
                )

        def guardar(e):
            if (
                not titulo.value
                or not descripcion.value
                or not especialidad.value
            ):
                snackbar(
                    "Título, descripción y especialidad son obligatorios.",
                    True
                )
                return

            try:
                tid = int(tecnico.value) if tecnico.value else None
                eid = int(especialidad.value)

                if editing["id"]:
                    repo.actualizar_ticket(
                        editing["id"],
                        titulo.value,
                        descripcion.value,
                        prioridad.value,
                        estado.value,
                        tid,
                        eid
                    )
                    snackbar("Ticket actualizado.")
                else:
                    if not usuario.value:
                        snackbar("Selecciona un usuario.", True)
                        return

                    repo.crear_ticket(
                        titulo.value,
                        descripcion.value,
                        prioridad.value,
                        int(usuario.value),
                        tid,
                        eid
                    )
                    snackbar("Ticket registrado.")

                limpiar()
                cargar()
                page.update()

            except Exception as ex:
                snackbar(f"Error al guardar ticket: {ex}", True)

        buscar.on_change = lambda e: cargar()
        filtro_estado.on_change = lambda e: cargar()

        try:
            cargar_combos()
        except Exception as ex:
            snackbar(f"Error cargando relaciones: {ex}", True)

        content.content = ft.Column([
            ft.Text("Tickets", size=24, weight=ft.FontWeight.BOLD),
            ft.Row([titulo, prioridad, estado], wrap=True),
            descripcion,
            ft.Row(
                [usuario, tecnico, especialidad],
                wrap=True
            ),
            ft.Row([
                ft.Button(content="Guardar",
                    icon=ft.Icons.SAVE,
                    on_click=guardar
                ),
                ft.OutlinedButton(content="Limpiar",
                    on_click=lambda e: (limpiar(), page.update())
                ),
            ]),
            ft.Row([buscar, filtro_estado], wrap=True),
            ft.Container(
                content=ft.Column(
                    [tabla],
                    scroll=ft.ScrollMode.AUTO
                ),
                expand=True
            ),
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
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.DASHBOARD,
                label="Inicio"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.CONFIRMATION_NUMBER,
                label="Tickets"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.PEOPLE,
                label="Usuarios"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.BUILD,
                label="Técnicos"
            ),
        ],
        on_change=nav_change
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
    ft.run(main)
