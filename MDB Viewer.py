from mdb_parser import MDBParser, MDBTable
from pynput import keyboard
from threading import Thread
from PIL import Image
import time
import re
import os

def clearConsole():
    os.system('cls||echo -e \\\\033c')

db = 0

filepath = os.path.dirname(os.path.realpath(__file__))

print("Available database files: ")

amount = 0
selection = -1
i = 1

for root, dir, file in os.walk(filepath):
    for name in file:
        if name.endswith(".mdb"):
            print(str(i) + ": " + name)
            i+=1
        amount+=1

while selection < 0 or selection > amount:
    selection = input("Select which number database you would like to view: ")
    selection = int(selection) - 1

i = 0
for root, dir, file in os.walk(filepath):
    for name in file:
        if name.endswith(".mdb"):
            if selection == i:
                db = MDBParser(name)
            i+=1

tables = db.tables

print("Available tables:")

i = 1
for table in tables:
    print(str(i) + ": " + table)
    i+=1
amount = len(tables)
selection = -1
while selection < 0 or selection > amount:
    selection = input("Select which number table you would like to view: ")
    selection = int(selection) - 1
currentTable = 0
tableLength = 0
i = 0
for table in tables:
    if i == selection:
        currentTable = db.get_table(table)
        break
    i+=1

for row in currentTable:
    tableLength+= 1

selectedRow = 0
scrolling = 0
currentImageName = ""

def on_press(key):
    global scrolling
    global quit
    if key == keyboard.Key.up:
        scrolling = -1
    elif key == keyboard.Key.down:
        scrolling = 1
    elif key == keyboard.Key.right:
        scrolling = 5
    elif key == keyboard.Key.left:
            scrolling = -5
    elif key == keyboard.Key.esc:
        quit()
def on_release(key):
    global scrolling
    if key == keyboard.Key.up:
        scrolling = 0
    elif key == keyboard.Key.down:
        scrolling = 0
    elif key == keyboard.Key.right:
        scrolling = 0
    elif key == keyboard.Key.left:
        scrolling = 0

def indexTable(index):
    i = 0
    for row in currentTable:
        if i == index:
            return row
        i+=1

def printData(row):
    i = 0
    for element in row:
        if element != "":
            print(str(i) + ": " + element)
        i+= 1

def updateConsole():
    global selectedRow
    selectedRow = clamp(selectedRow)
    clearConsole()
    print("Use arrow keys to scroll | Current Index: " + str(selectedRow) + "/" + str(tableLength) + "\n")
    printData(indexTable(selectedRow))

def clamp(number):
    if number < 0:
        number = 0
    elif number > tableLength - 1:
        number = tableLength - 1
    return number

updateConsole()

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

def Main():
    global selectedRow
    while True:
        time.sleep(.001)
        if scrolling != 0:
            selectedRow += scrolling
            updateConsole()
            time.sleep(.115)
            while scrolling != 0:
                selectedRow+= scrolling
                updateConsole()
                time.sleep(.015)

mainThread = Thread(target=Main)
mainThread.start()

listener.join()
mainThread.join()
