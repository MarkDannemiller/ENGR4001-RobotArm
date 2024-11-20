from machine import Pin, PWM
import math
import time
import utime
import rp2
rp2.PIO(0).remove_program()
from rp2 import PIO, StateMachine, asm_pio

# Set up Motor Pins =========================
freq = 1000  # 1 kHz (1000 cycles / second)

# Definition of where our pins are on the pico
IN1 = 3   # Motor IN1 on GP3
IN2 = 2  # Motor IN2 on GP2

# Sets up PWM over the IN1 and IN2 pins
pwm1 = PWM(Pin(IN1))
pwm2 = PWM(Pin(IN2))

pwm1.freq(freq)
pwm2.freq(freq)
#============================================
  
@asm_pio() # No additional arguments required

def pulse_counter():
    
    label("loop")           # Start of the loop
    mov(x, null)            # Clear X
    mov(osr, null)          # Clear OSR
    pull(noblock)           # Pull from TX FIFO - if this is empty the OSR is filled from X
                            # OSR must be empty for either to work
    mov(x, osr)             # Load value from OSR into X
    
    jmp(not_x, "continue")  # If X is not empty, we're going to reset the counter and output the data0
    mov(isr, y)             # Move Y (which is (2^32 - 1 - the number of edges)) into the ISR
    push()                  # Push that value into the RX FIFO
    mov(y, osr)             # Reset Y to 2^32 - 1 (which the value in the OSR right now)
       
    label("continue")       # If X is empty, we'll counting rising edges
    wait(0, pin, 0)         # wait for rising edge of input signal
    wait(1, pin, 0)
    jmp(y_dec, "loop")      # Jump back to the beginning and decrement Y.
    
# Create the state machine on the correct pin and start it, and initialise it.
pulse_counter_sm = StateMachine(0, pulse_counter, in_base=Pin(15)) #
pulse_counter_sm.active(1)
pulse_counter_sm.put(0xFFFFFFFF)

# Save the time in microseconds
ticks = utime.ticks_us()

def get_speed():
    global ticks
    utime.sleep(0.1)  # Wait for 1s
    last_ticks = ticks    
    pulse_counter_sm.put(0xFFFFFFFF) # This value both triggers the request for data and resets the counter
    ticks = utime.ticks_us() # Save the time the counter was restarted
                             # This is here so it can be right after the put() command for better accuracy
    
    if not pulse_counter_sm.rx_fifo(): # Check if there's any data to get
        print("No Data")
    else:
        pulses = 0xFFFFFFFF - pulse_counter_sm.get()            # Calculate the actual number of pulses
        period = utime.ticks_diff(utime.ticks_us(), last_ticks) # Calculate time difference
        # Display the data
        print(str(pulses) + " pulses, " + str(period/1000000) + " s, " + str(1000000 * pulses/period) + " Hz" )


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
        

while True:
    set_speed(float(input("Enter Speed: ")))
    for x in range(0,50):
        get_speed()


