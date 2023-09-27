import pygame
import sys
import random
import time
from constantes import *

# Inicializa o pygame
pygame.init()

# Define o tamanho da tela
screen = pygame.display.set_mode(screen_size)

# Define o título da janela
pygame.display.set_caption('Jogo da Forca')

# Define o ícone da janela
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)

# Fonte
font = pygame.font.SysFont('arial', 30)
letter_font = pygame.font.SysFont('arial', 60)
title_font = pygame.font.SysFont('arial', 80)

# FPS
clock = pygame.time.Clock()

# Desenha as caixas

row = 2
col = 13
gap = 20
size = 40
boxes = []

for row in range(row):
    for col in range(col):
        x = ((col * gap) + gap) + (col * size)
        y = ((row * gap) + gap) + (row * size) + 330
        box = pygame.Rect(x, y, size, size)
        boxes.append(box)
    
# Cria os botões de A a Z

buttons = []
A = 65

for ind, box in enumerate(boxes):
    letter  = chr(A + ind)
    button = [box, letter]
    buttons.append(button)

def draw_buttons(buttons):
    for box, letter in buttons:
        btn_text = font.render(letter, True, black)
        btn_rect = btn_text.get_rect(center=(box.x + 20, box.y + 20))
        screen.blit(btn_text, btn_rect)
        pygame.draw.rect(screen, black, box, 2)


# Desenha a palavra 
def draw_word(word, guessed):
    display_word = ''
    for letter in word:
        if letter in guessed:
            display_word += letter + ' '
        else:
            display_word += '_ '
            
    text = letter_font.render(display_word, True, black)
    screen.blit(text, (300, 200))


# Número de erros
hangman_status = 0


# Escolhe uma palavra aleatória
word_length = 999 # Número de letras da palavra -> 999 para garantir que o loop vai rodar pelo menos uma vez
while word_length > 12:
    word = random.choice(words).upper()
    word_length = len(word)

guessed = [] # Letras que o jogador já chutou


# Desenha a forca
def draw_hangman(hangman_status):
    if hangman_status<6:
        image = pygame.image.load(f'img/img_{hangman_status}.png')
    else:
        image = pygame.image.load(f'img/img_5.png')
    screen.blit(image, (150, 100))


# Desenha título
title = "FORCA"
title_text = title_font.render(title, True, (0, 0, 0))
title_rect = title_text.get_rect(center=(screen_width // 2, title_text.get_height() // 2 + 10))


# Loop principal do jogo

playing = True # Variável para controlar o loop principal
game_over = False # Variável para controlar o loop de game over

while playing:
    # Preenche a tela com a cor branca
    screen.fill(white)

    # Checar os eventos do mouse aqui:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

        # Checa se o evento é um clique do mouse
        if event.type == pygame.MOUSEBUTTONUP:
            click_pos = pygame.mouse.get_pos()
            # click_pos = event.pos

            # Checa se a letra está correta
            for button, letter in buttons:
                if button.collidepoint(click_pos):
                    if letter not in word:
                        hangman_status += 1
                    if hangman_status == 6:
                        playing = False
                        game_over = True
                    guessed.append(letter)
                    buttons.remove([button, letter])

    # Desenha a forca
    draw_hangman(hangman_status)
    
    for box in boxes:
        pygame.draw.rect(screen, black, box, 2)

    # Verifica se o jogador ganhou
    won = True
    for letter in word:
        if letter not in guessed:
            won = False
    
    if won:
        game_text = title_font.render('Você ganhou!', True, black)
        text_rect = game_text.get_rect(center=(screen_width//2, screen_height//2))
        screen.fill(white)
        screen.blit(game_text, text_rect)
        pygame.display.update() # Atualiza a tela
        time.sleep(2)
        pygame.quit()# Encerra o pygame
        sys.exit() # Encerra o programa
    else:
        game_text = title_font.render('Você perdeu!', True, black)
        word_text = letter_font.render(f'A palavra era {word}', True, black)


    # Desenha os botões
    draw_buttons(buttons)

    # Desenha a palavra
    draw_word(word, guessed)

    # Desenha o título
    screen.blit(title_text, title_rect)

    # 60 frames por segundo
    clock.tick(60)
    pygame.display.update() # Atualiza a tela

    # Mostrando tela de resultado
    if game_over:
        screen.fill(white)
        playing = False
        text_rect = game_text.get_rect(center=(screen_width//2, screen_height//2))
        screen.blit(game_text, text_rect)
        word_rect = word_text.get_rect(center=(screen_width//2, screen_height//2 + 100))
        screen.blit(word_text, word_rect)
        pygame.display.update() # Atualiza a tela
        playing = False
        time.sleep(2)
        pygame.quit()# Encerra o pygame
        sys.exit() # Encerra o programa

pygame.quit()# Encerra o pygame
sys.exit() # Encerra o programa