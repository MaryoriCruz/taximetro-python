import time
import logging

from logger_config import setup_logging
from history import save_trip_to_history
from config import load_config   # 👉 IMPORTANTE

config = load_config()
config = load_config()
STOPPED_PRICE_PER_SECOND = config["stopped_price_per_second"]
MOVING_PRICE_PER_SECOND = config["moving_price_per_second"]

# ============================================
# CARGAR PRECIOS DESDE CONFIG.JSON
# ============================================
config = load_config()
STOPPED_PRICE_PER_SECOND = config["stopped_price_per_second"]
MOVING_PRICE_PER_SECOND = config["moving_price_per_second"]


# ============================================
# FUNCIONES DE UX
# ============================================

def print_header():
    """Muestra el encabezado principal del programa."""
    print("\n==============================")
    print("        F5 TAXIMETER 🚕")
    print("==============================\n")


def print_help():
    """Muestra la lista de comandos disponibles con una pequeña explicación."""
    print("\nAvailable commands:")
    print("  start   -> Start a new trip (initial state: stopped)")
    print("  stop    -> Set state to 'stopped' and count stopped time")
    print("  move    -> Set state to 'moving' and count moving time")
    print("  finish  -> End current trip and show summary")
    print("  help    -> Show this help message")
    print("  exit    -> Exit the program\n")


# ============================================
# CALCULAR TARIFA
# ============================================

def calculate_fare(seconds_stopped, seconds_moving):
    """
    Funcion para calcular la tarifa total en euros
    Usando precios configurables.
    """
    fare = (
        seconds_stopped * STOPPED_PRICE_PER_SECOND
        + seconds_moving * MOVING_PRICE_PER_SECOND
    )
    print(f"Este es el total:{fare}")
    return fare


# ============================================
# TAXIMETER (CLI)
# ============================================

def taximeter():
    """Maneja la interfaz de línea de comandos del taxímetro con UX mejorada."""
    print_header()
    print(
        f"Current prices: stopped={STOPPED_PRICE_PER_SECOND} €/s, "
        f"moving={MOVING_PRICE_PER_SECOND} €/s"
    )
    print_help()

    trip_activate = False
    stopped_time = 0.0
    moving_time = 0.0
    state = None
    state_start_time = 0.0

    while True:
        try:
            # Mostrar estado actual
            if trip_activate:
                print(f"\n[Trip active] State: {state}")
            else:
                print("\n[No active trip]")

            command = input("> ").strip().lower()

            # =======================
            # START
            # =======================
            if command == "start":
                if trip_activate:
                    print("⚠️  A trip is already in progress. Use 'finish' to end it.")
                    continue

                trip_activate = True
                stopped_time = 0.0
                moving_time = 0.0
                state = "stopped"
                state_start_time = time.time()

                print("✅ Trip started. Initial state: 'stopped'.")
                logging.info("Trip started. Initial state: stopped")


            # =======================
            # STOP / MOVE
            # =======================
            elif command in ("stop", "move"):
                if not trip_activate:
                    print("⚠️  No active trip. Use 'start' to begin a new trip.")
                    continue

                duration = time.time() - state_start_time

                if state == "stopped":
                    stopped_time += duration
                else:
                    moving_time += duration

                state = "stopped" if command == "stop" else "moving"
                state_start_time = time.time()

                print(f"✅ State changed to '{state}'. (+{duration:.1f}s)")
                logging.info(
                    "State changed to %s | duration=%.1fs",
                    state,
                    duration
                )


            # =======================
            # FINISH
            # =======================
            elif command == "finish":
                if not trip_activate:
                    print("⚠️  No active trip to finish.")
                    continue

                duration = time.time() - state_start_time

                if state == "stopped":
                    stopped_time += duration
                else:
                    moving_time += duration

                total_fare = calculate_fare(stopped_time, moving_time)

                print("\n--- Trip Summary ---")
                print(f"Stopped time: {stopped_time:.1f} seconds")
                print(f"Moving time: {moving_time:.1f} seconds")
                print(f"Total fare: €{total_fare:.2f}")
                print("---------------------\n")

                logging.info(
                    "Trip finished | stopped=%.1fs moving=%.1fs total=%.2f€",
                    stopped_time,
                    moving_time,
                    total_fare,
                )

                save_trip_to_history(stopped_time, moving_time, total_fare)

                trip_activate = False
                state = None
                print("✅ Trip finished. You can start a new one with 'start'.")


            # =======================
            # HELP
            # =======================
            elif command == "help":
                print_help()


            # =======================
            # EXIT
            # =======================
            elif command == "exit":
                print("👋 Exiting the program. Goodbye!")
                logging.info("Program exited by user")
                break


            # =======================
            # ENTER VACÍO
            # =======================
            elif command == "":
                continue


            # =======================
            # COMANDO DESCONOCIDO
            # =======================
            else:
                print("❌ Unknown command. Type 'help' to see available commands.")
                logging.warning("Unknown command entered: %s", command)

        except KeyboardInterrupt:
            print("\n⚠️  Detected Ctrl + C. Use 'exit' to close the program safely.")


# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    setup_logging()
    taximeter()
