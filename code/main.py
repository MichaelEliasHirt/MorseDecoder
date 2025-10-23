import time
from machine import I2C, Pin,TouchPad
from I2C_LCD import I2cLcd

button = Pin(2,Pin.IN)

activeBuzzer=Pin(21,Pin.OUT)
activeBuzzer.value(0)

DIT_DURATION = 100
LOOP_SPEED:float = 5

DIT_BITS = DIT_DURATION / LOOP_SPEED
NO_BITS = DIT_BITS * 5
INTRA_BITS = DIT_BITS
INTERC_BITS = DIT_BITS * 3
ITERW_BITS = DIT_BITS * 7
STOP_BITS = DIT_BITS * 20

last_same_bits: int = 0
last_bit_on: int = 0
sequence: str = ""
string: str = ""

i2c = I2C(scl=Pin(14), sda=Pin(13), freq=400000)
devices = i2c.scan()
isPressed = False

MORSE_CODE = {"01":"a","1000":"b","1010":"c","100":"d","0":"e",
              "0010":"f","110":"g","0000":"h","00":"i","0111":"j","101":"k","0100":"l","11":"m",
              "10":"n","111":"o","0110":"p","1101":"q","010":"r","000":"s","1":"t","001":"u","0001":"v",
              "011":"w","1001":"x","1011":"y","1100":"z",
              "01111":"1","00111":"2","00011":"3","00001":"4","00000":"5",
              "10000":"6","11000":"7","11100":"8","11110":"9","11111":"0"
              }

if len(devices) == 0:
    print("No i2c device !")
else:
    for device in devices:
        print("I2C addr: "+hex(device))
        lcd = I2cLcd(i2c, device, 2, 16)


def main():
    global string
    while True:
        letter = morse_input()
        if letter:
            if letter == "#":
                string = ""
                lcd.clear()
            else:
                string += letter
                print("LETTER: ",letter)
    
            lcd.move_to(0, 0)
            lcd.putstr(string)
            
        time.sleep_ms(LOOP_SPEED)


def morse_input() -> str:
    global last_bit_on, last_same_bits, sequence
    letter = ""
    user_input = not button.value()
    if user_input:
        activeBuzzer.value(1)
    else: activeBuzzer.value(0)
    
    if user_input == last_bit_on:
        last_same_bits += 1
        
        if not last_bit_on:
            if sequence:
                if INTRA_BITS + 10 <= last_same_bits:
                    letter = check_sequence(sequence)
                    sequence = ""
            elif last_same_bits > STOP_BITS + 20:
                letter = "#"
        
    else:
        
        if last_bit_on:
            if 2 > last_same_bits:
                pass
            
            elif last_same_bits < DIT_BITS:
                sequence += "0"
                print("dit")
               
            elif DIT_BITS < last_same_bits < NO_BITS:
                sequence += "1"
                print("dah")
        else:
            if INTRA_BITS + 10 > last_same_bits:
                pass
            
            elif last_same_bits < INTERC_BITS + 10:
                print("gap---")
                sequence = ""
                
            elif last_same_bits < STOP_BITS:
                print("big-gap----")
                sequence = ""
                letter = " "
                
            else:
                letter = "#"
                  
        
        last_bit_on = user_input
        last_same_bits = 1
        
    return letter

def check_sequence(sequence:str):
    letter = MORSE_CODE.get(sequence)
    return letter

def update_display():
    lcd.move_to(0, 0)
    lcd.putstr("Counter:%d" %(count))
main()
try:
    main()
except:
    print("chrashed")





