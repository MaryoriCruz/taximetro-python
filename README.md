F5 Taximeter 🎄🚕

¡Edición navideña del taxímetro CLI!
Una aplicación de línea de comandos para calcular tarifas de viajes en taxi con mejoras UX: colores, animaciones LED, mensajes aleatorios y descuentos navideños.

Características principales

Interfaz de línea de comandos interactiva y colorida.

Registro de viajes en un historial (trip_history.txt).

Cálculo de tarifas según el tiempo detenido y en movimiento.

Modo Navidad (xmas):

15% de descuento en la tarifa final.

Animaciones LED navideñas.

Mensajes aleatorios festivos.

Mini animación LED y jingle navideño (led y jingle).

Formato de tiempo legible (mm:ss).

Comandos claros y guía incorporada (help).

Comandos disponibles
Comando	Descripción
start	Inicia un nuevo viaje (estado inicial: detenido).
stop	Cambia el estado a stopped y contabiliza tiempo detenido.
move	Cambia el estado a moving y contabiliza tiempo en movimiento.
finish	Termina el viaje, muestra resumen, aplica descuento si xmas está activado.
xmas	Alterna el modo Navidad: descuentos + animaciones.
led	Muestra animación de luces LED navideñas.
jingle	Reproduce un mini jingle navideño (beeps).
help	Muestra esta guía de comandos.
exit	Sale de la aplicación de forma segura.
Instalación

Clonar el repositorio:

git clone <URL_DEL_REPO>
cd taximeter-project


Crear y activar un entorno virtual:

python -m venv venv
# Windows
venv\Scripts\activate
# Linux / Mac
source venv/bin/activate


Instalar dependencias (si hay):

pip install -r requirements.txt


Configurar precios (opcional) en config.json:

{
  "stopped_price_per_second": 0.05,
  "moving_price_per_second": 0.10
}

Uso

Ejecuta el programa:

python main.py


Sigue los comandos interactivos en la terminal.

Activa el modo Navidad para descuentos y animaciones:

>xmas


Al terminar un viaje, usa:

>finish


Verás un resumen de tu viaje, el descuento (si aplica), y un mensaje aleatorio navideño.

Ejemplo de salida
🎄 Christmas Edition 🎄
Current prices: stopped=0.05 €/s, moving=0.10 €/s

> start
✅ Trip started. Initial state: 'stopped'.

> move
✅ State changed to 'moving'. (+12.3s)

> finish
--- Trip Summary ---
Stopped time: 00m 30s
Moving time:  00m 12s
Total fare:   1.65 €
🎁 Christmas discount applied! (15% OFF)
---------------------
🎄 ¡Feliz Navidad! Gracias por viajar con nosotros.

Historia de viajes

Cada viaje se guarda en trip_history.txt.

Registro incluye: fecha y hora, tiempo detenido, tiempo en movimiento y tarifa final.

Contribuciones

¡Bienvenidas!

Añadir más animaciones navideñas 🎅

Expandir modos de viaje y descuentos

Mejorar la UX en CLI

