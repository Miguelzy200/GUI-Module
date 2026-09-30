import pygame
from pygame.locals import *
import os.path
from collections.abc import Callable

def _org_position(pos:tuple[int,int], size:tuple[int,int], center:bool):
    new_pos = pos
    if center: new_pos = (new_pos[0]-size[0]/2, new_pos[1]-size[1]/2)
    if pos[0] < 0: new_pos = (0, new_pos[1])
    if pos[1] < 0: new_pos = (new_pos[0], 0)
    return new_pos

def _in_parent(ctr_pos:tuple[int,int], ctr_size:tuple[int,int], pos:tuple[int,int], size:tuple[int,int]):
    if (ctr_pos[0]+ctr_size[0] > pos[0]+size[0]) or (ctr_pos[1]+ctr_size[1] > pos[1]+size[1]):
        return False
    return True

def _check_path(path:str):
    return os.path.exists(path)

def _img_processing(image:pygame.Surface, image_size:tuple[int,int], size:tuple[int,int], prop_scale:bool):
    processed_img = image
    if prop_scale:
        axis = 0
        if size[1] > size[0]: axis = 1
        proportion = size[axis] / image_size[axis]
        processed_img = pygame.transform.smoothscale_by(processed_img, proportion)
    else: processed_img = pygame.transform.scale(processed_img, size)
    return processed_img

class Widget:
    def __init__(self, pos: tuple[int,int]): self.pos = pos
    def add_offset(self, offset:tuple[int,int]): pass
    def event_handler(self, event:pygame.event.Event): pass
    def draw(self, display:pygame.display): pass


class Frame(Widget):
    def __init__(self, 
                pos: tuple[int,int], 
                size:tuple[int,int], 
                color: tuple[int,int,int] = (255,255,255), 
                center:bool = False):
        self.content = list()
        self.pos = _org_position(pos, size, center)
        self.size = size
        self.color = color

    def add_content(self, widget: Widget):
        widget.add_offset(self.pos)
        self.content.append(widget)

    def event_handler(self, event):
        for content in self.content:
            content.event_handler(event)

    def draw(self, screen):
        pygame.draw.rect(
            screen, 
            self.color, 
            (self.pos[0], self.pos[1], self.size[0], self.size[1])
        )
        for content in self.content: 
            if _in_parent(content.pos, content.size, self.pos, self.size):
                content.draw(screen)


class Button(Widget):
    def __init__(self, 
                pos:tuple[int,int], 
                size:tuple[int,int] = (200,80), 
                label:str = "Clique aqui!", 
                text_size:int = 24, 
                text_color:tuple[int,int,int] = (50,50,50), 
                button_color:tuple[int,int,int] = (200,80,50), 
                locked:bool = False,
                center: bool = False):
        self.pos = _org_position(pos, size, center)
        self.size = size
        self.button_color = button_color
        self.label = label
        self.text_size = text_size
        self.text_color = text_color
        self.locked = locked
        self.center = center
        self.__offset = (0,0)
        self.__font = pygame.font.SysFont("arial", text_size, True)
        self.__text_render = self.__font.render(label, True, text_color)
        self.__prev = button_color
        self.__hover = False
        self.__button_rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.__text_rect = self.__text_render.get_rect()
        self.__text_rect.center = self.__button_rect.center
        self.__callback_func = None

    def add_offset(self, offset:tuple[int,int]):
        self.pos = (self.pos[0]+offset[0], self.pos[1]+offset[1])
        self.__offset = offset
        self.__button_rect.topleft = self.pos
        self.__text_rect.center = self.__button_rect.center

    def upd_button(self,
                pos:tuple[int,int] = None, 
                size:tuple[int,int] = None, 
                label:str = None, 
                text_size:int = None, 
                text_color:tuple[int,int,int] = None, 
                button_color:tuple[int,int,int] = None, 
                locked:bool = None,
                center:bool = None):
        if size != None: self.size = size
        if label != None: self.label = label
        if text_size != None: self.text_size = text_size
        if text_color != None: self.text_color = text_color
        if button_color != None: self.button_color = button_color
        if locked != None: self.locked = locked
        if center != None: self.center = center
        if pos != None: self.pos = _org_position((pos[0]+self.__offset[0], pos[1]+self.__offset[1]), self.size, self.center)
        self.__button_rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.__font = pygame.font.SysFont("arial", self.text_size, True)
        self.__text_render = self.__font.render(self.label, True, self.text_color)
        self.__text_rect = self.__text_render.get_rect()
        self.__text_rect.center = self.__button_rect.center
            
    def event_handler(self, event:pygame.event.Event):
        if event.type == MOUSEMOTION:
            if self.__button_rect.collidepoint(event.pos) and not self.__hover:
                self.__prev = self.button_color
                self.button_color = (
                    self.button_color[0] - (150*((self.button_color[0]/255)**3)), 
                    self.button_color[1] - (150*((self.button_color[1]/255)**3)), 
                    self.button_color[2] - (150*((self.button_color[2]/255)**3))
                )
                self.__hover = True
            elif not self.__button_rect.collidepoint(event.pos) and self.__hover:
                self.button_color = self.__prev
                self.__hover = False

        if event.type == MOUSEBUTTONDOWN:
            if not self.locked and self.__button_rect.collidepoint(event.pos):
                if self.__callback_func != None: self.__callback_func(self)

    def callback(self, callback_func: Callable):
        self.__callback_func = callback_func

    def draw(self, display):
        pygame.draw.rect(display, (255,255,255), self.__button_rect)
        pygame.draw.rect(display, self.button_color, (self.pos[0], self.pos[1], self.size[0], self.size[1]))
        display.blit(self.__text_render, self.__text_rect)


