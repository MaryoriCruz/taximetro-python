#config.py

import json
import os

#Valoremos que ahora mismo tiene nuestro codigo, con el config.json podemos modificarla

DEFAULT_CONFIG = {
    "stopped_price_per_second": 0.02,
    "moving_price_per_second": 0.05
}

def load_config(filename: str = "config.json") -> dict:
    """Carga la configuracion de precios desde un archivo JSON. 
        Si el archivo no existe o tiene errores, devuelve DEFAULT_CONFIG.
    """
    if not os.path.exists(filename):
        #Si no existe el archivo. devolvemos la configuración por defecto
        return DEFAULT_CONFIG.copy()
    
    try:
        #Abrimos y leemos el archivo config.json
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        # Si hay errores leyendo o parseando el JSON, usamos los valores por defecto
        return DEFAULT_CONFIG.copy()
        # Obtenemos los valores del JSON, o usamos los valores por defecto si faltan
        
    stopped_price = float(
        data.get("stopped_price_per_second", DEFAULT_CONFIG["stopped_price_per_second"])
    )

    moving_price = float(
        data.get("moving_price_per_second", DEFAULT_CONFIG["moving_price_per_second"])
    ) 

    return {
    "stopped_price_per_second": stopped_price,
    "moving_price_per_second": moving_price,
    }

    
