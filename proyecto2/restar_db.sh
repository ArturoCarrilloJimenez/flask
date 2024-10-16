#!/bin/bash

# x muestra los comandos que se realizan
# e en caso de fallar detiene la ejecucion
set -ex

flask --app manage.py drop_tables

flask --app manage.py create_tables

flask --app manage.py add_data_tables

flask --app manage.py create_admin