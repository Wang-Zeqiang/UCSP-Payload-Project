import time
import math
import board
import analogio

adc = analogio.AnalogIn(board.A0)

R_FIXED = 10000   # 10k fixed resistor
R0 = 10000        # thermistor resistance at 25 C
T0 = 298.15       # 25 C in Kelvin
B = 3950          # beta constant
VCC = 3.3

while True:
    raw = adc.value
    vout = raw / 65535 * adc.reference_voltage
    print(f"ADC: {raw}, voltage: {vout:.3f} V")

    # Avoid dividing by zero if the wiring is loose or shorted
    if vout <= 0 or vout >= VCC:
        print("Check wiring: no valid reading")
    else:
        r_therm = R_FIXED * vout / (VCC - vout)
        inv_t = 1 / T0 + (1 / B) * math.log(r_therm / R0)
        temp_c = 1 / inv_t - 273.15
        temp_f = temp_c * 9 / 5 + 32
        print(f"Temp: {temp_c:.1f} C / {temp_f:.1f} F")

    time.sleep(1)