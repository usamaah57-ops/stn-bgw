def check_alerts(services):
    alerts = []

    # Fuel not arrived yet
    if "FUEL_ARRIVAL" not in services:
        alerts.append("⚠️ Fuel Arrival not recorded yet")

    # Loadsheet not completed
    if "LOADSHEET" not in services:
        alerts.append("⚠️ Loadsheet not completed")

    # Doors not closed
    if "CLOSE_DOOR" not in services:
        alerts.append("⚠️ Doors not closed")

    return alerts
