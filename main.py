import board
import busio
i2c = busio.I2C(scl=board.GP17, sda=board.GP16)

import adafruit_ht16k33.segments
from time import sleep

#put all the displays in a list
displays = [
    adafruit_ht16k33.segments.Seg14x4(i2c,address=0x70)
    ,adafruit_ht16k33.segments.Seg14x4(i2c,address=0x71)
    ,adafruit_ht16k33.segments.Seg14x4(i2c,address=0x72)
    ,adafruit_ht16k33.segments.Seg14x4(i2c,address=0x73)
]

#map the row, display, digit to the corresponding display digit
top_row_display_digit_map = (
    (0,0,0) #row 0, display 0, digit 0
    ,(0,0,1)
    ,(0,0,2)
    ,(0,0,3)
    ,(0,1,0) #row 0, dislay 1, digit 0 (5th digit in first row)
    ,(0,1,1)
)

bottom_row_display_digit_map = (
    (1,2,2) 
    ,(1,2,3)
    ,(1,3,0)
    ,(1,3,1)
    ,(1,3,2) 
    ,(1,3,3)
)

top_row_text = "SCOTTS"
bottom_row_text = "ROBOTS"
sleep_duration = 0.1

#restart animation on a loop
while True:
    #scroll in the top row from the left
    for animation_offset in range (1,len(top_row_text)+1):
        for digit_index in range(animation_offset):
            display = displays[top_row_display_digit_map[digit_index][1]] 
            mapped_digit = top_row_display_digit_map[digit_index][2]
            display[mapped_digit] = top_row_text[digit_index + (len(top_row_text) - animation_offset)]
        sleep(sleep_duration)

    #wait a half second before bottom row
    sleep(0.5)

    #scroll in bottom row from right
    for animation_offset in range (1,len(bottom_row_text)+1):
        for digit_index in range(animation_offset):
            display = displays[bottom_row_display_digit_map[(len(bottom_row_text)-1)-digit_index][1]] 
            mapped_digit = bottom_row_display_digit_map[(len(bottom_row_text)-1)-digit_index][2]
            display[mapped_digit] = bottom_row_text[(len(bottom_row_text)-1 - digit_index) - (len(bottom_row_text) - animation_offset)]
        sleep(sleep_duration)
    
    #sleep 10 seconds before looping the animation
    sleep(10)

    #clear rows before restarting animataion
    for digit in top_row_display_digit_map:
        displays[digit[1]][digit[2]] = " "
    for digit in bottom_row_display_digit_map:
        displays[digit[1]][digit[2]] = " "
