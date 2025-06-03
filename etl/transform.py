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

def transformar_para_kpi_reservas():
    """Transformación básica para KPI de reservas"""
    df = transformar_tabla("raw_reserva")
    df = df[df["estado"].isin([True, False])]
    return df
