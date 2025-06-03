type_defs = """
    type Query {
        obtenerKPIStockMinimo(tenant_id: Int!): KPIStockMinimo
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
"""
