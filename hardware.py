from time import sleep

import RPi.GPIO as GPIO
import smbus


class Hardware:
    def __init__(self, config):
        self.i2c = smbus.SMBus(1)
        self.adc = ADC(config, self.i2c)
        self.sorter = Servo(config, self.i2c, True)
        self.feeder = Servo(config, self.i2c, False)
        self.magazine = Magazine(config)

    def query_feed(self):
        return self.magazine.check_empty()

    def feed(self):
        if self.magazine.check_empty() == 0:
            return False
        else:
            # feeder_servo.attach(FEED_PIN);
            self.feeder.set_speed(self.feeder.speed)
            while not self.adc.check_sensor():
                sleep(0.02)
            # feeder_servo.detach()
            return True

    def sort(self, dir):
        self.sorter.set_angle(150) if dir else self.sorter.set_angle(30);
        while ADC.check_sensor(): sleep(.20)
        sleep(.150)
        self.sorter.set_angle(83)
        return True


class Magazine:
    state = False

    def __init__(self, config):
        """Initialize magazine object via allocation of gpio-pin from config
        :param config: configration file"""
        self.pin = config.gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        self.state = True if (GPIO.input(self.pin) == 1) else False

    def check_empty(self):
        """check if container is empty via gpio-attached switch
        :return: state of the magazine switch"""
        self.state = True if (GPIO.input(self.pin) == 1) else False
        return self.state


class ADC:
    CONTROL = 0x00

    def __init__(self, config, bus):
        self.adr = hex(config.ADC)  # probably 0x48
        self.thresh = int(config.thresh)
        self.i2c = bus
        self.i2c.write_byte_data(self.adr, self.CONTROL, 0x00)

    def check_sensor(self):
        sensor_value = 0.0
        self.i2c.read_byte_data(self.adr, 0)
        for i in range(0, 10):
            sleep(0.01)
            sensor_value += self.i2c.read_byte_data(self.adr, 0)
        sensor_value = sensor_value / 10
        return True if sensor_value <= self.thresh else False


class Servo:
    """PCA9685 PWM Controller Servo Object. See datasheet @ https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf"""
    # registers
    MODE1 = 0x00
    MODE2 = 0x01
    PRE_SCALE = 0xFE

    def __init__(self, config, bus, sort_or_feed):
        self.adr = hex(config.Servo)  # probably 0x40
        self.i2c = bus
        self.speed = int(config.servo_speed)
        self.channel = int(config.sort_pin) if sort_or_feed else int(config.feed_pin)

        # initialize channel register addresses (as to not do that manually...)
        # e.g: Channel["ON"]["LOW"] = 0xf2
        reg_on = {"LOW": 0x06 + 4 * self.channel, "HIGH": 0x07 + 4 * self.channel}
        reg_off = {"LOW": 0x08 + 4 * self.channel, "HIGH": 0x09 + 4 * self.channel}
        self.register = ({"ON": reg_on, "OFF": reg_off})

        # initialize control registers (pgs. 14 & 16 for reference. May need some testing in MODE2)
        self.i2c.write_byte_data(self.adr, self.MODE1, 0x00)
        self.i2c.write_byte_data(self.adr, self.MODE1, 0x1C)

        # set default servo pwm frequency
        self.i2c.write_byte_data(self.adr, self.PRE_SCALE, 0x79)  # 50Hz (20ms) @ 25MHz internal oscillator

    def set_speed(self, speed):
        """Divide given value in high and low byte and write it to i2c
        :param speed: integer 0..4095 corresponding to angle/speed of servo"""
        speed_low = speed & 0x00FF
        speed_high = (speed & 0xFF00) >> 8

        self.i2c.write_byte_data(self.adr, self.register["ON"]["LOW"], 0x00)
        self.i2c.write_byte_data(self.adr, self.register["ON"]["HIGH"], 0x00)
        self.i2c.write_byte_data(self.adr, self.register["OFF"]["LOW"], speed_low)
        self.i2c.write_byte_data(self.adr, self.register["OFF"]["HIGH"], speed_high)

    def set_pwm_freq(self, freq):
        """Setting PWM period to given frequency. See pg.25 of PCA9685 Datasheet
         :param freq: """
        value = int((25000000 / (4096.0 * freq)) - 1)
        self.i2c.write_byte_data(self.adr, self.PRE_SCALE, value)

    def set_angle(self, deg):
        """set servo to a angle
        :param deg: Angle 0..180deg"""
        self.set_speed(int((deg / 180.0) * 4096))
