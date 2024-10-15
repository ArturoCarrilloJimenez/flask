# Comandos flask

### Entrar en la carpeta de entorno virtual y ejecutar este para verlo en el navegador

```bash
source entornovirtual/bin/activate

flask --app proyect1/manage.py run --host=0.0.0.0 --port=8080 --debug
```

### Acualizar archivo requerimientos

```bash
pip freeze > requirements.txt
```

### Crear data base con el modelo y añadir datos de manage.py

```bash
flask --app manage.py create_tables

flask --app manage.py add_data_tables
```