class Text(Widget):
    def __init__(self, 
                pos:tuple[int,int], 
                label:str = "Seu texto aqui.", 
                text_color:tuple[int,int,int] = (0,0,0), 
                bg_color:tuple[int,int,int] = None,
                text_font:str = "arial", 
                text_size:int = 24,
                bold:bool = True, 
                italic:bool = False,
                antialias:bool = True,
                center:bool = False):
        self.label = label
        self.text_color = text_color
        self.bg_color = bg_color
        self.text_size = text_size
        self.text_font = pygame.font.SysFont(text_font, text_size, bold, italic)
        self.bold = bold
        self.italic = italic
        self.antialias = antialias
        self.__text_render = self.text_font.render(label, antialias, text_color, bg_color)
        self.size = (self.__text_render.get_width(), self.__text_render.get_height())
        self.pos = _org_position(pos, self.size, center)
        self.size = self.__text_render.get_size()

    def add_offset(self, offset:tuple[int,int]):
        self.pos = (self.pos[0]+offset[0], self.pos[1]+offset[1])

    def upd_text(self, 
                label:str = None, 
                text_color:tuple[int,int,int] = None, 
                bg_color:tuple[int,int,int] = None, 
                text_font:str = None, 
                text_size:int = None,
                bold:bool = None,
                italic:bool = None,
                antialias:bool = None):
        if label!=None: self.label = label
        if text_color!=None: self.text_color = text_color
        if bg_color!=None: self.bg_color = bg_color
        if bold!=None: self.bold = bold
        if italic!=None: self.italic = italic
        if text_size!=None: self.text_size = text_size
        if antialias!=None: self.antialias = antialias
        if text_font!=None: self.text_font = pygame.font.SysFont(text_font, self.text_size, self.bold, self.italic)
        self.__text_render = self.text_font.render(self.label, self.antialias, self.text_color, self.bg_color)
        self.size = self.__text_render.get_size()

    def draw(self, display:pygame.display):
        display.blit(self.__text_render, self.pos)


class Image(Widget):
    def __init__(self, 
                pos:tuple[int,int], 
                path:str,
                size:tuple[int,int] = None, 
                border_width:int = 0, 
                border_color:tuple[int,int,int] = (255,255,255),
                proportional_scale:bool = True,
                visible:bool = True,
                center:bool = False):
        if _check_path(path):
            self.image = pygame.image.load(path)
            if self.image.get_masks()[3] == 0: self.image.convert()
            else: self.image.convert_alpha()
        else: self.image = pygame.Surface((1,1))
        if size: self.image = _img_processing(self.image, self.image.get_size(), size, proportional_scale)
        self.image_path = path
        self.size = self.image.get_size()
        self.border_width = border_width
        self.border_color = border_color
        self.proportional_scale = proportional_scale
        self.pos = _org_position(pos, self.size, center)
        self.visible = visible
        self.__image_rect = self.image.get_rect()

    def add_offset(self, offset):
        self.pos = (self.pos[0]+offset[0], self.pos[1]+offset[1])
        self.__image_rect.topleft = self.pos

    def upd_image(self, 
                size:tuple[int,int] = None, 
                border_width:int = None,  
                border_color:tuple[int,int,int] = None, 
                proportional_scale:bool = None, 
                visible:bool = None):
        if border_width!=None: self.border_width = border_width
        if border_color!=None: self.border_color = border_color
        if proportional_scale!=None: self.proportional_scale = proportional_scale
        if visible!=None: self.visible = visible
        if size!=None: 
            self.image = _img_processing(self.image, self.size, size, self.proportional_scale)
            self.size = self.image.get_size()
            self.__image_rect.size = self.size

    def draw(self, display:pygame.display):
        if not self.visible: return
        pygame.draw.rect(
            display,
            self.border_color, (
                self.__image_rect.left-self.border_width,
                self.__image_rect.top-self.border_width,
                self.__image_rect.size[0]+self.border_width*2,
                self.__image_rect.size[1]+self.border_width*2
        ))
        display.blit(self.image, self.__image_rect)