# === PICO PWM COMMUNICATION VERSION 2 ===

from machine import Pin, PWM, ADC, UART
import time
import random

# === CONFIGURATION ===
PWM_PIN = 15         # Broche PWM
ADC_PIN = 26         # Broche ADC (après filtre RC)
UART_TX = 0          # UART TX
UART_RX = 1          # UART RX
PWM_FREQ = 1000      # Fréquence PWM en Hz

# === INITIALISATION ===
pwm = PWM(Pin(PWM_PIN))
pwm.freq(PWM_FREQ)

adc = ADC(Pin(ADC_PIN))
uart = UART(0, baudrate=9600, tx=Pin(UART_TX), rx=Pin(UART_RX))

# === FONCTIONS ===

def set_duty_cycle(percent):
    """Applique un rapport cyclique PWM en %"""
    duty_u16 = int(percent * 65535 / 100)
    pwm.duty_u16(duty_u16)
    print(f"PWM duty cycle set to {percent:.1f}%")
    return percent

def read_voltage():
    """Lit la tension analogique en volts via ADC"""
    raw = adc.read_u16()
    voltage = raw * 3.3 / 65535
    print(f"ADC voltage: {voltage:.2f} V")
    return voltage

def compare_pwm(desired, measured_voltage):
    """Compare la consigne PWM à la tension mesurée"""
    expected_voltage = desired * 3.3 / 100
    diff = abs(expected_voltage - measured_voltage)
    print(f"Différence attendue vs mesurée : {diff:.2f} V")
    return diff

def send_data(data):
    """Envoie une chaîne via UART"""
    uart.write(data + "\n")
    print(f"Sent: {data}")

def receive_data():
    """Lit les données UART reçues"""
    if uart.any():
        data = uart.readline().decode().strip()
        print(f"Received: {data}")
        return data
    return None

# === PROGRAMME PRINCIPAL ===
def main():
    while True:
        # 1. Génère une consigne PWM aléatoire entre 10% et 90%
        duty = random.randint(10, 90)
        set_duty_cycle(duty)

        # 2. Attend que le filtre RC stabilise (simulation)
        time.sleep(1.5)

        # 3. Lit la tension analogique
        voltage = read_voltage()

        # 4. Compare la tension à la consigne PWM
        compare_pwm(duty, voltage)

        # 5. Envoie la consigne via UART
        send_data(f"PWM={duty}")

        # 6. Attend et affiche la réponse éventuelle
        response = receive_data()

        # 7. Pause avant la prochaine boucle
        time.sleep(2)

# === EXÉCUTION ===
main()