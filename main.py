import flet as ft
from repository import SoporteRepository

repo = SoporteRepository()

PRIMARY = "#1E40AF"
PRIMARY_2 = "#2563EB"
NAVY = "#0F172A"
SUCCESS = "#15803D"
WARNING = "#C2410C"
DANGER = "#B91C1C"
INFO = "#0369A1"
BACKGROUND = "#EEF2F7"
SURFACE = "#FFFFFF"
TEXT = "#0F172A"
MUTED = "#64748B"
BORDER = "#CBD5E1"



def main(page: ft.Page):
    page.title = "SoporteTI Manager"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = BACKGROUND
    page.padding = 0

    def snackbar(msg, error=False):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(msg),
            bgcolor=DANGER if error else SUCCESS,
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

    title = ft.Text(
        "SoporteTI Manager",
        size=26,
        weight=ft.FontWeight.BOLD,
        color="#FFFFFF",
    )
    subtitle = ft.Text(
        "Centro de gestión de soporte técnico",
        color="#DBEAFE",
        size=13,
    )
    content = ft.Container(expand=True, padding=24)

    def panel(child, padding=18):
        return ft.Container(
            content=child,
            bgcolor=SURFACE,
            padding=padding,
            border_radius=14,
            border=ft.Border.all(1, BORDER),
        )

    def metric_card(title_text, value, icon, bg, fg, subtitle_text=""):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(icon, color="#FFFFFF", size=26),
                        bgcolor=fg,
                        width=52,
                        height=52,
                        border_radius=12,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Column(
                        [
                            ft.Text(title_text, size=13, color=MUTED),
                            ft.Text(
                                str(value),
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT,
                            ),
                            ft.Text(subtitle_text, size=11, color=MUTED) if subtitle_text else ft.Container(),
                        ],
                        spacing=1,
                    ),
                ],
                spacing=14,
            ),
            bgcolor=bg,
            padding=18,
            width=225,
            border_radius=14,
            border=ft.Border.all(1, BORDER),
        )

    def status_chip(texto, fg, bg):
        return ft.Container(
            content=ft.Text(texto, size=11, weight=ft.FontWeight.BOLD, color=fg),
            bgcolor=bg,
            padding=ft.Padding.symmetric(horizontal=10, vertical=5),
            border_radius=999,
        )

    def dashboard_view():
        try:
            resumen_rows = repo.resumen()
            tickets = repo.listar_tickets("", "Todos")
            usuarios = repo.listar_usuarios("")
            tecnicos = repo.listar_tecnicos()
            especialidades = repo.listar_especialidades()

            resumen = {r["estado"]: r["total"] for r in resumen_rows}
            total = len(tickets)
            abiertos = resumen.get("Abierto", 0)
            proceso = resumen.get("En proceso", 0)
            resueltos = resumen.get("Resuelto", 0)
            cerrados = resumen.get("Cerrado", 0)
            criticos = sum(1 for t in tickets if t["prioridad"] == "Crítica")
            sin_asignar = sum(1 for t in tickets if t["tecnico"] == "Sin asignar")

            prioridad_info = {
                "Baja": ("#166534", "#DCFCE7"),
                "Media": ("#075985", "#E0F2FE"),
                "Alta": ("#9A3412", "#FFEDD5"),
                "Crítica": ("#991B1B", "#FEE2E2"),
            }
            estado_info = {
                "Abierto": ("#075985", "#E0F2FE"),
                "En proceso": ("#9A3412", "#FFEDD5"),
                "Resuelto": ("#166534", "#DCFCE7"),
                "Cerrado": ("#475569", "#E2E8F0"),
            }

            recent_rows = []
            for t in tickets[:6]:
                pfg, pbg = prioridad_info.get(t["prioridad"], (MUTED, "#E2E8F0"))
                efg, ebg = estado_info.get(t["estado"], (MUTED, "#E2E8F0"))
                recent_rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(f'#{t["id_ticket"]}', weight=ft.FontWeight.BOLD)),
                            ft.DataCell(ft.Text(t["titulo"])),
                            ft.DataCell(ft.Text(t["usuario"])),
                            ft.DataCell(ft.Text(t["tecnico"])),
                            ft.DataCell(status_chip(t["prioridad"], pfg, pbg)),
                            ft.DataCell(status_chip(t["estado"], efg, ebg)),
                        ]
                    )
                )

            if recent_rows:
                recent_content = ft.Row(
                    [
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("ID")),
                                ft.DataColumn(ft.Text("Ticket")),
                                ft.DataColumn(ft.Text("Usuario")),
                                ft.DataColumn(ft.Text("Técnico")),
                                ft.DataColumn(ft.Text("Prioridad")),
                                ft.DataColumn(ft.Text("Estado")),
                            ],
                            rows=recent_rows,
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO,
                )
            else:
                recent_content = ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.INBOX, size=40, color=MUTED),
                            ft.Text("Todavía no hay tickets registrados.", color=MUTED),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=25,
                    alignment=ft.Alignment.CENTER,
                )

            content.content = ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "Panel principal",
                                        size=30,
                                        weight=ft.FontWeight.BOLD,
                                        color=TEXT,
                                    ),
                                    ft.Text(
                                        "Vista general del servicio de soporte.",
                                        color=MUTED,
                                    ),
                                ],
                                spacing=2,
                            ),
                            ft.Container(expand=True),
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.CIRCLE, color=SUCCESS, size=12),
                                        ft.Text("Sistema operativo", color=SUCCESS, size=12),
                                    ],
                                    spacing=6,
                                ),
                                bgcolor="#DCFCE7",
                                padding=ft.Padding.symmetric(horizontal=12, vertical=7),
                                border_radius=999,
                            ),
                        ]
                    ),

                    ft.Text(
                        "Estado de tickets",
                        size=17,
                        weight=ft.FontWeight.BOLD,
                        color=TEXT,
                    ),
                    ft.Row(
                        [
                            metric_card("Tickets totales", total, ft.Icons.CONFIRMATION_NUMBER, "#EFF6FF", PRIMARY, "Todos los registros"),
                            metric_card("Abiertos", abiertos, ft.Icons.MARK_EMAIL_UNREAD, "#E0F2FE", INFO, "Esperando atención"),
                            metric_card("En proceso", proceso, ft.Icons.SYNC, "#FFF7ED", WARNING, "Actualmente atendidos"),
                            metric_card("Resueltos", resueltos, ft.Icons.CHECK_CIRCLE, "#F0FDF4", SUCCESS, "Problemas solucionados"),
                        ],
                        wrap=True,
                        spacing=14,
                    ),
                    ft.Row(
                        [
                            metric_card("Cerrados", cerrados, ft.Icons.ARCHIVE, "#F8FAFC", "#475569", "Casos finalizados"),
                            metric_card("Críticos", criticos, ft.Icons.WARNING, "#FEF2F2", DANGER, "Prioridad crítica"),
                            metric_card("Sin asignar", sin_asignar, ft.Icons.PERSON_OFF, "#FFF7ED", WARNING, "Requieren técnico"),
                            metric_card("Usuarios", len(usuarios), ft.Icons.PEOPLE, "#F5F3FF", "#6D28D9", "Solicitantes"),
                        ],
                        wrap=True,
                        spacing=14,
                    ),

                    ft.Text(
                        "Recursos del sistema",
                        size=17,
                        weight=ft.FontWeight.BOLD,
                        color=TEXT,
                    ),
                    ft.Row(
                        [
                            metric_card("Técnicos", len(tecnicos), ft.Icons.ENGINEERING, "#ECFDF5", "#047857", "Personal disponible"),
                            metric_card("Especialidades", len(especialidades), ft.Icons.CATEGORY, "#FDF4FF", "#A21CAF", "Áreas de soporte"),
                        ],
                        wrap=True,
                        spacing=14,
                    ),

                    panel(
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text(
                                            "Tickets recientes",
                                            size=18,
                                            weight=ft.FontWeight.BOLD,
                                            color=TEXT,
                                        ),
                                        ft.Container(expand=True),
                                        ft.Text(
                                            "Últimos 6 registros",
                                            size=12,
                                            color=MUTED,
                                        ),
                                    ]
                                ),
                                recent_content,
                            ],
                            spacing=12,
                        )
                    ),
                ],
                spacing=16,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            )

        except Exception as ex:
            content.content = panel(
                ft.Column(
                    [
                        ft.Icon(ft.Icons.ERROR_OUTLINE, color=DANGER, size=40),
                        ft.Text(
                            "No se pudo cargar el panel",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT,
                        ),
                        ft.Text(str(ex), color=MUTED),
                    ],
                    spacing=8,
                )
            )

        page.update()

    def usuarios_view():
        nombre = ft.TextField(label="Nombre completo", width=220)
        email = ft.TextField(label="Correo electrónico", width=240)
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
                                            tooltip="Editar",
                                            on_click=editar_factory(r)
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            tooltip="Eliminar",
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
            ft.Text("Usuarios", size=26, weight=ft.FontWeight.BOLD, color=TEXT),
            ft.Text("Registra y administra a las personas que pueden solicitar soporte.", color=MUTED),
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
        t_email = ft.TextField(label="Correo electrónico", width=240)
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
        e_desc = ft.TextField(label="Descripción del problema", width=300)
        tec_dd = ft.Dropdown(label="Técnico asignado", width=250)
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
                size=26,
                weight=ft.FontWeight.BOLD,
                color=TEXT
            ),
            ft.Text(
                "Organiza al equipo de soporte y las áreas que puede atender.",
                color=MUTED
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
        titulo = ft.TextField(label="Título del problema", width=300)
        descripcion = ft.TextField(
            label="Descripción del problema",
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

        usuario = ft.Dropdown(label="Usuario solicitante", width=250)
        tecnico = ft.Dropdown(label="Técnico asignado", width=250)
        especialidad = ft.Dropdown(label="Especialidad", width=250)

        buscar = ft.TextField(
            label="Buscar ticket o usuario",
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
                                            tooltip="Editar",
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
                                            tooltip="Eliminar",
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
            ft.Text("Tickets", size=26, weight=ft.FontWeight.BOLD, color=TEXT),
            ft.Text("Crea, asigna, busca y actualiza solicitudes de soporte.", color=MUTED),
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
            usuarios_view()
        elif idx == 2:
            tecnicos_view()
        else:
            tickets_view()

    nav = ft.NavigationRail(
        selected_index=0,
        bgcolor="#E2E8F0",
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=96,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.DASHBOARD,
                label="Inicio"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.PEOPLE,
                label="Usuarios"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.ENGINEERING,
                label="Técnicos"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.CONFIRMATION_NUMBER,
                label="Tickets"
            ),
        ],
        on_change=nav_change
    )

    page.add(
        ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(ft.Icons.SUPPORT_AGENT, color="#FFFFFF", size=28),
                                bgcolor=PRIMARY_2,
                                width=46,
                                height=46,
                                border_radius=12,
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Column([title, subtitle], spacing=1),
                            ft.Container(expand=True),
                            ft.Container(
                                content=ft.Text(
                                    "Soporte TI",
                                    color="#DBEAFE",
                                    size=12,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                bgcolor="#1E3A8A",
                                padding=ft.Padding.symmetric(horizontal=12, vertical=7),
                                border_radius=999,
                            ),
                        ],
                        spacing=12,
                    ),
                    bgcolor=NAVY,
                    padding=ft.Padding.symmetric(horizontal=24, vertical=15),
                ),
                ft.Row(
                    [
                        ft.Container(
                            content=nav,
                            bgcolor="#E2E8F0",
                            padding=ft.Padding.only(top=12),
                        ),
                        ft.Container(
                            content=content,
                            expand=True,
                            bgcolor=BACKGROUND,
                        ),
                    ],
                    expand=True,
                    spacing=0,
                ),
            ],
            expand=True,
            spacing=0,
        )
    )

    dashboard_view()

if __name__ == "__main__":
    ft.run(main)