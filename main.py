import time
from pynput.keyboard import Controller
from PIL import ImageGrab


LIFE_COLOR = (239, 12, 4)
LIFE_COOR = (183, 29)

MANA_COLOR = (59, 61, 251)
MANA_COOR = (183, 46)

# Cada posición corresponde a una tecla
#
# posición 0 -> tecla 1 -> cada 3 segundos
# posición 1 -> tecla 2 -> cada 7 segundos
# posición 2 -> tecla 3 -> cada 10 segundos
# posición 3 -> tecla 4 -> cada 50 segundos
# posición 4 -> tecla 5 -> cada 90 segundos
# posición 5 -> tecla 6 -> cada 120 segundos
# posición 6 -> tecla 7 -> cada 150 segundos
# posición 7 -> tecla 8 -> cada 300 segundos
HABILIDADES = [3, 7, 10, 50, 90, 120, 150, 300]

# Habilidad de apuntar
APUNTAR_INTERVALO = 4
MANA_INTERVALO = 120
RECOGER_INTERVALO = 1

keyboard = Controller()


def press_key(key):
    keyboard.press(key)
    keyboard.release(key)


def pick_color(coor):
    x, y = coor

    return ImageGrab.grab(
        bbox=(x, y, x + 1, y + 1)
    ).getpixel((0, 0))


# Esperar 5 segundos
time.sleep(5)


# Buffos iniciales
for key in "45678":
    press_key(key)
    time.sleep(2.5)


# Inicio del temporizador
inicio = time.monotonic()

# Última ejecución de cada habilidad
ultima_ejecucion = [0] * len(HABILIDADES)

# Última ejecución de "e"
ultima_ejecucion_e = 0
ultima_ejecucion_0 = 0
ultima_ejecucion_f = 0

while True:

    ahora = time.monotonic()

    # Tiempo transcurrido
    tiempo = ahora - inicio

    # --------------------------------
    # ATAQUE BÁSICO
    # --------------------------------
    press_key("r")

    # --------------------------------
    # APUNTAR
    # Cada 4 segundos
    # --------------------------------
    if tiempo - ultima_ejecucion_e >= APUNTAR_INTERVALO:

        press_key("e")

        ultima_ejecucion_e = tiempo

    if tiempo - ultima_ejecucion_0 >= MANA_INTERVALO:
        press_key("0")
        ultima_ejecucion_0 = tiempo

    if tiempo - ultima_ejecucion_f >= RECOGER_INTERVALO:
        press_key("f")
        ultima_ejecucion_f = tiempo



    # --------------------------------
    # VIDA
    # --------------------------------
    if pick_color(LIFE_COOR) != LIFE_COLOR:
        press_key("9")

    # --------------------------------
    # MANA
    # --------------------------------
    """
    if pick_color(MANA_COOR) != MANA_COLOR:
        press_key("0")
    """
    # --------------------------------
    # HABILIDADES
    # --------------------------------
    for posicion, intervalo in enumerate(HABILIDADES):

        # Posición 0 = tecla 1
        # Posición 1 = tecla 2
        # ...
        tecla = str(posicion + 1)

        if tiempo - ultima_ejecucion[posicion] >= intervalo:

            press_key(tecla)

            ultima_ejecucion[posicion] = tiempo

    # Pequeña pausa
    time.sleep(0.05)