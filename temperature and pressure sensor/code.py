import time
import board
import adafruit_bmp280

i2c = board.I2C()
sensor = adafruit_bmp280.Adafruit_BMP280_I2C(
    i2c, address=0x77
)

while True:
    print("Temperature: {:.2f} C".format(sensor.temperature))
    print("Pressure: {:.2f} hPa".format(sensor.pressure))
    print()
    time.sleep(1)