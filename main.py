# main.py

import threading
import schedule
import time
import uvicorn
from fastapi import FastAPI
from ariadne.asgi import GraphQL
from ariadne import make_executable_schema

from etl.sync import ejecutar_sync
from api.schema import type_defs
from api.resolvers import query

# Configurar esquema de GraphQL
schema = make_executable_schema(type_defs, query)
graphql_app = GraphQL(schema, debug=True)

# Crear instancia FastAPI y montar GraphQL
app = FastAPI()
app.mount("/", graphql_app)

# Función que corre el ETL cada 5 minutos
def start_etl_schedule():
    print("🔁 Iniciando ETL programado...")
    ejecutar_sync()  # Sync inicial
    schedule.every(5).minutes.do(ejecutar_sync)

    while True:
        schedule.run_pending()
        time.sleep(1)

# Ejecutar app y ETL al iniciar
if __name__ == "__main__":
    threading.Thread(target=start_etl_schedule, daemon=True).start()
    print("🚀 Servidor iniciado en http://localhost:8000")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
