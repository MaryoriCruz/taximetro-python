from datetime import datetime

def save_trip_to_history(seconds_stopped, seconds_moving, total_fare):
    """
    Guarda un registro del trayecto en un archivo de texto.
    Cada línea representa un viaje.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    line = (
        f"{timestamp} | "
        f"stopped={seconds_stopped:.1f}s | "
        f"moving={seconds_moving:.1f}s | "
        f"fare={total_fare:.2f}€\n"
    )

    with open("trip_history.txt", "a", encoding="utf-8") as file:
        file.write(line)