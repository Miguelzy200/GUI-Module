import sys, os # Importing widgets module
pasta_atual = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(pasta_atual, "..", ".."))
sys.path.insert(0, root)

import pygame
from pygame.locals import *
from widgets import *
import serial

pygame.init()
display = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("Teste Comunicação Serial")

# --------- Defining log class ---------
class Log(Widget):
    def __init__(self, container:Frame, font:str, text_size:int, start_offset:tuple[int, int] = (0,0), between_lines:int=10):
        self.container = container
        self.offset = start_offset
        self.pos = start_offset
        self.font = font
        self.size = (container.size[0]-start_offset[0], container.size[1]-start_offset[1])
        self.text_size = text_size
        self.log_list = list()
        self.__between_lines = between_lines
        self.__line_height = pygame.font.SysFont(font, text_size).get_height()
        self.__countdown = 0

    def remove_first(self):
        self.log_list.pop(0)
        for t in self.log_list:
            t.pos = (t.pos[0], t.pos[1] - self.__between_lines - self.__line_height)

    def add_last(self, log: str):
        if len(self.log_list) == 0:
            pos = self.pos
        else:
            pos = (self.pos[0], self.log_list[-1].pos[1]+self.__between_lines+self.__line_height)

        if (pos[1]+self.__line_height) >= (self.container.pos[1]+self.container.size[1]): 
            self.remove_first()
            pos = (pos[0], pos[1]-self.__between_lines-self.__line_height)
        
        new_log = Text(
            pos=pos,
            label=log,
            text_font=self.font,
            text_size=self.text_size,
            bold=False
        )

        self.log_list.append(new_log)

    def add_offset(self, offset:tuple[int,int]):
        self.pos = (self.pos[0]+offset[0], self.pos[1]+offset[1])

    def draw(self, display):
        for l in self.log_list: l.draw(display)
        if len(self.log_list) != 0:
            self.__countdown += 1
            if self.__countdown >= 5000: #not actual seconds, this is counting per frame
                self.remove_first()
                self.__countdown = 0


# --------- Creating interface using widgets module ---------
Frames = {
    "caption": Frame(
        pos=(250,50),
        size=(700, 100)
    ), 
    "input": Frame(
        pos=(175, 200),
        size=(350, 450)
    ), 
    "output": Frame(
        pos=(675, 200),
        size=(350, 450)
    ),
    "buttons": Frame(
        pos=(200, 710), 
        size=(800, 140)
    )
}

frame_keys = ["caption", "input", "output", "buttons"]

Frames["caption"].add_content(Text(
    pos=(Frames["caption"].size[0]/2, Frames["caption"].size[1]/2),
    label="Comunicação Serial via Python",
    text_size=36,
    center=True
))

Frames["input"].add_content(Text(
    pos=(Frames["input"].size[0]/2, 30),
    label="--------- Input ---------",
    text_size=32,
    center=True
))
input_log = Log(Frames["input"], "arial", 24, (20,50), 0)
Frames["input"].add_content(input_log)

Frames["output"].add_content(Text(
    pos=(Frames["output"].size[0]/2, 30),
    label="-------- Output --------",
    text_size=32,
    center=True
))
output_log = Log(Frames["output"], "arial", 24, (20,50), 0)
Frames["output"].add_content(output_log)

buttons = [
    Button(
        pos=(Frames["buttons"].size[0]/2-150, Frames["buttons"].size[1]/2 - 35),
        size=(120, 50),
        label="Liga A",
        text_color=(255,255,255),
        button_color=(50, 180, 50),
        text_size=26,
        center=True
    ),
    Button(
        pos=(Frames["buttons"].size[0]/2 + 150, Frames["buttons"].size[1]/2 - 35),
        size=(120, 50),
        label="Desliga A",
        text_color=(255,255,255),
        text_size=26,
        center=True
    ),
    Button(
        pos=(Frames["buttons"].size[0]/2 - 150, Frames["buttons"].size[1]/2 + 35),
        size=(120, 50),
        label="Liga B",
        text_color=(255,255,255),
        button_color=(50, 180, 50),
        text_size=26,
        center=True
        ),
    Button(
        pos=(Frames["buttons"].size[0]/2 + 150, Frames["buttons"].size[1]/2 + 35),
        size=(120, 50),
        label="Desliga B",
        text_color=(255,255,255),
        text_size=26,
        center=True
    ),
]

# --------- Creating serial connection dependences ---------
connection_status = 0
_previous_state = 0
status_translate = [
    "Nao foi possível estabelecer conexão serial",
    "Conexão serial interrompida",
    "Conexão serial OK"
]
status_colors = [
    (255,0,0),
    (255,0,0),
    (20,200,20)
]
serial_port = None

def connect():
    global serial_port, _previous_state, connection_status
    try:
        serial_port = serial.Serial("COM3", 9600, timeout=0.05)
        _previous_state = connection_status
        connection_status = 2
    except:
        _previous_state = connection_status
        connection_status = 0

connect()

def reconnect(button): connect()

def read_bytes():
    global connection_status, _previous_state
    try:
        if serial_port.in_waiting > 0:
            data = serial_port.readline().decode("utf-8", errors="ignore").strip()
            input_log.add_last(f"-> {data}")
    except: 
        _previous_state = connection_status
        connection_status = 1

def send_byte(button: Button):
    global input_log, output_log, serial_port, connection_status, _previous_state
    if connection_status == 2:
        try:
            command_dict = {
                "Liga A": "on_a", 
                "Desliga A": "off_a",
                "Liga B": "on_b",
                "Desliga B": "off_b"
            }
            serial_port.write(f"{command_dict[button.label]}\n".encode("utf-8"))
            output_log.add_last(f"-> {button.label}")
        except: 
            _previous_state = connection_status
            connection_status = 1

for b in buttons:
    b.callback(send_byte)
    Frames["buttons"].add_content(b)

connection_status_text = Text(
    pos=(0,873), 
    label=f" {status_translate[connection_status]} ",
    text_color=status_colors[connection_status],
    bg_color=(255,255,255)
)

reconnect_button = Button(
    pos=(connection_status_text.size[0], connection_status_text.pos[1]),
    size=(180,connection_status_text.size[1]),
    label="Reconectar",
    text_size=20,
    text_color=(255,255,255),
    button_color=(20,20,220),
    locked=False
)
reconnect_button.callback(reconnect)

while True:
    display.fill((180, 180, 250))
    for event in pygame.event.get():
        if event.type == QUIT:
            if connection_status == 2: serial_port.close()
            pygame.quit()
            sys.exit()
        for f in frame_keys:
            Frames[f].event_handler(event)
        reconnect_button.event_handler(event)

    if connection_status == 2: read_bytes()
    else: reconnect_button.draw(display)
    connection_status_text.draw(display)

    if _previous_state!=connection_status:
        _previous_state = connection_status
        if connection_status == 2: reconnect_button.upd_button(locked=True)
        else: reconnect_button.upd_button(locked=False)
        connection_status_text.upd_text(
            label=f" {status_translate[connection_status]} ",
            text_color=status_colors[connection_status]
        )
        reconnect_button.upd_button(pos=(
            connection_status_text.size[0],
            connection_status_text.pos[1]
        ))

    for f in frame_keys:
        Frames[f].draw(display)

    pygame.display.flip()