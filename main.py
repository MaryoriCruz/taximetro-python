import time
import logging

from logger_config import setup_logging


def calculate_fare(seconds_stopped, seconds_moving):
    """
    Funcion para calcular la tarifa total en euros
    stopped: 0.02 €/s
    Moving: 0.05 €/s
    """
    fare = seconds_stopped * 0.02 + seconds_moving * 0.05
    print(f"Este es el total:{fare}")
    return fare

def taximeter():
    """
    Funcion para manejar y mostrar las opciones del taxímetro.
    """
    print("Welcome to the F5 taximeter")
    print("Available commands: 'start', 'stop', 'move', 'finish', 'exit'\n")
    trip_activate = False
    start_time = 0
    stopped_time = 0
    moving_time = 0
    state = None 
    state_start_time = 0

    while True: 
        command = input("> ").strip().lower()
        if command == "start":
            if trip_activate:
                print("Error: A trip is already in progress")
                continue
            trip_activate = True
            start_time = time.time()
            stopped_time = 0
            moving_time = 0
            state = "stopped"
            state_start_time = time.time()
            print("Trip started.Initial state: 'stopped' ")
            logging.info("Trip started. Initial state: stopped")
        
        elif command in ("stop", "move"):
            if not trip_activate: 
                print("Error: No active trip.Please start first")
                continue
            duration = time.time()- state_start_time
            if state == "stopped":
                stopped_time += duration
            else: 
                moving_time += duration

            state = "stopped" if command == "stop" else "moving"
            state_start_time = time.time()
            print(f"State changed to '{state}'. ")
            logging.info(
                "State changed to %s | duration=%.1fs",
                state,
                duration
            )
        
        elif command == "finish":
            if not trip_activate:
                print("Error: No active trip to finish.")
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
                "Trip finished | stopped=%1fs moving=%.1fs total=%.2f€",
                stopped_time,
                moving_time,
                total_fare
                )

            trip_activate = False
            state = None

        elif command == "exit":
            print("Exiting the program, Goodbye")
            logging.info("Program exited by user")
            break
        else:
            print("Unknown command. Use: start, stop, move, finish, or exit")
            logging.warning("Unknown command entered: %s", command)

if __name__ == "__main__":
    setup_logging()
    taximeter()
        



