import pygame 
import random
import sys 

# inicia o pygame
pygame.init()

# tela
LARGURA = 400
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Scrolling running")

# FPS
clock = pygame.time.Clock()
FPS = 60

# cores
BRANCO = (255, 255, 255)
ROSA = (255, 105, 180)
MARROM = (150, 75, 0)
AZUL = (0, 120, 255)
VERMELHO = (200, 0, 0)

# fontes pra escrever textos
fonte = pygame.font.SysFont(None, 40)
fonte_maior = pygame.font.SysFont(None, 60)

# mostra o menu
def mostrar_menu():
    botao = pygame.Rect(LARGURA // 2 - 75, ALTURA // 2, 150, 50)

    while True:
        tela.fill(BRANCO)

        # título
        titulo = fonte_maior.render("Scrolling running", True, AZUL)
        tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 150))

        # botão iniciar
        pygame.draw.rect(tela, ROSA, botao)
        texto_botao = fonte.render("Iniciar", True, BRANCO)
        tela.blit(texto_botao, (botao.centerx - texto_botao.get_width() // 2,
                                botao.centery - texto_botao.get_height() // 2))

        # verifica o do mouse
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao.collidepoint(evento.pos):
                    return

        pygame.display.update()
        clock.tick(FPS)

# função principal do jogo
def jogar():
    # personagem
    scrolling = pygame.Rect(180, 500, 40, 40)
    vel_x = 0
    vel_y = 0
    gravidade = 0.7
    pulo = -18

    # plataformas 
    plataformas = []
    plataformas.append(pygame.Rect(LARGURA // 2 - 40, ALTURA - 50, 80, 10))

    # Gera as primeiras plataformas
    y_pos = ALTURA - 100 
    for i in range(5):
        x = random.randint(0, LARGURA - 80)
        y_pos -= random.randint(60, 90)
        if y_pos < 0:
            y_pos = random.randint(20, 50)
        plataformas.append(pygame.Rect(x, y_pos, 80, 10))

    # loop do jogo
    while True:
        clock.tick(FPS)
        tela.fill(BRANCO)

        # eventos do sistema do jogo
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # controles do jogador
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            vel_x = -5
        elif teclas[pygame.K_RIGHT]:
            vel_x = 5
        else:
            vel_x = 0

        scrolling.x += vel_x

        # colisão com a tela
        if scrolling.left < 0:
            scrolling.left = 0
        if scrolling.right > 400:
            scrolling.right = 400

        # gravidade
        vel_y += gravidade
        scrolling.y += vel_y

        # verifica colisão com as plataformas (para pular)
        for plataforma in plataformas:
            if vel_y > 0 and scrolling.colliderect(plataforma):
                if scrolling.bottom <= plataforma.top + vel_y:
                    scrolling.bottom = plataforma.top
                    vel_y = pulo


        if scrolling.y < ALTURA // 3:
            deslocamento = abs(vel_y)
            scrolling.y += deslocamento

            # move todas as plataformas para baixo
            for plataforma in plataformas:
                plataforma.y += deslocamento

            # remove plataformas que saíram da tela
        novas_plataformas = []
        for plataforma in plataformas:
            if plataforma.y < ALTURA:
                novas_plataformas.append(plataforma)
        plataformas = novas_plataformas

        # criação de novas plataformas
        while len(plataformas) < 8:
            y_mais_alta = ALTURA
            for plataforma in plataformas:
                if plataforma.y < y_mais_alta:
                    y_mais_alta = plataforma.y

            y_nova = y_mais_alta - random.randint(60, 90)
            x_nova = random.randint(0, LARGURA - 80)

            nova_plataforma = pygame.Rect(x_nova, y_nova, 80, 10)
            plataformas.append(nova_plataforma)

        # desenha o jogador
        pygame.draw.rect(tela, AZUL, scrolling)

        # desenha as plataformas
        for plataforma in plataformas:
            pygame.draw.rect(tela, MARROM, plataforma)

        # Game Over
        if scrolling.top > ALTURA:
            texto = fonte.render("GAME OVER", True, VERMELHO)
            tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2))
            pygame.display.update()
            pygame.time.wait(2000)
            return

        pygame.display.update()

# loop principal
while True:
    mostrar_menu()
    jogar()

