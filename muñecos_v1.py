#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pygame
import sys
import os
import random

class TextBox:
    def __init__(self, font, color, rect, text_position):
        self.font = font
        self.color = color
        self.rect = rect
        self.players = []  # Lista para almacenar los nombres y coordenadas de los personajes
        self.text_position = text_position
        self.active = False
        self.text = ''

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                player_name = self.text
                player_x = -100
                player_y = 540
                self.players.append((player_name, player_x, player_y))  # Agrega el nombre y las coordenadas a la lista
                self.text = ''
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def draw_players(self, screen):
        for player_name, player_x, player_y, player_image in self.players:
            text_surface = self.font.render(player_name, True, self.color)
            screen.blit(text_surface, (player_x + 10, player_y - 20))
            screen.blit(player_image, (player_x, player_y))  # Dibuja el personaje junto al nombre
           
def coor_random(x_random, y_random, x_max, x_min, y_max, y_min): 
    '''Devuelve coordenada random dentro de los limites marcados'''
    x_random = random.randint(x_min, x_max)
    y_random = random.randint(y_min, y_max)
    
    return x_random, y_random
        
def move(x, y, x_random, y_random):
    '''Mueve el personaje un píxel hacia la coordenada de destino'''
    if x < x_random:
        x += 1
    elif x > x_random:
        x -= 1
    if y < y_random:
        y += 1
    elif y > y_random:
        y -= 1  
    
    return x, y

# Inicializa pygame
pygame.init()

# Crea la ventana
screen = pygame.display.set_mode((650, 650))

# Titulo de la ventana
pygame.display.set_caption("Consome Panchi")


# Carga el icono y lo pone en la ventana
path_icon = "./icon/"
icon = pygame.image.load(path_icon + "icon.gif").convert()
pygame.display.set_icon(icon)

# Carga el fondo y lo pone en la ventana
path_bg = "./bg/"
background = pygame.image.load(path_bg + "background.gif").convert()
player_control = 0

# Carga de player primario
x_random, y_random = 260, 210
x, y = 260, 210 
epsilon = 1
player_principal = pygame.image.load("./personaje_principal/panchi.gif").convert()
player_dimension_principal = pygame.transform.scale(player_principal, (100, 100))

# Carga de player secundario
path_images = "./images/"
rutas = os.listdir(path_images)
player = pygame.image.load(path_images + rutas[player_control])
player_dimension = pygame.transform.scale(player, (100,100))

clock = pygame.time.Clock()
fps = 100
red = (255,0,0)
green = (37, 211, 102)
running = True

# Crea un objeto de texto
font = pygame.font.Font(None, 36)  # Fuente predeterminada con tamaño 36

# Posición del texto en la ventana
text_position = (screen.get_width() - 10, 10)  # Ajusta la posición según sea necesario

# Crea un objeto TextBox
textbox = TextBox(font, red, pygame.Rect(10, 10, 200, 40), text_position)

# Rango de movimiento del primer personaje
x_min_principal = 200
x_max_principal = 330
y_min_principal = 150
y_max_principal = 230

# Rango de los siguientes personajes
x_min = 20
x_max = 580
y_min = 450
y_max = 545

# Inicializar las coordenadas de destino para cada personaje
player_destinations = [(random.randint(x_min, x_max), random.randint(y_min, y_max)) for _ in range(10)]

while running:
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()       
            sys.exit()  
        textbox.handle_event(event)   

        # Manejo de clics del mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Verifica si se hizo clic con el botón izquierdo
                # Comprueba si el clic fue dentro del área de algún personaje
                for i, (player_name, player_x, player_y, _) in enumerate(textbox.players):
                    if player_x <= event.pos[0] <= player_x + 100 and player_y <= event.pos[1] <= player_y + 100:
                        if player_control >= len(rutas):
                            player_control = 0
                        # Se actualizan las imagenes por si se han metido mas en la carpeta
                        path_images = "./images/"
                        rutas = os.listdir(path_images)
                        # Cambia la imagen del personaje haciendo una sustitución en la lista de jugadores                        
                        player = pygame.image.load(path_images+rutas[player_control])                        
                        player_dimension = pygame.transform.scale(player, (100,100))
                        textbox.players[i] = (player_name, player_x, player_y, player_dimension)
                        player_control += 1
                        break

    # Blit del fondo en la ventana  
    screen.blit(background, (-200,-200))
    
    # Blit del player en la ventana
    screen.blit(player_dimension_principal, (x, y)) 
    
    # Si el personaje ha llegado a su destino, elige una nueva coordenada aleatoria
    if abs(x - x_random) < epsilon and abs(y - y_random) < epsilon:
        x_random, y_random = coor_random(x_random, y_random, x_max_principal, x_min_principal, y_max_principal, y_min_principal)
        
    # Movimiento del personaje principal
    x, y = move(x, y, x_random, y_random) 

    
    # Movimiento de los personajes secundarios
    for i in range(len(textbox.players)):
        player_name, player_x, player_y = textbox.players[i][:3]  # Ignora la nueva imagen del jugador
        player_dest_x, player_dest_y = player_destinations[i]
        
        # Si el personaje ha llegado a su destino, elige una nueva coordenada aleatoria
        if abs(player_x - player_dest_x) < epsilon and abs(player_y - player_dest_y) < epsilon:
            player_dest_x, player_dest_y = coor_random(x_random, y_random, x_max, x_min, y_max, y_min)
            player_destinations[i] = (player_dest_x, player_dest_y)
        
        # Mueve el personaje un píxel hacia la coordenada de destino        
        player_x, player_y = move(player_x, player_y, player_dest_x, player_dest_y)
        
        # Verifica si ya hay una imagen del jugador en la tupla antes de intentar acceder a ella
        if len(textbox.players[i]) > 3:
            textbox.players[i] = (player_name, player_x, player_y, textbox.players[i][3])  # Mantén la imagen del jugador
        else:
            # Si no hay imagen del jugador, simplemente agrega la nueva tupla sin modificarla
            textbox.players[i] = (player_name, player_x, player_y, player_dimension)

    
    # Dibuja los jugadores y sus nombres
    textbox.draw_players(screen)
    
    # Dibuja el textbox en la pantalla
    textbox.draw(screen)
    
    pygame.display.update()

    clock.tick(fps)  # limits FPS to 60