#!/usr/bin/env python3

import RPi.GPIO as GPIO # type: ignore

class Motor:
    def __init__(self, enablePin, forwardPin, backwardPin):
        self.enablePin = enablePin
        self.forwardPin = forwardPin
        self.backwardPin = backwardPin

        self._speed = 0

        GPIO.setup(self.enablePin, GPIO.OUT)
        GPIO.setup(self.forwardPin, GPIO.OUT)
        GPIO.setup(self.backwardPin, GPIO.OUT)

        self.speedpwm = GPIO.PWM(self.enablePin, 1000)
        self.speedpwm.start(0)
        pass

    @property
    def speed(self):
        return self._speed


    def set_speed(self, new_speed):
        print("new_speed", new_speed)
        new_speed = max(-100, new_speed)
        new_speed = min(100, new_speed)

        self._speed = new_speed
        self.speedpwm.ChangeDutyCycle(abs(new_speed))

        if(new_speed >= 0):
            GPIO.output(self.forwardPin, GPIO.HIGH)
            GPIO.output(self.backwardPin, GPIO.LOW)
        else:
            GPIO.output(self.forwardPin, GPIO.LOW)
            GPIO.output(self.backwardPin, GPIO.HIGH)

    def __del__(self):
        self.speedpwm.stop()
        GPIO.output(self.enablePin, GPIO.LOW)
        GPIO.output(self.forwardPin, GPIO.LOW)
        GPIO.output(self.backwardPin, GPIO.LOW)

        GPIO.cleanup()
        print('Motor deleted')


class Robot:
    def __init__(self):
        self.FrontLeftMotor = Motor(35, 16, 15)
        self.BackLeftMotor = Motor(12, 11, 13)
        self.BackRightMotor = Motor(32, 38, 40)
        self.FrontRightMotor = Motor(33, 37, 31)
        pass

    def set_speed(self, speedLeft, speedRight):
        self.BackLeftMotor.set_speed(speedLeft)
        self.FrontLeftMotor.set_speed(speedLeft)

        self.BackRightMotor.set_speed(speedRight)
        self.FrontRightMotor.set_speed(speedRight)

    def move(self, linearVel, angularVel):
        speedleft = linearVel - angularVel/2
        speedright = linearVel + angularVel/2
        self.set_speed(speedleft, speedright)

        return linearVel/angularVel if angularVel!=0 else float('inf')

    def move_with_radius(self, speed, radius):
        w = speed/radius if radius>0 else float('inf')
        self.move(speed, w)

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)