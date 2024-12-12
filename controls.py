import time
from gpiozero import LED

# stepper for turntable
table_in1 = LED(26)
table_in2 = LED(21)
table_in3 = LED(20)
table_in4 = LED(16)

# stepper for fan arm
# A - 19
# B - 13
# C - 6
# D - 5
fan_in1 = LED(19)
fan_in2 = LED(13)
fan_in3 = LED(6)
fan_in4 = LED(5)

SPEED_DELAY = 0.002

def cw():

    for _ in range(10):
        table_in4.off()
        table_in1.on()
        table_in2.on()
        time.sleep(SPEED_DELAY)

        # table_in1.off()
        # time.sleep(SPEED_DELAY)

        table_in1.off()
        table_in3.on()
        time.sleep(SPEED_DELAY)

        # table_in2.off()
        # time.sleep(SPEED_DELAY)
        
        table_in2.off()
        table_in4.on()
        time.sleep(SPEED_DELAY)

        # table_in3.off()
        # time.sleep(SPEED_DELAY)

        table_in3.off()
        table_in1.on()
        time.sleep(SPEED_DELAY)

        # table_in4.off()
        # time.sleep(SPEED_DELAY)

def ccw():

    for _ in range(10):
        table_in4.on()
        table_in1.on()
        table_in2.off()
        time.sleep(SPEED_DELAY)

        table_in1.off()
        table_in3.on()
        time.sleep(SPEED_DELAY)
        
        table_in2.on()
        table_in4.off()
        time.sleep(SPEED_DELAY)

        table_in3.off()
        table_in1.on()
        time.sleep(SPEED_DELAY)

def down():

    for _ in range(10):
        fan_in4.off()
        fan_in1.on()
        fan_in2.on()
        time.sleep(SPEED_DELAY)

        # fan_in1.off()
        # time.sleep(SPEED_DELAY)

        fan_in1.off()
        fan_in3.on()
        time.sleep(SPEED_DELAY)

        # fan_in2.off()
        # time.sleep(SPEED_DELAY)
        
        fan_in2.off()
        fan_in4.on()
        time.sleep(SPEED_DELAY)

        # fan_in3.off()
        # time.sleep(SPEED_DELAY)

        fan_in3.off()
        fan_in1.on()
        time.sleep(SPEED_DELAY)

        # fan_in4.off()
        # time.sleep(SPEED_DELAY)

def up():

    for _ in range(10):
        fan_in4.on()
        fan_in1.on()
        fan_in2.off()
        time.sleep(SPEED_DELAY)

        fan_in1.off()
        fan_in3.on()
        time.sleep(SPEED_DELAY)
        
        fan_in2.on()
        fan_in4.off()
        time.sleep(SPEED_DELAY)

        fan_in3.off()
        fan_in1.on()
        time.sleep(SPEED_DELAY)

if __name__ == "__main__":
    # for _ in range(8):
    #    up()
    for _ in range(8000):
       ccw()
    # for _ in range(8):
    #    down()
    for _ in range(8000):
       cw()
