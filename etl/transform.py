import pandas as pd
from bd.database import get_conn_bi

def transformar_tabla(tabla_raw):
    """Carga datos de una tabla raw y devuelve un DataFrame limpio"""
    conn = get_conn_bi()
    df = pd.read_sql_query(f"SELECT * FROM {tabla_raw}", conn)
    conn.close()

    if "fecha_hora" in df.columns:
        df["fecha_hora"] = pd.to_datetime(df["fecha_hora"], errors="coerce")
        df["anio"] = df["fecha_hora"].dt.year
        df["mes"] = df["fecha_hora"].dt.month
        df["dia"] = df["fecha_hora"].dt.day

    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

    if "estado" in df.columns:
        df["estado"] = df["estado"].fillna(False).astype(bool)

    return df

def transformar_para_kpi_stock_minimo():
    """Carga y transforma datos para el KPI de stock mínimo"""
    conn = get_conn_bi()
    query = """
    SELECT
        ai.almaceninsumo_id,
        ai.cantidad,
        ai.stock_minimo,
        ai.almacen_id,
        ai.insumo_id,
        i.nombre AS nombre,
        i.categoria_id,
        i.tenant_id,
        c.nombre AS categoria,
        a.nombre AS almacen
    FROM raw_almacen_insumo ai
    JOIN raw_insumo i ON ai.insumo_id = i.insumo_id
    LEFT JOIN raw_categoria c ON i.categoria_id = c.categoria_id AND i.tenant_id = c.tenant_id
    LEFT JOIN raw_almacen a ON ai.almacen_id = a.almacen_id AND a.tenant_id = i.tenant_id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    df["categoria"] = df["categoria"].fillna("Sin categoría")
    df["almacen"] = df["almacen"].fillna("Sin almacén")

    return df

def transformar_para_kpi_reservas_completo():
    """Carga y transforma datos para los KPIs de reservas"""
    conn = get_conn_bi()

    # Carga de tablas raw
    df_reserva = pd.read_sql_query("SELECT * FROM raw_reserva", conn)
    df_cuenta_mesa = pd.read_sql_query("SELECT * FROM raw_cuenta_mesa", conn)
    df_venta = pd.read_sql_query("SELECT * FROM raw_venta", conn)

    conn.close()

    # --- Procesamiento de RESERVAS ---
    df_reserva["fecha_reserva"] = pd.to_datetime(df_reserva["fecha_reserva"], errors="coerce")
    df_reserva["created_at"] = pd.to_datetime(df_reserva["created_at"], errors="coerce")  # importante para agrupaciones
    df_reserva["anio"] = df_reserva["fecha_reserva"].dt.year
    df_reserva["mes"] = df_reserva["fecha_reserva"].dt.month
    df_reserva["semana"] = df_reserva["fecha_reserva"].dt.isocalendar().week
    df_reserva["dia"] = df_reserva["fecha_reserva"].dt.day
    df_reserva["estado"] = df_reserva["estado"].fillna(False).astype(bool)

    # --- Procesamiento de CUENTA MESA ---
    df_cuenta_mesa["fecha_hora_ini"] = pd.to_datetime(df_cuenta_mesa["fecha_hora_ini"], errors="coerce")
    df_cuenta_mesa["created_at"] = pd.to_datetime(df_cuenta_mesa["created_at"], errors="coerce")

    # --- Procesamiento de VENTAS ---
    df_venta["fecha_venta"] = pd.to_datetime(df_venta["fecha_venta"], errors="coerce")

    return df_reserva, df_cuenta_mesa, df_venta
