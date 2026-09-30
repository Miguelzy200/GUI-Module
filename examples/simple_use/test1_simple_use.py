import sys, os # Importing widgets module
pasta_atual = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(pasta_atual, "..", ".."))
sys.path.insert(0, root)

import pygame
from pygame.locals import *
from widgets import *

pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Simulação")

main_frame = Frame(
    (screen.get_width()/2-300, screen.get_height()/2+50),
    (300,500),
    center=True
) 

alt_frame = Frame(
    (screen.get_width()/2+200, screen.get_height()/2+50),
    (600,500),
    center=True
) 

increment_button = Button(
    pos=(50,50),
    label="Subir",
    button_color=(200,250,20)
)

decrement_button = Button(
    pos=(50, 200),
    label="Descer",
    button_color=(20,250,20)
)

click_counter = 0

click_count_text = Text(
    pos = (alt_frame.size[0]/2, alt_frame.size[1]/2+50),
    label = f" Clicks: {click_counter} !!! ",
    text_size=40,
    text_color=(255,255,255),
    bg_color=(50,50,120),
    center = True
)

def aumentar_callback(botao):
    global click_counter
    click_counter += 1
    click_count_text.upd_text(label = f" Clicks: {click_counter} !!! ")
    decrement_button.locked = False

def diminuir_callback(botao):
    global click_counter
    click_counter -= 1
    click_count_text.upd_text(label = f" Clicks: {click_counter} !!! ")

increment_button.callback(aumentar_callback)
decrement_button.callback(diminuir_callback)

main_frame.add_content(increment_button)
main_frame.add_content(decrement_button)
alt_frame.add_content(click_count_text)

main_frame.add_content(Button(
    pos=(50, 350),
    label="Botao 3",
    button_color=(20,100,250)
))

sec_counter = 0
aux = 0

sec_counter_text = Text(
    pos=(alt_frame.size[0]/2, alt_frame.size[1]/2),
    label=f" Contador: {sec_counter} ",
    text_size=40,
    text_color=(255,255,255),
    bg_color=(50,50,120),
    center=True
)
alt_frame.add_content(Text((30,30), label="Ola amigo"))
alt_frame.add_content(sec_counter_text)
alt_frame.add_content(Text((30,130), text_size=10, label="Este é um textinhozinho."))
alt_frame.add_content(Image(
    pos=(alt_frame.size[0]/2, alt_frame.size[1]/2),
    size=(200,200),
    path="gato_pfp.jpg",
    border_width=15,
    border_color=(100,0,0),
    proportional_scale=False,
    center=True,
    visible=False
))

while True:
    for event in pygame.event.get():
        main_frame.event_handler(event)
        alt_frame.event_handler(event)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    aux+=1
    if aux >= 1000:
        aux = 0
        sec_counter+=1
        sec_counter_text.upd_text(label=f" Contador: {sec_counter} ")

    if click_counter == 0: decrement_button.locked = True

    screen.fill((200,240,255))
    alt_frame.draw(screen)
    main_frame.draw(screen)
    
    pygame.display.flip()