from machine import Pin, PWM
import time
import servo_translator

# servo setup
shoulder_servo = PWM(Pin(0))
elbow_servo = PWM(Pin(1))
pen_servo = PWM(Pin(2))

for s in (shoulder_servo, elbow_servo, pen_servo):
    s.freq(50)

# pen control
def pen_up():
    pen_servo.duty_u16(servo_translator.translate(0))
    time.sleep(0.2)

def pen_down():
    pen_servo.duty_u16(servo_translator.translate(90))
    time.sleep(0.2)

# g-code parser
def parse_gcode_line(line: str):
    line = line.strip()
    if line.startswith("M3"):   # pen down
        return ("PEN_DOWN", None, None)
    elif line.startswith("M5"): # pen up
        return ("PEN_UP", None, None)
    elif line.startswith("G1"): # move command
        parts = line.split()
        s = e = None
        for p in parts:
            if p.startswith("S"):
                s = float(p[1:])
            elif p.startswith("E"):
                e = float(p[1:])
        return ("MOVE", s, e)
    else:
        return ("IGNORE", None, None)

# execute file
def execute_gcode(filename: str):
    with open(filename, "r") as f:
        for line in f:
            cmd, s, e = parse_gcode_line(line)
            if cmd == "MOVE" and s is not None and e is not None:
                shoulder_servo.duty_u16(servo_translator.translate(s))
                elbow_servo.duty_u16(servo_translator.translate(e))
                time.sleep(0.05)
            elif cmd == "PEN_DOWN":
                pen_down()
            elif cmd == "PEN_UP":
                pen_up()

# main code
def main():
    execute_gcode("circle.gcode")
    pen_up()

if __name__ == "__main__":
    main()