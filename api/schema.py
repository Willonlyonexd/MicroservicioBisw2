type_defs = """
    type Query {
        obtenerKPIStockMinimo(tenant_id: Int!): KPIStockMinimo
        obtenerKPIReservas(tenant_id: Int!): KPIReservas
        obtenerKPIMerma(tenant_id: Int!): KPIMerma
    }

    type KPIStockMinimo {
        porcentaje_bajo_stock: Float
        total_items: Int
        items_bajo_stock: Int
        top_insumos: [InsumoDesviado]
        por_categoria: [GrupoStock]
        por_almacen: [GrupoStock]
    }

    type InsumoDesviado {
        insumo_id: Int
        nombre: String
        cantidad: Float
        stock_minimo: Float
        desviacion: Float
    }

    type GrupoStock {
        nombre: String
        porcentaje_bajo_stock: Float
    }

    type KPIReservas {
        tasa_abandono: Float
        reservas_por_dia: [GrupoFecha]
        reservas_por_semana: [GrupoSemana]
        reservas_por_mes: [GrupoMes]
        tamanio_promedio_grupo: Float
        conversion_ventas: Float
    }

    type GrupoFecha {
        fecha: String
        anio: Int
        mes: Int
        nombre_mes: String
        dia: Int
        nombre_dia: String
        semana_anio: Int
        total: Int
        confirmadas: Int
        abandonadas: Int
    }

    type GrupoSemana {
        semana: Int
        anio: Int
        inicio_semana: String
        fin_semana: String
        total: Int
        confirmadas: Int
        abandonadas: Int
    }

    type GrupoMes {
        mes: Int
        anio: Int
        nombre_mes: String
        total: Int
        confirmadas: Int
        abandonadas: Int
    }

    type KPIMerma {
        porcentaje_merma: Float
        total_consumido: Float
        total_mermado: Float
        top_insumos: [InsumoMerma]
        por_categoria: [GrupoMerma]
        por_almacen: [GrupoMerma]
        por_dia: [GrupoTiempo]
        por_mes: [GrupoTiempo]
        motivos_merma: [GrupoMotivo]
    }

    type InsumoMerma {
        insumo_id: Int
        insumo: String
        cantidad_merma: Float
    }

    type GrupoMerma {
        nombre: String
        porcentaje_merma: Float
    }

    type GrupoTiempo {
        fecha: String
        total_merma: Float
    }

    type GrupoMotivo {
        motivo: String
        cantidad: Float
        porcentaje: Float
    }
"""
