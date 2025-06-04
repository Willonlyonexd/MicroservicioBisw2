import pandas as pd
from etl.transform import transformar_para_kpi_merma

def calcular_kpi_merma(tenant_id: int):
    df = transformar_para_kpi_merma()

    # Filtrar por tenant
    df = df[df["tenant_id"] == tenant_id]

    if df.empty:
        return {
            "porcentaje_merma": 0.0,
            "total_consumido": 0.0,
            "total_mermado": 0.0,
            "top_insumos": [],
            "por_categoria": [],
            "por_almacen": [],
            "por_dia": [],
            "por_mes": [],
            "motivos_merma": []
        }

    # Clasificación de movimientos
    df_consumo = df[df["tipo_movimiento_id"] == 2]
    df_merma = df[df["tipo_movimiento_id"] == 3]

    total_consumido = df_consumo["cantidad"].sum()
    total_mermado = df_merma["cantidad"].sum()

    total_total = total_consumido + total_mermado
    porcentaje_merma = round((total_mermado / total_total) * 100, 2) if total_total > 0 else 0.0

    # Top insumos con mayor merma
    top_insumos = df_merma.groupby(["insumo_id", "insumo"])["cantidad"] \
        .sum().reset_index(name="cantidad_merma") \
        .sort_values(by="cantidad_merma", ascending=False) \
        .head(10).to_dict(orient="records")

    # Por categoría
    por_categoria = df_merma.groupby("categoria")["cantidad"] \
        .sum().reset_index(name="total_merma")
    total = por_categoria["total_merma"].sum()
    por_categoria["porcentaje_merma"] = round((por_categoria["total_merma"] / total) * 100, 2)
    por_categoria = por_categoria[["categoria", "porcentaje_merma"]]
    por_categoria = por_categoria.rename(columns={"categoria": "nombre"}).to_dict(orient="records")

    # Por almacén
    por_almacen = df_merma.groupby("almacen")["cantidad"] \
        .sum().reset_index(name="total_merma")
    total = por_almacen["total_merma"].sum()
    por_almacen["porcentaje_merma"] = round((por_almacen["total_merma"] / total) * 100, 2)
    por_almacen = por_almacen[["almacen", "porcentaje_merma"]]
    por_almacen = por_almacen.rename(columns={"almacen": "nombre"}).to_dict(orient="records")

    # Tendencia por día
    por_dia = df_merma.groupby("fecha")["cantidad"] \
        .sum().reset_index(name="total_merma")
    por_dia = por_dia.sort_values("fecha")
    por_dia = por_dia.to_dict(orient="records")

    # Tendencia por mes
    df_merma["anio_mes"] = df_merma["fecha_hora"].dt.to_period("M").astype(str)
    por_mes = df_merma.groupby("anio_mes")["cantidad"] \
        .sum().reset_index(name="total_merma")
    por_mes = por_mes.rename(columns={"anio_mes": "fecha"})
    por_mes = por_mes.to_dict(orient="records")

    # Distribución por motivo
    motivos = df_merma.groupby("motivo")["cantidad"] \
        .sum().reset_index(name="cantidad")
    total_motivo = motivos["cantidad"].sum()
    motivos["porcentaje"] = round((motivos["cantidad"] / total_motivo) * 100, 2)
    motivos = motivos.rename(columns={"motivo": "motivo"}).to_dict(orient="records")

    return {
        "porcentaje_merma": porcentaje_merma,
        "total_consumido": round(total_consumido, 2),
        "total_mermado": round(total_mermado, 2),
        "top_insumos": top_insumos,
        "por_categoria": por_categoria,
        "por_almacen": por_almacen,
        "por_dia": por_dia,
        "por_mes": por_mes,
        "motivos_merma": motivos
    }
