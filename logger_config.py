import logging


def setup_logging():
    """
    Configura el sistema de loggig para el taximetro.
    """
    logging.basicConfig(
        filename="taximeter.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

