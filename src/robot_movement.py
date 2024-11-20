import time
import mecanum_pico.py

# Move Forward and Then Diagonal
move_robot(1, 0, 0)
time.sleep(5.0)
move_robot(1, 1, 0)
time.sleep(2.0)
move_robot(1, -1, 0)
time.sleep(2.0)
stop()
time.sleep(5.0)

# Move in a box
move_robot(1, 0, 0)
time.sleep(2.0)
move_robot(0, 1, 0)
time.sleep(2.0)
move_robot(-1, 0, 0)
time.sleep(2.0)
move_robot(0, -1, 0)
time.sleep(2.0)
stop()