import time
import logging
import random


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
    print(f"  {MAGENTA}led{RESET}     -> Show LED garland animation")
    print(f"  {MAGENTA}jingle{RESET}  -> Play a tiny Christmas jingle (beeps)")

def print_separator():
    """Imprime una línea separadora navideña."""
    print(f"{MAGENTA}" + "-" * 35 + RESET)
    
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

def led_strip_animation(cycles: int = 22, delay: float = 0.08, length: int = 26):
    """
    Animación de una guirnalda LED navideña con colores cambiantes.
    """
    colors = [RED, GREEN, YELLOW, CYAN, MAGENTA]
    symbol_on = "●"
    symbol_off = "○"

    for step in range(cycles):
        strip = ""

        for pos in range(length):
            color = colors[(pos + step) % len(colors)]

            if (pos + step) % 2 == 0:
                strip += f"{color}{symbol_on}{RESET} "
            else:
                strip += f"{color}{symbol_off}{RESET} "

        print(f"\r{strip}", end="", flush=True)
        time.sleep(delay)

    # Limpia la línea al final
    print("\r" + " " * (length * 2) + "\r", end="")


def play_xmas_jingle():
    """
    Hace una mini-melodia con beeps.
    Nota: en algunas terminales el sonido puede estar desactivado.
    """
    try:
        import winsound  # Solo Windows
        notes = [
            (659, 150), (659, 150), (659, 250),   # ♪ ♪ ♪
            (659, 150), (659, 150), (659, 250),   # ♪ ♪ ♪
            (659, 150), (784, 150), (523, 150), (587, 150), (659, 400)  # remate
        ]
        for freq, dur in notes:
            winsound.Beep(freq, dur)
            time.sleep(0.02)
    except Exception:
        # Fallback universal: campanita de consola
        for _ in range(10):
            print("\a", end="", flush=True)
            time.sleep(0.12)

def get_random_xmas_message(xmas_mode: bool = False) -> str:
    """
    Devuelve un mensaje navideño aleatorio para mostrar al finalizar el viaje.
    Si xmas_mode es True, prioriza mensajes con temática navideña.
    """
    generic = [
    "🚕 Gracias por viajar con nosotros.",
    "🌟 Esperamos que tu día vaya genial.",
    "👍 ¡Viaje finalizado con éxito!",
    "😄 ¡Vuelve pronto!",
]
    xmas_only = [
    "🎄 ¡Feliz Navidad! Gracias por viajar con nosotros.",
    "🎅 Que tus viajes sean tan suaves como la nieve.",
    "✨ ¡Ho ho ho! Descuento navideño aplicado.",
    "🧦 Ojalá tu día esté lleno de magia navideña.",
    ]
    pool = xmas_only + generic if xmas_mode else generic + xmas_only
    return random.choice(pool)
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
                #-------aquí estan nuetsros mensajes aleatorios---------
                msg = get_random_xmas_message(xmas_mode)
                print_separator()
                print(f"{MAGENTA}{BOLD}{msg}{RESET}")
                print_separator()
                logging.info("Showed random xmas message: %s", msg)
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
                    led_strip_animation()
                    play_xmas_jingle()
                    logging.info("Christmas mode activated")
                else:
                    print(f"{YELLOW}🎄 Christmas mode DEACTIVATED. Normal fares restored.{RESET}")
                    logging.info("Christmas mode deactivated")
            
            # =======================
            # LUCES LED
            # =======================
            elif command =="led":
                led_strip_animation()
            
            # =======================
            # SONIDO NAVIDEÑO
            # =======================
            elif command == "jingle":
                play_xmas_jingle()

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
