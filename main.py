import time
import logging


from logger_config import setup_logging
from history import save_trip_to_history
from config import load_config   # 👉 IMPORTANTE

# ============================================
# COLORES (ANSI)
# ============================================

RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"

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
    """Muestra el encabezado principal del programa (versión navideña)."""
    print(f"\n{MAGENTA}{BOLD}==============================")
    print("        F5 TAXIMETER 🚕")
    print("      🎄 Christmas Edition 🎄")
    print("==============================" + RESET)

def print_help():
    """Muestra la lista de comandos disponibles con una pequeña explicación."""
    print(f"\n{BOLD}Available commands:{RESET}")
    print(f"  {GREEN}start{RESET}   -> Start a new trip (initial state: stopped)")
    print(f"  {GREEN}stop{RESET}    -> Set state to 'stopped' and count stopped time")
    print(f"  {GREEN}move{RESET}    -> Set state to 'moving' and count moving time")
    print(f"  {GREEN}finish{RESET}  -> End current trip and show summary")
    print(f"  {MAGENTA}xmas{RESET}    -> Toggle Christmas mode (discount + lights)")
    print(f"  {CYAN}help{RESET}    -> Show this help message")
    print(f"  {RED}exit{RESET}    -> Exit the program\n")


def format_time(seconds: float) -> str:
    """
    Convierte segundos a formato mm:ss.
    Ejemplo: 75.3 -> "01:15"
    """
    total_seconds = int(seconds)
    minutes = total_seconds // 60
    remaining_seconds = total_seconds % 60
    return f"{minutes:02d}:{remaining_seconds:02d}"

def xmas_lights_animation(cycles: int = 3, delay: float = 0.2):
    """
    Muestra una animación simple de luces navideñas.
    'cycles' indica cuántas veces se repite el patrón.
    """

    patterns = [
        f"{RED}*{GREEN}*{YELLOW}*{CYAN}*{MAGENTA}*{RESET}",
        f"{GREEN}*{YELLOW}*{CYAN}*{MAGENTA}*{RED}*{RESET}",
        f"{YELLOW}*{CYAN}*{MAGENTA}*{RED}*{GREEN}*{RESET}",
    ]

    for i in range(cycles):
        pattern = patterns[i % len(patterns)]
        print(f"\r{pattern}  Christmas mode ON! {pattern}", end="", flush=True)
        time.sleep(delay) 

    print("\r" + " " * 60 + "\r", end="")
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
        f"Current prices: {YELLOW}stopped={STOPPED_PRICE_PER_SECOND} €/s{RESET}, "
        f"{YELLOW}moving={MOVING_PRICE_PER_SECOND} €/s{RESET}"
    )
    print_help()

    trip_activate = False
    stopped_time = 0.0
    moving_time = 0.0
    state = None
    state_start_time = 0.0

    xmas_mode = False # 🎄 Indica si el modo Navidad está activo

    while True:
        try:
            # Mostrar estado actual
            if trip_activate:
                print(
                    f"\n{CYAN}[Trip active]{RESET} "
                    f"State: {GREEN}{state}{RESET} | "
                    f"stopped={format_time(stopped_time)} | "
                    f"moving={format_time(moving_time)}"
                )
            else:
                print(f"\n{YELLOW}[No active trip]{RESET}")

            command = input("> ").strip().lower()

            # =======================
            # START
            # =======================
            if command == "start":
                if trip_activate:
                    print(f"{YELLOW}⚠️  A trip is already in progress. Use 'finish' to end it.{RESET}")
                    continue

                trip_activate = True
                stopped_time = 0.0
                moving_time = 0.0
                state = "stopped"
                state_start_time = time.time()

                print(f"{GREEN}✅ Trip started. Initial state: 'stopped'.{RESET}")
                logging.info("Trip started. Initial state: stopped")

            # =======================
            # STOP / MOVE
            # =======================
            elif command in ("stop", "move"):
                if not trip_activate:
                    print(f"{YELLOW}⚠️  No active trip. Use 'start' to begin a new trip.{RESET}")
                    continue

                duration = time.time() - state_start_time

                if state == "stopped":
                    stopped_time += duration
                else:
                    moving_time += duration

                state = "stopped" if command == "stop" else "moving"
                state_start_time = time.time()

                print(
                    f"{GREEN}✅ State changed to '{state}'. "
                    f"(+{duration:.1f}s){RESET}"
                )
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
                    print(f"{YELLOW}⚠️  No active trip to finish.{RESET}")
                    continue

                duration = time.time() - state_start_time

                if state == "stopped":
                    stopped_time += duration
                else:
                    moving_time += duration

                total_fare = calculate_fare(stopped_time, moving_time)

                # Aplicamos descuento navideño si el modo está activado
                final_fare = total_fare
                discount_text = ""
                if xmas_mode:
                    final_fare = total_fare * 0.8  # 20% de descuento
                    discount_text = f"{GREEN} (🎄 Christmas discount applied -20%){RESET}"

                print("\n--- Trip Summary ---")
                print(f"Stopped time: {format_time(stopped_time)} ({stopped_time:.1f} seconds)")
                print(f"Moving time: {format_time(moving_time)} ({moving_time:.1f} seconds)")
                print(f"Base fare : €{total_fare:.2f}")
                print(f"Final fare: {GREEN}€{final_fare:.2f}{RESET}{discount_text}")
                print("---------------------\n")
        
                logging.info(
                    "Trip finished | stopped=%.1fs moving=%.1fs base=%.2f€ final=%.2f€ xmas_mode=%s",
                    stopped_time,
                    moving_time,
                    total_fare,
                    final_fare,
                    xmas_mode,
                )

                save_trip_to_history(stopped_time, moving_time, final_fare)

                trip_activate = False
                state = None
                print(f"{GREEN}✅ Trip finished. You can start a new one with 'start'.{RESET}")

            # =======================
            # XMAS MODE (NAVIDAD)
            # =======================
            elif command == "xmas":
                xmas_mode = not xmas_mode  # alterna True/False

                if xmas_mode:
                    print(f"{GREEN}🎄 Christmas mode ACTIVATED! 20% discount applied to fares.{RESET}")
                    xmas_lights_animation()
                    logging.info("Christmas mode activated")
                else:
                    print(f"{YELLOW}🎄 Christmas mode DEACTIVATED. Normal fares restored.{RESET}")
                    logging.info("Christmas mode deactivated")


            # =======================
            # HELP
            # =======================
            elif command == "help":
                print_help()


            # =======================
            # EXIT
            # =======================
            elif command == "exit":
                print(f"{CYAN}👋 Exiting the program. Goodbye!{RESET}")
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
                print(
                    f"{RED}❌ Unknown command.{RESET} "
                    f"Type {CYAN}'help'{RESET} to see available commands."
                )
                logging.warning("Unknown command entered: %s", command)

        except KeyboardInterrupt:
            print(
                f"\n{YELLOW}⚠️  Detected Ctrl + C. "
                f"Use 'exit' to close the program safely.{RESET}"
            )



# ============================================
# EJECUCIÓN
# ============================================

if __name__ == "__main__":
    setup_logging()
    taximeter()
