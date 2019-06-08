from time import sleep

import RPi.GPIO as GPIO
import smbus


class hardware:
    def __init__(self, config):
        bus = smbus.SMBus(1)
        self.ADC = ADC(config, bus)
        self.sorter = Servo(config, bus, True)
        self.feeder = Servo(config, bus, False)
        self.magazine = magazine(config)

    def query_feed(self):
        return self.magazine.check_empty()

    def feed(self):
        if self.magazine.check_empty() == 0:
            return False
        else:
            # feeder_servo.attach(FEED_PIN);
            self.feeder.write(self.feeder.speed)
            while not self.ADC.check_sensor():
                sleep(0.02)
            # feeder_servo.detach()
            return True

    def sort(self, dir):
        self.sorter.write(150) if dir else self.sorter.write(30);
        while ADC.check_sensor(): sleep(.20)
        sleep(.150)
        self.sorter.write(83)
        return True


class magazine:
    state = False

    def __init__(self, config):
        """Initialize magazine object via allocation of gpio-pin from config
        :param: configration file"""
        self.pin = config.gpio
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
        self.state = True if (GPIO.input(self.pin) == 1) else self.state = False

    def check_empty(self):
        """check if container is empty via gpio-attached switch"""
        self.state = True if (GPIO.input(self.pin) == 1) else self.state = False
        return self.state


class ADC:
    # TODO:register etc
    def __init__(self, config, bus):
        self.addr = hex(config.ADC)
        self.thresh = int(config.thresh)

    def check_sensor(self):
        sensorValue = 0.0
        for i in range(0, 10):
        # TODO get i2c values
        sensorValue = sensorValue / 10
        return True if sensorValue <= self.thresh else return False


class Servo:
    # TODO:register etc
    def __init__(self, config, bus, SortOrFeed):
        self.addr = hex(config.Servo)

        if SortOrFeed:
            self.pin = int(config.sort_pin)
        else:
            self.pin = int(config.feed_pin)

        self.bus = bus
        self.speed = int(config.servo_speed)

    def set_speed(self, speed):
        self.speed = speed

    def write(self, value):
    #TODO write to servo
