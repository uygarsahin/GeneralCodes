import ctypes
import random
import os
from time import sleep

SetCursorPos = ctypes.windll.user32.SetCursorPos
mouse_event = ctypes.windll.user32.mouse_event

def left_click(x, y, clicks=1):
    SetCursorPos(x, y)
    for i in range(clicks):
      mouse_event(2, 0, 0, 0, 0)
      mouse_event(4, 0, 0, 0, 0)

def random_number(min_value, max_value):
    return random.randint(min_value, max_value)
os.system('cls')
while True:
      #left_click(300, 300)
      left_click(random_number(300,1200),random_number(300,800))  
      sleep(5)
      #left_click(500, 500)
      left_click(random_number(300,1200),random_number(300,800)) 
      sleep(5)
