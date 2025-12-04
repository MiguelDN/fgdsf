from datetime import datetime, date, timedelta

FORMATO = "%Y-%m-%d"

def fechas_inicio_semanas_str(timeline_from, timeline_to, delay_dias=0):
    """
    _summary_

    Args:
        timeline_from (_type_): _description_
        timeline_to (_type_): _description_
        delay_dias (int, optional): _description_. Defaults to 0.

    Returns:
        _type_: _description_
    """
    # Parsear strings a date
    fecha_inicio_original = datetime.strptime(timeline_from, FORMATO).date()
    fecha_fin = datetime.strptime(timeline_to, FORMATO).date()
    

    # 1) Aplicar delay
    fecha_inicio = fecha_inicio_original + timedelta(days=delay_dias)
    fecha_fin+=timedelta(days=delay_dias)

    # Si el inicio real queda fuera del rango, no hay semanas
    if fecha_inicio > fecha_fin:
        return []

    fechas = [fecha_inicio]

    # 2) Calcular el primer lunes después del inicio (o el mismo si ya es lunes)
    # weekday(): lunes=0,...,domingo=6
    if fecha_inicio.weekday() == 0:
        # Si ya es lunes, el siguiente será dentro de 7 días
        siguiente_lunes = fecha_inicio + timedelta(days=7)
    else:
        dias_hasta_lunes = 7 - fecha_inicio.weekday()
        siguiente_lunes = fecha_inicio + timedelta(days=dias_hasta_lunes)

    # 3) Añadir lunes sucesivos hasta salir del rango
    while siguiente_lunes <= fecha_fin:
        fechas.append(siguiente_lunes)
        siguiente_lunes += timedelta(days=7)

    # Devolver como strings YYYY-MM-DD
    return [f.strftime(FORMATO) for f in fechas]