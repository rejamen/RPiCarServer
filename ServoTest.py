#!/usr/bin/python

from Raspi_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x6F)

servoMin = 180  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

'''
 p1 = (0   , 180)
 p2 = (180 , 600)

 m = y2 - y1  / x2 - x1
 m = 600 - 180 / 180 - 0
 m = 420 / 180
 m = 42 / 18

 y - y1 = m(x - x1), para el punto p1(0,180)
 y - 180 = 42(x - 0)/18
 y - 180 = 42 x /18
 y = 180  + 42x/18   siendo Y(valor a PWM) y X(angulo)

Para la posicion actual del motor  una vez ensamblado, los valores
permitidos son: 130 (maximo giro a la izquierda) y 230 (maximo derecha)

'''

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
try:
	while (True):
  	# Change speed of continuous servo on channel O
  		angle = raw_input("Angulo: ")
  		servoMin = 180 + 42*(int)(angle)/18
  		pwm.setPWM(0, 0, servoMin)

except KeyboardInterrupt:
		angle = "180"
		servoMin = 180 + 42*(int)(angle)/18
		pwm.setPWM(0, 0, servoMin)
		print "Motor stopped at 180 dregrees!!!"
		quit()
