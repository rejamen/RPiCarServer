from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from Raspi_PWM_Servo_Driver import PWM

import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Raspi_MotorHAT(addr=0x6f)


#Parametros para el servo motor
pwm = PWM(0x6F)

servoMin = 180  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

minAngle = 140
maxAngle = 230

minSpeed = 0
maxSpeed = 255

''' Ajuste matematico para variacion lineal del angulo de
 giro del servo
 
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
pwm.setPWMFreq(60)                        # Set frequency to 60 Hz to servo motor


# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)

	setAngle("180")
	servoMin = 180 + 42*statusRegister['angle']/18
  	pwm.setPWM(0, 0, servoMin)

atexit.register(turnOffMotors)

#Motor variables
motorLeft = mh.getMotor(1)
motorRight = mh.getMotor(2)

#Registro de estado: indica el estado de los motores. Consiste en un diccionario de 
#n posiciones en las que cada posicion almacena una propiedad de un motor 
#determinado: estado (on/off), velocidad, direccion de rotacion, angulo de giro 
#(para el caso de los servo), etc. 

#El programa principal se encuentra en un bucle infinito verificando el estado
#de dicho registro y actuando sobre los motores segun este lo indique. El valor
#de este registro sera modificado por la aplicacion cliente.

statusRegister = {
	'status': "off",        #indica el estado de TODOS los motores. 
	
	'direction': "forward", #indica la direccion de los motores traseros 
							#(ambos se moveran en la misma direccion siempre)
	
	'speed': 40,         # velocidad de los motores traseros. Valor entero
							#que varia entre 0 y velocidad maxima, usado para 
							#generar PWM.

	'angle': 180,		 # angulo de giro para el servo de la direccion
} 

#FUNCIONES PARA MODIFICAR LOS PARAMETROS INDIVIDUALES DEL REGISTRO DE ESTADO
#Cambia el estado de los motores traseros on/off
def setStatus(status):
	statusRegister['status'] = status

#Cambia la direccion forward/backward
def setDirection(direction):
	statusRegister['direction'] = direction

#Cambia la velocidad de los motores 0 - Vmax
def setSpeed(speed):
	auxSpeed = (int)speed
	if auxSpeed >= minSpeed and auxSpeed <= maxSpeed:
		statusRegister['speed'] = (int)(speed)
		

#Cambia el angulo de giro de la direccion
def setAngle(angle):
	auxAngle = (int)(angle)
	if auxAngle >= minAngle and auxAngle <= maxAngle: #valores permitidos de giro
		statusRegister['angle'] = auxAngle

#Servo motor
def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  pulseLength /= 4096                     # 12 bits of resolution
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)


#FUNCION PARA ACTUAR SOBRE LOS MOTORES SEGUN EL ESTADO DE 
#LAS PROPIEDADES
def checkStatusRegister():
	motorLeft.setSpeed(statusRegister['speed'])
	motorRight.setSpeed(statusRegister['speed'])

	if statusRegister['status'] == "on" and statusRegister['direction'] == "forward":
		motorLeft.run(Raspi_MotorHAT.FORWARD);
		motorRight.run(Raspi_MotorHAT.FORWARD);
	elif statusRegister['status'] == "on" and statusRegister['direction'] == "backward":
		motorLeft.run(Raspi_MotorHAT.BACKWARD);
		motorRight.run(Raspi_MotorHAT.BACKWARD);
	elif statusRegister['status'] == "off":
		motorLeft.run(Raspi_MotorHAT.RELEASE);
		motorRight.run(Raspi_MotorHAT.RELEASE);

	#establecer angulo de giro
  	servoMin = 180 + 42*statusRegister['angle']/18
  	pwm.setPWM(0, 0, servoMin)







while (1):
	prop = raw_input("\ndefina propiedad a modificar (status/direction/speed/angle): ")
	if prop == "status" or prop == "direction" or prop == "speed" or prop == "angle":
		value = raw_input("valor para la propiedad %s: " %prop)
		if prop == "status":
			setStatus(value)
		elif prop == "direction":
			setDirection(value)
		elif prop == "speed":
			setSpeed(value)
		elif prop == "angle":
			setAngle(value)
		
		print ("\nRegistro de estado:")
		print (statusRegister)

		checkStatusRegister()


	else:
		print ("Propiedad incorrecta %s" %prop)
		print ("test")
