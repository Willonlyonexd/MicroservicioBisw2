from ariadne import QueryType
from kpi.stock_minimo import calcular_porcentaje_stock_minimo
from kpi.reservas import calcular_kpis_reservas
from kpi.merma import calcular_kpi_merma

query = QueryType()

@query.field("obtenerKPIStockMinimo")
def resolve_kpi_stock_minimo(_, info, tenant_id):
    return calcular_porcentaje_stock_minimo(tenant_id)

@query.field("obtenerKPIReservas")
def resolve_kpi_reservas(_, info, tenant_id):
    return calcular_kpis_reservas(tenant_id)

@query.field("obtenerKPIMerma")
def resolve_kpi_merma(_, info, tenant_id):
    return calcular_kpi_merma(tenant_id)
