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
    "host": "dpg-d12cckh5pdvs73cjrjd0-a.oregon-postgres.render.com",
    "port": 5432,
    "dbname": "erp_bi",
    "user": "erp_bi_user",
    "password": "uertnfJpJgYEUfn02w7MSPbyueivAZaW"
}




# Umbrales configurables para alertas opcional
#UMBRAL_STOCK_MINIMO = 10.0  # %
#UMBRAL_MERMA_MAXIMA = 20.0  # %
#UMBRAL_ABANDONO_MAXIMO = 15.0  # %
