from machine import Pin, PWM
import math
import time

freq = 1000  # 1 kHz (1000 cycles / second)

# Definition of where our pins are on the pico
IN1 = 3   # Motor IN1 on GP3
IN2 = 2  # Motor IN2 on GP2

# Sets up PWM over the IN1 and IN2 pins
pwm1 = PWM(Pin(IN1))
pwm2 = PWM(Pin(IN2))

pwm1.freq(freq)
pwm2.freq(freq)




# duty_cycle : [-1.0, 1.0]
def set_speed(speed):
    speed = max(min(speed, 1), -1)
    duty_cycle = int(abs(speed) * 65535)
    
    # Spin Forwards
    if speed > 0: 
        pwm1.duty_u16(duty_cycle)
        pwm2.duty_u16(0)
    # Spin Backwards
    elif speed < 0: 
        pwm2.duty_u16(duty_cycle)
        pwm1.duty_u16(0)
    # Stop Condition
    else:
        pwm1.duty_u16(0)
        pwm2.duty_u16(0)
    print("Set speed to:", speed)
        
        
# set_speed(1.0)
# time.sleep(5.0)
# set_speed(0.25)
# time.sleep(5.0)
# set_speed(-1.0)
# time.sleep(5.0)
while True:
    set_speed(float(input("Enter Speed: ")))
    
