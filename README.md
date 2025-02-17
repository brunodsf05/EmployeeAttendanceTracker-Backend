# ControlDePresencia2025 - Android
Hecho por Bruno Di Sabatino

## Base de datos
Son comandos para alterar la base de datos durante el desarrollo:

### Inicio
Es necesario para inicializar la base de datos y sus tablas.
```sh
flask db init
```

### Tras cada cambio
Actualiza la base de datos con los cambios que le hayamos hecho a los modelos.
```sh
flask db migrate
flask db upgrade
```