# database.py

import psycopg2
from config.config import DB_ERP, DB_BI

def get_conn_erp():
    """Devuelve conexión a la base de datos del ERP (microservicio_erp5)"""
    return psycopg2.connect(
        host=DB_ERP["host"],
        port=DB_ERP["port"],
        dbname=DB_ERP["dbname"],
        user=DB_ERP["user"],
        password=DB_ERP["password"]
    )

def get_conn_bi():
    """Devuelve conexión a la base de datos del BI (microservicio_bi2)"""
    return psycopg2.connect(
        host=DB_BI["host"],
        port=DB_BI["port"],
        dbname=DB_BI["dbname"],
        user=DB_BI["user"],
        password=DB_BI["password"]
    )
