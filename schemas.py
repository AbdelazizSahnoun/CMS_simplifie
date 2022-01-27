glissade_update_schema = {
    "type": "object",
    "required": ["nom", "ouvert", "deblaye", "condition"],
    "properties": {
        "id": {"type": "number"},
        "nom": {"type": "string"},
        "ouvert": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
        },
        "deblaye": {
            "type": "number",
            "minimum": 0,
            "maximum": 1,
        },
        "condition": {"type": "string"},
    },
    "additionalProperties": False,
}
