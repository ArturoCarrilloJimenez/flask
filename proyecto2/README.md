# Comandos flask

### Entrar en la carpeta de entorno virtual y ejecutar este para verlo en el navegador

```bash
source entornovirtual/bin/activate

flask --app proyecto2/manage.py run --host=0.0.0.0 --port=8080 --debug
```

### Acuatizar archivo requerimientos

```bash
pip freeze > requirements.txt
```

### Crear data base con el modelo y añadir datos

```bash
sh restar_db.sh 
```