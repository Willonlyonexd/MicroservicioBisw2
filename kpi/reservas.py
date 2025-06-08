import pandas as pd
from etl.transform import transformar_para_kpi_reservas_completo
import calendar

def calcular_kpis_reservas(tenant_id: int):
    df_reserva, df_cuenta_mesa, df_venta = transformar_para_kpi_reservas_completo()

    # Filtrado por tenant
    df_reserva = df_reserva[df_reserva["tenant_id"] == tenant_id]
    df_cuenta_mesa = df_cuenta_mesa[df_cuenta_mesa["tenant_id"] == tenant_id]
    df_venta = df_venta[df_venta["tenant_id"] == tenant_id]

    if df_reserva.empty:
        return {
            "tasa_abandono": 0.0,
            "reservas_por_dia": [],
            "reservas_por_semana": [],
            "reservas_por_mes": [],
            "tamanio_promedio_grupo": 0.0,
            "conversion_ventas": 0.0
        }

    df_reserva["created_at"] = pd.to_datetime(df_reserva["created_at"], errors="coerce")

    # Tasa de abandono
    total_reservas = len(df_reserva)
    total_confirmadas = df_reserva[df_reserva["estado"]].shape[0]
    total_abandonadas = total_reservas - total_confirmadas
    tasa_abandono = round((total_abandonadas / total_reservas) * 100, 2)

    # Enriquecimiento de fechas
    df_reserva["fecha"] = df_reserva["created_at"].dt.date
    df_reserva["anio"] = df_reserva["created_at"].dt.year
    df_reserva["mes"] = df_reserva["created_at"].dt.month
    df_reserva["nombre_mes"] = df_reserva["mes"].apply(lambda x: calendar.month_name[x])
    df_reserva["dia"] = df_reserva["created_at"].dt.day
    df_reserva["nombre_dia"] = df_reserva["created_at"].dt.day_name()
    df_reserva["semana"] = df_reserva["created_at"].dt.isocalendar().week
    df_reserva["semana_anio"] = df_reserva["semana"]
    df_reserva["inicio_semana"] = df_reserva["created_at"] - pd.to_timedelta(df_reserva["created_at"].dt.weekday, unit="d")
    df_reserva["fin_semana"] = df_reserva["inicio_semana"] + pd.Timedelta(days=6)

    # Por Día
    agrupado_dia = df_reserva.groupby("fecha").agg(
        anio=("anio", "first"),
        mes=("mes", "first"),
        nombre_mes=("nombre_mes", "first"),
        dia=("dia", "first"),
        nombre_dia=("nombre_dia", "first"),
        semana_anio=("semana_anio", "first"),
        total=("reserva_id", "count"),
        confirmadas=("estado", lambda x: x.sum()),
        abandonadas=("estado", lambda x: (~x).sum())
    ).reset_index()

    reservas_por_dia = [
        {
            "fecha": str(row["fecha"]),
            "anio": int(row["anio"]),
            "mes": int(row["mes"]),
            "nombre_mes": row["nombre_mes"],
            "dia": int(row["dia"]),
            "nombre_dia": row["nombre_dia"],
            "semana_anio": int(row["semana_anio"]),
            "total": int(row["total"]),
            "confirmadas": int(row["confirmadas"]),
            "abandonadas": int(row["abandonadas"])
        }
        for _, row in agrupado_dia.iterrows()
    ]

    # Por Semana (agrupado correctamente por anio + semana)
    agrupado_semana = df_reserva.groupby(["anio", "semana"]).agg(
        inicio_semana=("inicio_semana", "first"),
        fin_semana=("fin_semana", "first"),
        total=("reserva_id", "count"),
        confirmadas=("estado", lambda x: x.sum()),
        abandonadas=("estado", lambda x: (~x).sum())
    ).reset_index().sort_values(by=["anio", "semana"])

    reservas_por_semana = [
        {
            "semana": int(row["semana"]),
            "anio": int(row["anio"]),
            "inicio_semana": row["inicio_semana"].strftime("%Y-%m-%d"),
            "fin_semana": row["fin_semana"].strftime("%Y-%m-%d"),
            "total": int(row["total"]),
            "confirmadas": int(row["confirmadas"]),
            "abandonadas": int(row["abandonadas"])
        }
        for _, row in agrupado_semana.iterrows()
    ]

    # Por Mes (agrupado correctamente por anio + mes)
    agrupado_mes = df_reserva.groupby(["anio", "mes"]).agg(
        nombre_mes=("nombre_mes", "first"),
        total=("reserva_id", "count"),
        confirmadas=("estado", lambda x: x.sum()),
        abandonadas=("estado", lambda x: (~x).sum())
    ).reset_index().sort_values(by=["anio", "mes"])

    reservas_por_mes = [
        {
            "mes": int(row["mes"]),
            "anio": int(row["anio"]),
            "nombre_mes": row["nombre_mes"],
            "total": int(row["total"]),
            "confirmadas": int(row["confirmadas"]),
            "abandonadas": int(row["abandonadas"])
        }
        for _, row in agrupado_mes.iterrows()
    ]

    # Tamaño promedio del grupo
    col_personas = "cantidad_personas" if "cantidad_personas" in df_reserva.columns else "num_comensales"
    tamanio_promedio_grupo = round(df_reserva[col_personas].mean(), 2) if col_personas in df_reserva else 0.0

    # Conversión en ventas
    cuentas_con_reserva = df_cuenta_mesa[["cuenta_mesa_id", "created_at"]].copy()
    ventas_con_cuenta = df_venta.merge(cuentas_con_reserva, on="cuenta_mesa_id", how="inner")
    total_con_venta = ventas_con_cuenta.shape[0]
    conversion_ventas = round((total_con_venta / total_reservas) * 100, 2) if total_reservas > 0 else 0.0

    return {
        "tasa_abandono": tasa_abandono,
        "reservas_por_dia": reservas_por_dia,
        "reservas_por_semana": reservas_por_semana,
        "reservas_por_mes": reservas_por_mes,
        "tamanio_promedio_grupo": tamanio_promedio_grupo,
        "conversion_ventas": conversion_ventas
    }
