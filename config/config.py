# config.py

# Conexión a la base de datos del ERP (fuente de datos)
DB_ERP = {
    "host": "localhost",
    "port": 5432,
    "dbname": "erp_zamo1",
    "user": "postgres",
    "password": "will"
}

# Conexión a la base de datos local del microservicio BI (data warehouse)
DB_BI = {
    "host": "localhost",
    "port": 5432,
    "dbname": "microservicio_zamo",
    "user": "postgres",
    "password": "will"
}



# Umbrales configurables para alertas opcional
#UMBRAL_STOCK_MINIMO = 10.0  # %
#UMBRAL_MERMA_MAXIMA = 20.0  # %
#UMBRAL_ABANDONO_MAXIMO = 15.0  # %
