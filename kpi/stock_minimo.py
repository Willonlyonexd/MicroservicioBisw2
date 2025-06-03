from etl.transform import transformar_para_kpi_stock_minimo

def calcular_porcentaje_stock_minimo(tenant_id):
    df = transformar_para_kpi_stock_minimo()

    # Verificación preventiva
    if "tenant_id" not in df.columns:
        raise ValueError("La columna 'tenant_id' no existe en el DataFrame")

    # Filtro por tenant
    df = df[df["tenant_id"] == tenant_id]

    if df.empty:
        return {
            "porcentaje_bajo_stock": 0,
            "total_items": 0,
            "items_bajo_stock": 0,
            "top_insumos": [],
            "por_categoria": [],
            "por_almacen": []
        }

    total_items = df.shape[0]
    df_bajo_stock = df[df["cantidad"] < df["stock_minimo"]]
    items_bajo_stock = df_bajo_stock.shape[0]
    porcentaje = round((items_bajo_stock / total_items) * 100, 2)

    # Top 10 insumos con mayor desviación negativa
    df_bajo_stock = df_bajo_stock.copy()
    df_bajo_stock["desviacion"] = df_bajo_stock["cantidad"] - df_bajo_stock["stock_minimo"]

    top_insumos = df_bajo_stock.sort_values("desviacion").head(10)[
        ["insumo_id", "nombre", "cantidad", "stock_minimo", "desviacion"]
    ].to_dict(orient="records")

    # Agrupación por categoría (si está presente)
    por_categoria = []
    if "categoria" in df.columns:
        por_categoria = df.groupby("categoria") \
            .apply(lambda g: round((g[g["cantidad"] < g["stock_minimo"]].shape[0] / g.shape[0]) * 100, 2)) \
            .reset_index(name="porcentaje_bajo_stock") \
            .rename(columns={"categoria": "nombre"}) \
            .to_dict(orient="records")

    # Agrupación por almacén (si está presente)
    por_almacen = []
    if "almacen" in df.columns:
        por_almacen = df.groupby("almacen") \
            .apply(lambda g: round((g[g["cantidad"] < g["stock_minimo"]].shape[0] / g.shape[0]) * 100, 2)) \
            .reset_index(name="porcentaje_bajo_stock") \
            .rename(columns={"almacen": "nombre"}) \
            .to_dict(orient="records")

    return {
        "porcentaje_bajo_stock": porcentaje,
        "total_items": total_items,
        "items_bajo_stock": items_bajo_stock,
        "top_insumos": top_insumos,
        "por_categoria": por_categoria,
        "por_almacen": por_almacen
    }
