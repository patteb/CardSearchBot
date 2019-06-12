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
            self.feeder.write(self.feeder.speed)
            while not self.adc.check_sensor():
                sleep(0.02)
            # feeder_servo.detach()
            return True

    def sort(self, dir):
        self.sorter.write(150) if dir else self.sorter.write(30);
        while ADC.check_sensor(): sleep(.20)
        sleep(.150)
        self.sorter.write(83)
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
    # led[0]['ON']['HIGH']
    # TODO:register etc
    def __init__(self, config, bus, SortOrFeed):
        self.adr = hex(config.Servo)  # probably 0x40
        self.i2c = bus
        self.speed = int(config.servo_speed)

        if SortOrFeed:
            self.channel = int(config.sort_pin)
        else:
            self.channel = int(config.feed_pin)

    def set_speed(self, speed):
        self.speed = speed

    def write(self, value):
        pass
    # TODO write to servo
