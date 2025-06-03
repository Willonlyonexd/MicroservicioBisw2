# etl/sync.py

import schedule
import time
import psycopg2.extras
import logging
from bd.database import get_conn_erp, get_conn_bi

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

TABLAS = [
    ("cliente", "raw_cliente"),
    ("cuenta_mesa", "raw_cuenta_mesa"),
    ("pedido", "raw_pedido"),
    ("pedido_detalle", "raw_pedido_detalle"),
    ("producto", "raw_producto"),
    ("categoria", "raw_categoria"),
    ("insumo", "raw_insumo"),
    ("movimiento_inventario", "raw_movimiento_inventario"),
    ("almacen_insumo", "raw_almacen_insumo"),
    ("almacen", "raw_almacen"),
    ("tipo_movimiento", "raw_tipo_movimiento"),
    ("reserva", "raw_reserva"),
    ("venta", "raw_venta")
]

def sincronizar_tabla(tabla_origen, tabla_destino):
    try:
        conn_erp = get_conn_erp()
        conn_bi = get_conn_bi()
        cur_erp = conn_erp.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur_bi = conn_bi.cursor()

        cur_erp.execute(f"SELECT * FROM {tabla_origen}")
        registros = cur_erp.fetchall()

        if registros:
            columnas = registros[0].keys()
            columnas_str = ', '.join(columnas)
            valores_str = ', '.join([f"%({col})s" for col in columnas])

            # Limpiar tabla destino
            cur_bi.execute(f"DELETE FROM {tabla_destino}")

            # Insertar registros nuevos
            for fila in registros:
                cur_bi.execute(f"INSERT INTO {tabla_destino} ({columnas_str}) VALUES ({valores_str})", fila)

            conn_bi.commit()
            logging.info(f"✔️ Sincronizada: {tabla_destino} ({len(registros)} registros)")
        else:
            logging.warning(f"⚠️ Sincronización omitida: {tabla_destino} (sin datos)")

        cur_erp.close()
        cur_bi.close()
        conn_erp.close()
        conn_bi.close()

    except Exception as e:
        logging.error(f"❌ Error en sincronización de {tabla_destino}: {e}")

def ejecutar_sync():
    logging.info("🔄 Iniciando sincronización ETL")
    for origen, destino in TABLAS:
        sincronizar_tabla(origen, destino)
    logging.info("✅ Sincronización completa")

if __name__ == "__main__":
    # Programar cada 5 minutos
    schedule.every(5).minutes.do(ejecutar_sync)
    logging.info("🟢 Servicio de sincronización programado cada 5 minutos...")

    # Ejecutar al iniciar
    ejecutar_sync()

    while True:
        schedule.run_pending()
        time.sleep(1)
