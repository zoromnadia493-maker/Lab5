from machine import Pin, I2C
import time

# Initialisation I2C
i2c = I2C(1, sda=Pin(14), scl=Pin(15))
rtc_address = 0x68

# Lecture des secondes au format DCB
def lire_secondes():
    raw = i2c.readfrom_mem(rtc_address, 0x00, 1)
    return (raw[0] >> 4) * 10 + (raw[0] & 0x0F)

# Initialisation du bouton
bouton = Pin(16, Pin.IN, Pin.PULL_DOWN)

# Ouverture du journal
log = open("log.txt", "a")

try:
    print("Appuie pour démarrer le jeu…")
    while True:
        while bouton.value() == 0:
            pass
        debut = lire_secondes()
        print("Début : {} secondes".format(debut))

        print("Compte mental de 15 secondes…")
        while bouton.value() == 0:
            pass
        fin = lire_secondes()
        print("Fin : {} secondes".format(fin))

        delta = (fin - debut) % 60
        print("Temps estimé : {} secondes".format(delta))

        log.write("Temps estimé : {} secondes\n".format(delta))
        log.flush()

        print("Nouvel essai dans 3 secondes…")
        time.sleep(3)

finally:
    log.close()