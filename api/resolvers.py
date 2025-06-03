from ariadne import QueryType
from kpi.stock_minimo import calcular_porcentaje_stock_minimo

query = QueryType()

@query.field("obtenerKPIStockMinimo")
def resolve_kpi_stock_minimo(_, info, tenant_id):
    return calcular_porcentaje_stock_minimo(tenant_id)
