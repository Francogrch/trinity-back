## Entorno virtual

Crear entorno:

    python -m venv .venv

Activar entorno:

    source ./.venv/bin/activate

## Instalar dependencias

    pip install -r ./requirements.txt  

## Resetear la base de datos

    flask resetdb

## Correr flask

    flask run

o

    flask --app ./app.py run --debug
o

    python app.py
