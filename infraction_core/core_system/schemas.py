schema_comparendos = {
    "type": "object",
    "properties": {
        "data": {
            "type": "object",
            "properties": {
                "comparendos": {
                    "type": ["object", "array"],
                    "items": {
                        "type": "object",
                        "properties": 
                            {
                                "codigoInfraccion": {"type": "string"},
                                "descripcionInfraccion": {"type": "string"},
                                "direccionComparendo": {"type": "string"},
                                "estadoComparendo": {"type": "string"},
                                "fechaComparendo": {"type": "string"},
                                "fotodeteccion": {"type": "string"},
                                "infractorComparendo": {"type": "string"},
                                "numeroComparendo": {"type": "string"},
                                "placaVehiculo": {"type": "string"},
                                "secretariaComparendo": {"type": "string"},
                                "servicioVehiculo": {"type": "string"},
                                "tipoVehiculo": {"type": "string"},
                                "total": {"type": "string"}
                            },
                            "required": ["codigoInfraccion", "descripcionInfraccion", "direccionComparendo",
                                         "estadoComparendo", "fechaComparendo", "infractorComparendo",
                                         "numeroComparendo", "placaVehiculo", "secretariaComparendo",
                                         "servicioVehiculo", "tipoVehiculo", "total"
                                         ]
                    }
                }
                                     
            },
            "required": ["comparendos"]
        }
    },
    "required": ["data"]
}

schema_resoluciones = {
    "type": "object",
    "properties": {
        "data": {
            "type": "object",
            "properties": {
                "resoluciones": {
                    "type": ["object", "array"],
                    "items":{
                        "properties": 
                            {
                                     
                                "estadosResoluciones": {"type": "string"},
                                "fechaComparendo": {"type": "string"},
                                "fechaResolucion": {"type": "string"},
                                "nombresInfractores": {"type": "string"},
                                "numeroComparendo": {"type": "string"},
                                "resoluciones": {"type": "string"},
                                "secretarias": {"type": "string"},
                                "total": {"type": "string"}
                            }, 
                            "required": ['estadosResoluciones', "fechaComparendo", "fechaResolucion",
                                         "nombresInfractores", "numeroComparendo", "resoluciones",
                                         "secretarias", "total"]}
                }
            },
            "required": ["resoluciones"]
        }
    },
    "required": ["data"]
}

