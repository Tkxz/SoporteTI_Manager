# Commits sugeridos

Para cumplir el requisito de mostrar avance real, evita subir todo en un solo commit.

Una secuencia recomendable:

```bash
git init
git add .
git commit -m "chore: estructura inicial del proyecto"
```

Después de crear la base:

```bash
git add sql/
git commit -m "feat: crear modelo relacional de soporte TI"
```

Después de configurar conexión:

```bash
git add database.py .env.example requirements.txt
git commit -m "feat: agregar conexion MySQL y variables de entorno"
```

Después del CRUD:

```bash
git add repository.py main.py
git commit -m "feat: implementar CRUD de usuarios tecnicos y tickets"
```

Después del trigger y procedimiento:

```bash
git add sql/02_trigger.sql sql/03_procedure.sql
git commit -m "feat: agregar historial automatico y cierre de tickets"
```

Después de filtros y resumen:

```bash
git add main.py sql/05_queries.sql
git commit -m "feat: agregar filtros joins y resumen de tickets"
```

Al finalizar documentación y captura:

```bash
git add README.md screenshots/
git commit -m "docs: completar README y captura de la aplicacion"
```
