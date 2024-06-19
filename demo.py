

import hd44780

pinout={
    'RS_GP_PIN': 22,	# pin 29
    'RW_GP_PIN': 21,	# pin 27
    'E_GP_PIN': 20,	# pin 26
    'D0_GP_PIN': 10,	# pin 14
    'D1_GP_PIN': 11,	# pin 15
    'D2_GP_PIN': 14,	# pin 19
    'D3_GP_PIN': 15,	# pin 20
    'D4_GP_PIN': 16,	# pin 21
    'D5_GP_PIN': 17,	# pin 22
    'D6_GP_PIN': 18,	# pin 24
    'D7_GP_PIN': 19	# pin 25
    }

lcd=hd44780.lcd(False,1,0,False,pinout)	# 8 bit, 2 lines, 5x8 font, read only mode
#lcd=hd44780.lcd(True,1,0,False,pinout)	# 4 bit, 2 lines, 5x8 font, read only mode

def hello():
    lcd.command('0000000001',22000)	# clear display, set DDRAM to 0
    lcd.command('0000001111')	# display on, cursor on, blink on
    lcd.command('0000000110')	# increment cursor position, no shift
    lcd.command('1010111100')	# print katakana character 'シ' (Shi) (ROM Code: A00)
    lcd.command('0011000000')	# 2nd row, 1st column
    lcd.command('1001000011')	# print latin chatacter'C'
    lcd.command('1011110110')	# print greek chatacter'Σ'

# hello()
