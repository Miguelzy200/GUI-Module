# GUI Module

A simple module that turn easier gui creation with pygame.

## About this project

This project was created to practice modules development using POO and apply Data Structure and Algorithms concepts, such as Queues. Also meant to integrate this module in future projects.

So far, the module has this widgets avialable:
- 'Frame'
- 'Text'
- 'Button'
- 'Image'

This repository also contains **examples of usage (examples/)**, including a real application on a led controller which uses an arduino and serial communication to turn the led on/off.

## Requirements

- Python 3.x
- Pygame
- PySerial

## Install

### Clone the repository
```bash
git clone
cd GUI-Module
```

### Create and active a virtual enviroment
```bash
python -m venv venv
venv/Scripts/Activate
```

### Install dependences
```bash
pip install -r requirements.txt
```

## Usage

```py
import pygame
from pygame.locals import *
from sys import exit
from widgets import Button

pygame.init()
display = pygame.display.set_mode((800,800))

button = Button(
    pos=(100,200),
    size=(180, 90),
    label="Ping"
)

def on_click(button):
    print("Pong!")

button.callback(on_click)

while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            exit()
        button.event_handler(event)
    
    button.draw(display)
    pygame.display.flip()
```

## Widgets

### Frame
A container that group other widgets
```py
Frame(
    pos=(100,100)
    size=(300,200)
)

Frame.add_content(
    Button(
        pos=(10,10)
    )
)
```

### Text
Render a text on screen, can be modified (text color, text size, background color...)
```py
Text(
    pos=(10,10),
    label="Your text here"
)
```

### Button
Create an interactive button which accepts custom functions as callback.
```py
Button(
    pos=(10,10),
    label="Click me",
    color=(220,80,80)
)
```

### Image
Render an image on screen, can be (proportional or not) resized.
```py
Image(
    pos= (10,10),
    size=(200,50),
    proportional_scale=True
)
```

## Examples

### /Simple Use
Basic application of the widgets, includes a timer and a click counter.

### /Arduino Control
An interface, created with the module, that allows turn on/off a leds in an arduino circuit via serial communication. The application send commands to the arduino which decides either turn on or turn off the led, then return a message. It also contains the arduino code.

## Status: In development

> This is the very first version of the project, many features will be add on...

## License

MIT License