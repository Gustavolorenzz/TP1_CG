#  Trabalho Pratico 1 - Computação Gráfica
#  Aluno: Gustavo Lorenzo
#  Date: 2025-03-23
"""Este código define uma interface gráfica usando Pygame para desenhar e manipular formas.
Inclui funcionalidades para desenhar linhas e círculos, selecionar e transformar formas,
e aplicar algoritmos de recorte (Cohen-Sutherland e Liang-Barsky) às formas.

A classe Interface inicializa a janela do Pygame e configura vários atributos para desenhar e manipular formas.
Inclui métodos para desenhar linhas e círculos, selecionar formas, rotacionar, transladar, escalar e refletir formas.
Também inclui métodos para definir e aplicar janelas de recorte usando os algoritmos Cohen-Sutherland e Liang-Barsky.

A classe Botao define botões para a interface, permitindo ao usuário selecionar diferentes modos de desenho e transformação.
A classe CampoTexto define campos de entrada de texto para inserir valores para transformações.
A classe Circulo define um círculo e inclui um método para desenhar o círculo usando simetria.
A classe Reta define uma linha e inclui métodos para desenhar a linha usando os algoritmos de Bresenham e DDA.
A classe ClippingWindow define uma janela de recorte e inclui métodos para aplicar os algoritmos de recorte Cohen-Sutherland e Liang-Barsky.

A função principal inicializa a classe Interface e inicia o loop de eventos do Pygame."""

import pygame
import sys
import numpy as np

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (200, 200, 200)

class Interface:
    #definições de variáveis iniciais
    def __init__(self):
        #inicializa a janela do Pygame
        pygame.init()
        pygame.display.set_caption("Paint")
        self.width, self.height = 800, 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill(WHITE)
        self.font = pygame.font.SysFont('Arial', 20)
        self.loop = True
        #vetor de pontos para desenhar a reta
        self.meu_vetor = []
        #vetor que armazena os poligono(meu_vetor) em si
        self.estrutura = []
        #vetor que armazena o tipo de poligonos (retaDDA, retaBresenham ou círculos)
        self.poligonos = []
        self.cor = RED
        #variável para armazenar o poligono que será desenhado(reta ou circulo)
        self.poligono = ""
        #variável para armazenar o algoritmo que será utilizado(DDA ou Bresenham)
        self.modo_atual = ""
        #variáveis para seleção de objetos
        self.state = False
        self.selecao_inicio = None
        self.obj_selected = []
        self.operacao = ""
        #variáveis para janela
        self.clipping_window = ClippingWindow()
        self.defining_clip_window = False
        self.clipping_algorithm = "cohen_sutherland" 
        self.clipped_estrutura = []
        self.clipped_poligonos = []
        self.clipping_applied = False
        #campos de texto para entrada de valores
        self.rotation_field = CampoTexto(170, 520, 60, 30, "Ângulo")
        self.translate_x_field = CampoTexto(170, 560, 60, 30, "X")
        self.translate_y_field = CampoTexto(240, 560, 60, 30, "Y")
        self.scale_x_field = CampoTexto(170, 600, 60, 30, "X")
        self.scale_y_field = CampoTexto(240, 600, 60, 30, "Y")

        self.labels = {
            "rotation": self.font.render("Ângulo:", True, BLACK),
            "translate": self.font.render("Translação:", True, BLACK),
            "scale": self.font.render("Escala:", True, BLACK)
    }

    
    

    def desenhar_reta(self):
        # Será chamado quando o botão "Reta" for clicado
        if not self.state:
            print("Modo: Reta selecionado")
            self.poligono = "reta"

    def desenhar_circulo(self):
        # Será chamado quando o botão "Círculo" for clicado
        if not self.state:
            print("Modo: Círculo selecionado")
            self.poligono = "circulo"
        
    def modo_dda(self):
        # Será chamado quando o botão "DDA" for clicado
        if not self.state:
            print("Algoritmo: DDA selecionado")
            self.modo_atual = "DDA"
        
    def modo_bresenham(self):
        # Será chamado quando o botão "Bresenham" for clicado
        if not self.state:
            print("Algoritmo: Bresenham selecionado")
            self.modo_atual = "Bresenham"
    
    #altera o modo de seleção
    def modo_selecao(self):
        self.state = not self.state
        if self.state:
            print("Modo: Seleção selecionado")
            self.selecao_inicio = None
            self.obj_selected = []
            self.poligono = ""
        else:
            print("Modo: Seleção desativado")
            self.clipping_applied = False
            self.screen.fill(WHITE)
            self.obj_selected = []
            # Reset clipping window state if needed
            if not self.defining_clip_window:
                self.clipping_window.active = False
                self.clipping_window = ClippingWindow()
                self.redesenhar_tela()

    #rotaciona o poligono selecionado
    def rotacionar(self):
        if self.state and len(self.obj_selected) > 0:
            print("Modo: rotacao selecionado")
            try:
                angulo = int(self.rotation_field.get_value())
                print(f"Rotating by angle={angulo}")
                for i in self.obj_selected:
                    estrutura = self.estrutura[i]
                    for j in range(len(estrutura)):
                        x, y = estrutura[j]
                        x -= estrutura[0][0]
                        y -= estrutura[0][1]
                        x_novo = int(x*np.cos(np.radians(angulo)) - y*np.sin(np.radians(angulo)))
                        y_novo = int(x*np.sin(np.radians(angulo)) + y*np.cos(np.radians(angulo)))
                        estrutura[j] = (x_novo + estrutura[0][0], y_novo + estrutura[0][1])
                self.redesenhar_tela()
            except ValueError:
                print("Valor inválido para rotação")
            self.poligono = ""
    #translada o poligono selecionado
    #POR ALGUM MOTIVO, NÃO CONSEGUI CHAMAR O HANDLE_EVENT PARA A TRANSLAÇÃO, TIVE QUE JOGAR O CODIGO AQUI
    #(aparentemente estava dando problema do input K_EVENT estar sendo obrigatório) -> deu certo :)
    def transladar(self):
        if self.state and len(self.obj_selected) > 0:
            print("Modo: translacao selecionado")
            try:
                dx = int(np.round(self.translate_x_field.get_value()))
                dy = int(np.round(self.translate_y_field.get_value()))
                print(f"Translating by dx={dx}, dy={dy}")

                for i in self.obj_selected:
                    estrutura = self.estrutura[i]
                    for j in range(len(estrutura)):
                        estrutura[j] = (estrutura[j][0] + dx, estrutura[j][1] + dy)
                self.redesenhar_tela() 
            except ValueError:
                print("Valores inválidos para translação") 
            self.poligono = ""
    #escala o poligono selecionado
    def escalar(self):
        if self.state and len(self.obj_selected) > 0:
            try:
                print("Modo: escala selecionado")
                sx = float(self.scale_x_field.get_value())
                sy = float(self.scale_y_field.get_value())
                print(f"Scaling by sx={sx}, sy={sy}")
                if sx != 0 and sy != 0:
                    for i in self.obj_selected:
                        estrutura = self.estrutura[i]
                        for j in range(len(estrutura)):
                            x, y = estrutura[j]
                            x -= estrutura[0][0]
                            y -= estrutura[0][1]
                            x_novo = int(np.round(x*sx))
                            y_novo = int(np.round(y*sy))
                            estrutura[j] = (x_novo + estrutura[0][0], y_novo + estrutura[0][1])
                    self.redesenhar_tela()
                else:
                    print("Valores de escala não podem ser 0")
            except ValueError:
                print("Valores inválidos para escala")
            self.poligono = ""
    #reflete o poligono selecionado no eixo X
    def refletirX(self):
        if self.state and len(self.obj_selected) > 0:
            self.operacao = "refletirX"
            print("Modo: refletirX selecionado")
    #reflete o poligono selecionado no eixo Y
    def refletirY(self):
        if self.state and len(self.obj_selected) > 0:
            self.operacao = "refletirY"
            print("Modo: refletirY selecionado")
    #reflete o poligono selecionado no eixo X e Y
    def refletirXY(self):
        if self.state  and len(self.obj_selected) > 0:
            self.operacao = "refletirXY"
            print("Modo: refletirXY selecionado")

    #função para definir a janela de recorte
    def definir_janela_recorte(self):
        """Inicia o modo de definição da janela de recorte."""
        self.defining_clip_window = True
        self.meu_vetor = []
        print("Modo: Definir janela de recorte selecionado")
        print("Clique para definir os cantos da janela de recorte")

    def usar_cohen_sutherland(self):
        """Define o algoritmo de Cohen-Sutherland como o algoritmo de recorte a ser usado."""
        self.clipping_algorithm = "cohen_sutherland"
        print("Algoritmo de recorte: Cohen-Sutherland selecionado")

    def usar_liang_barsky(self):
        """Define o algoritmo de Liang-Barsky como o algoritmo de recorte a ser usado."""
        self.clipping_algorithm = "liang_barsky"
        print("Algoritmo de recorte: Liang-Barsky selecionado")

    def aplicar_recorte(self):
        if not self.clipping_window.active:
            print("Primeiro defina uma janela de recorte")
            return
        
        # Criar listas para armazenar os objetos recortados
        self.clipped_estrutura = []
        self.clipped_poligonos = []
        
        # Processar todas as retas
        for i, pontos in enumerate(self.estrutura):
            if self.poligonos[i] in ["retaDDA", "retaBresenham"]:
                tipo = self.poligonos[i]
                
                # Criar um novo conjunto de pontos para o polígono recortado
                clipped_pontos = []
                
                # Processar cada segmento de linha do polígono
                for j in range(len(pontos)):
                    x1, y1 = pontos[j]
                    if j == len(pontos) - 1:
                        x2, y2 = pontos[0]
                    else:
                        x2, y2 = pontos[j + 1]
                    
                    # Aplicar algoritmo de recorte selecionado
                    if self.clipping_algorithm == "cohen_sutherland":
                        visible, coords = self.clipping_window.cohen_sutherland(x1, y1, x2, y2)
                    else:  # liang_barsky
                        visible, coords = self.clipping_window.liang_barsky(x1, y1, x2, y2)
                    
                    # Se a linha estiver visível, adicionar ao novo polígono
                    if visible and coords:
                        nx1, ny1, nx2, ny2 = coords
                        
                        # Se este é o primeiro ponto ou diferente do último adicionado
                        if not clipped_pontos or (nx1, ny1) != clipped_pontos[-1]:
                            clipped_pontos.append((nx1, ny1))
                        
                        clipped_pontos.append((nx2, ny2))
                
                # Se o polígono tiver pontos suficientes, adicionar à nova estrutura
                if len(clipped_pontos) >= 2:
                    self.clipped_estrutura.append(clipped_pontos)
                    self.clipped_poligonos.append(tipo)
            
            elif self.poligonos[i] == "circulo":
                # Manter círculos inalterados por enquanto
                self.clipped_estrutura.append(pontos)
                self.clipped_poligonos.append("circulo")
        
        self.clipping_applied = True
        
        # Redesenhar a tela com os objetos recortados
        self.redesenhar_tela()
        
        print(f"Recorte aplicado usando algoritmo {self.clipping_algorithm}")   

    #o handle event serve para as alterações que acontecem quando se aperta um botão
    def handle_event(self):
        if self.modo_atual == "DDA"  and self.poligono == "reta":
            if len(self.meu_vetor) > 1:
                for i in range(len(self.meu_vetor) - 1):
                    x1, y1 = self.meu_vetor[i]
                    x2, y2 = self.meu_vetor[i + 1]
                    reta = Reta(x1, y1, x2, y2)
                    reta.drawDDA(self.screen, self.cor)
                if len(self.meu_vetor) > 2:    
                    reta = Reta(self.meu_vetor[-1][0], self.meu_vetor[-1][1], self.meu_vetor[0][0], self.meu_vetor[0][1])
                    reta.drawDDA(self.screen, self.cor)
                self.estrutura.append(self.meu_vetor)
                self.poligonos.append("retaDDA")
                self.meu_vetor = []
            else:
                print("É necessário ter mais de 1 ponto para desenhar uma reta")
        elif self.modo_atual == "Bresenham" and self.poligono == "reta":
            if len(self.meu_vetor) > 1:
                for i in range(len(self.meu_vetor) - 1):
                    x1, y1 = self.meu_vetor[i]
                    x2, y2 = self.meu_vetor[i + 1]
                    reta = Reta(x1, y1, x2, y2)
                    reta.drawBreseham(self.screen, self.cor)
                if len(self.meu_vetor) > 2:
                    reta = Reta(self.meu_vetor[-1][0], self.meu_vetor[-1][1], self.meu_vetor[0][0], self.meu_vetor[0][1])
                    reta.drawBreseham(self.screen, self.cor)
                self.estrutura.append(self.meu_vetor)
                self.poligonos.append("retaBresenham")
                self.meu_vetor = []
            else:
                print("É necessário ter mais de 1 ponto para desenhar uma reta")
        elif self.poligono == "circulo":
            if len(self.meu_vetor) == 2:
                x1, y1 = self.meu_vetor[0]
                x2, y2 = self.meu_vetor[1]
                circulo = Circulo(x1, x2, y1, y2)
                circulo.draw(self.screen, self.cor)
                self.estrutura.append(self.meu_vetor)
                self.poligonos.append("circulo")
                self.meu_vetor = []
            else:
                print("É necessário ter apenas 2 pontos para desenhar um círculo")
        #operação de refletir no eixo X
        elif self.state and self.operacao == "refletirX":
            for i in self.obj_selected:
                if not(self.poligonos[i] == "circulo"):
                    estrutura = self.estrutura[i]
                    for j in range(len(estrutura)):
                        estrutura[j] = (estrutura[j][0],2*estrutura[0][1]- estrutura[j][1])
            self.redesenhar_tela()
        #operação de refletir no eixo Y
        elif self.state and self.operacao == "refletirY" and len(self.obj_selected) > 0:
            for i in self.obj_selected:
                if not(self.poligonos[i] == "circulo"):
                    estrutura = self.estrutura[i]
                    for j in range(len(estrutura)):
                        estrutura[j] = (2*estrutura[0][0]- estrutura[j][0], estrutura[j][1])
            self.redesenhar_tela()
        #operação de refletir no eixo X e Y
        elif self.state and self.operacao == "refletirXY" and len(self.obj_selected) > 0:
            for i in self.obj_selected:
                if not(self.poligonos[i] == "circulo"):
                    estrutura = self.estrutura[i]
                    for j in range(len(estrutura)):
                        estrutura[j] = (2*estrutura[0][0]- estrutura[j][0], 2*estrutura[0][1]- estrutura[j][1])
            self.redesenhar_tela() 
        
               
        self.poligono = ""
        self.operacao = ""
    
    #os pontos inicial e final da seleção precisam estar em ordem, do superior esquerdo para o inferior direito
    def verificar_selecao(self, x1, y1, x2, y2):
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        
        self.obj_selected = []
        #verifica os objetos que possuem pontos dentro da área de seleção
        for i, estrutura in enumerate(self.estrutura):
            for x, y in estrutura:
                if x1 <= x <= x2 and y1 <= y <= y2:
                    self.obj_selected.append(i)
                    break
        print(f"Objetos selecionados: {self.obj_selected}")
        self.redesenhar_tela()


    def resetar_recorte(self):
        """Reseta o recorte aplicado e volta para a visualização original."""
        self.clipping_applied = False
        self.redesenhar_tela()
        print("Recorte resetado")


    def redesenhar_tela(self):
        # Limpa a tela
        self.screen.fill(WHITE)

        # Desenhar a janela de recorte, se estiver ativa
        if self.clipping_window.active and (self.state or self.defining_clip_window):
            self.clipping_window.draw(self.screen, GREEN)

        # Determinar qual estrutura de dados usar
        estrutura_to_use = self.clipped_estrutura if self.clipping_applied else self.estrutura
        poligonos_to_use = self.clipped_poligonos if self.clipping_applied else self.poligonos

        for i, pontos in enumerate(estrutura_to_use):
            if i >= len(poligonos_to_use):
                continue  # Proteger contra índices inválidos
                
            cor = BLUE if i in self.obj_selected else RED
            tipo = poligonos_to_use[i]
            
            # Desenhar os pontos para todos os objetos
            for ponto in pontos:
                pygame.draw.circle(self.screen, cor, ponto, 3)
            
            if tipo == "retaDDA":
                for j in range(len(pontos) - 1):
                    x1, y1 = pontos[j]
                    x2, y2 = pontos[j + 1]
                    reta = Reta(x1, y1, x2, y2)
                    reta.drawDDA(self.screen, cor)
                if len(pontos) > 2:
                    reta = Reta(pontos[-1][0], pontos[-1][1], pontos[0][0], pontos[0][1])
                    reta.drawDDA(self.screen, cor)
            
            elif tipo == "retaBresenham":
                for j in range(len(pontos) - 1):
                    x1, y1 = pontos[j]
                    x2, y2 = pontos[j + 1]
                    reta = Reta(x1, y1, x2, y2)
                    reta.drawBreseham(self.screen, cor)
                if len(pontos) > 2:
                    reta = Reta(pontos[-1][0], pontos[-1][1], pontos[0][0], pontos[0][1])
                    reta.drawBreseham(self.screen, cor)
            
            elif tipo == "circulo":
                x1, y1 = pontos[0]
                x2, y2 = pontos[1]
                circulo = Circulo(x1, x2, y1, y2)
                circulo.draw(self.screen, cor)

    def draw_input_fields(self):
        # Desenha os campos de texto e seus labels
        
        # Rotação
        self.screen.blit(self.labels["rotation"], (10, 530))
        self.rotation_field.draw(self.screen)
        
        # Translação
        self.screen.blit(self.labels["translate"], (10, 570))
        self.translate_x_field.draw(self.screen)
        self.translate_y_field.draw(self.screen)
        
        # Escala
        self.screen.blit(self.labels["scale"], (10, 610))
        self.scale_x_field.draw(self.screen)
        self.scale_y_field.draw(self.screen)

    def inicialize_tela(self):
        #adiciona os botoes
        botao = Botao(10, 10, 150, 30, GRAY, 
                 ["Reta", "Circunferência", "DDA", "Bresenham", "Selecionar", 
                  "Rotacionar", "Transladar", "Escalar", "Refletir X", "Refletir Y", 
                  "Refletir XY", "Definir Recorte", "Cohen-Sutherland", "Liang-Barsky", "Aplicar Recorte"],
                 [self.desenhar_reta, self.desenhar_circulo, self.modo_dda, 
                  self.modo_bresenham, self.modo_selecao, self.rotacionar, 
                  self.transladar, self.escalar, self.refletirX, self.refletirY, 
                  self.refletirXY, self.definir_janela_recorte, self.usar_cohen_sutherland, 
                  self.usar_liang_barsky, self.aplicar_recorte])
        while self.loop:
            for event in pygame.event.get():
                #fecha a janela
                if event.type == pygame.QUIT:
                    m=0
                    #imprime os poligonos e seus pontos(verificação de funcionamento) -> para testes :)
                    for estrutura in self.estrutura:
                        for i, j in estrutura:
                            print(i, j)
                        print(self.poligonos[m])
                        m+=1
                        print("-----")  #separador entre elementos de self.estrutura
                    self.loop = False
                
                
                text_field_handled = False
                #verifica se o campo de texto foi clicado
                if self.state:
                    if self.rotation_field.handle_event(event):
                        text_field_handled = True
                    elif self.translate_x_field.handle_event(event):
                        text_field_handled = True
                    elif self.translate_y_field.handle_event(event):
                        text_field_handled = True
                    elif self.scale_x_field.handle_event(event):
                        text_field_handled = True
                    elif self.scale_y_field.handle_event(event):
                        text_field_handled = True
                #se o campo de texto foi clicado, não processa o evento de clique do mouse
                if text_field_handled:
                    continue

                

                #adiciona um ponto ao vetor de pontos
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if botao.handle_event(event, self.state):
                        if self.defining_clip_window:
                            x,y = pygame.mouse.get_pos()
                            pygame.draw.circle(self.screen, GREEN, (x, y), 3)
                            self.meu_vetor.append((x, y))
                            print(f"Ponto de recorte adicionado: {x}, {y}")
                            
                            # Se tiver 2 pontos, define a janela de recorte
                            if len(self.meu_vetor) == 2:

                                x1, y1 = self.meu_vetor[0]
                                x2, y2 = self.meu_vetor[1]
                                self.clipping_window.set_coordinates(
                                    min(x1, x2), min(y1, y2),
                                    max(x1, x2), max(y1, y2)
                                )
                                self.clipping_window.active = True
                                self.defining_clip_window = False
                                self.meu_vetor = []
                                self.redesenhar_tela()
                                print("Janela de recorte definida")

                        #modo normal
                        if not self.state:
                            x, y = pygame.mouse.get_pos()
                            pygame.draw.circle(self.screen, RED, (x, y), 3)
                            self.meu_vetor.append((x, y))
                            print(f"Ponto adicionado:{x}, {y}")
                        else:
                            self.selecao_inicio = pygame.mouse.get_pos()
                    else:
                        if not self.state:
                            self.handle_event()
                        else:
                            # Chama a função de refletir se o estado estiver ativo
                            if self.operacao in ["refletirX", "refletirY", "refletirXY"]:
                                if event.type == pygame.KEYDOWN and self.state and len(self.obj_selected) > 0:
                                    if self.operacao == "rotacionar":
                                        self.handle_event()
                                    elif self.operacao == "transladar":
                                        self.handle_event()
                                    elif self.operacao == "escalar":
                                        self.handle_event()
                                self.handle_event()
                        
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.state and self.selecao_inicio is not None:
                        #finaliza a seleção
                        selecao_fim = pygame.mouse.get_pos()
                        self.verificar_selecao(self.selecao_inicio[0], self.selecao_inicio[1], 
                                              selecao_fim[0], selecao_fim[1])
                        self.selecao_inicio = None
                
                elif event.type == pygame.MOUSEMOTION and self.state and self.selecao_inicio is not None:
                    #redesenha a tela para não acumular retângulos de seleção
                    self.redesenhar_tela()
                    
                    #desenha o retângulo de seleção
                    pos_atual = pygame.mouse.get_pos()
                    select_rect = pygame.Rect(
                        min(self.selecao_inicio[0], pos_atual[0]),
                        min(self.selecao_inicio[1], pos_atual[1]),
                        abs(pos_atual[0] - self.selecao_inicio[0]),
                        abs(pos_atual[1] - self.selecao_inicio[1])
                    )
                    pygame.draw.rect(self.screen, BLUE, select_rect, 1)



                #funcao limpar tela(tela e retas e objetos e poligonos e tudo)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.meu_vetor = []
                        self.estrutura = []
                        self.poligonos = []
                        self.obj_selected = []
                        self.clipping_window.active = False
                        self.defining_clip_window = False
                        self.screen.fill(WHITE)
            #desenha os botoes
            botao.draw(self.screen, self.state)

            if self.state:
                self.draw_input_fields()
            
            pygame.display.update()
            pygame.display.flip()
        pygame.quit()

class Botao:
    #construtor da classe Botao
    def __init__(self, x, y, width, height, color, texts, functions):
        self.font = pygame.font.SysFont('Arial', 16)
        self.buttons = []
        j = 0
        for i, text in enumerate(texts):
            button_text = self.font.render(text, True, BLACK)
            button_rect = pygame.Rect(x, y + i * (height + 5), width, height)
            self.buttons.append((button_text, button_rect, functions[i], False))
        self.color = color
        self.highlight_color = (min(color[0] + 50, 255), 
                               min(color[1] + 50, 255), 
                               min(color[2] + 50, 255))
        self.disabled_color = (100, 100, 100)
    #função para desenhar os botões
    def draw(self, surface, selection_mode=False):
        for i, (button_text, button_rect, _, is_active) in enumerate(self.buttons):
            #determina a cor do botão
            if i == 4:  #botão "Selecionar"
                current_color = self.highlight_color if is_active else self.color
            elif selection_mode and i < 4:  #botões desabilitados no modo de seleção
                current_color = self.disabled_color
            else:
                current_color = self.highlight_color if is_active else self.color
                
            pygame.draw.rect(surface, current_color, button_rect)
            pygame.draw.rect(surface, BLACK, button_rect, 1)  # Borda
            text_rect = button_text.get_rect(center=button_rect.center)
            surface.blit(button_text, text_rect)
    #função para verificar se o botão foi clicado -> utiliza um contador para representar os botoes, mas é selecionado pela posição do mouse clicado
    def handle_event(self, event, selection_mode=False):
        mouse_pos = event.pos
        for i, (_, button_rect, function, _) in enumerate(self.buttons):
            if button_rect.collidepoint(mouse_pos):
                #se estiver no modo de seleção, só permite clicar no botão "Selecionar"
                if selection_mode and i < 4 and i !=4:
                    return True  # Retorna True para não processar o clique como um ponto
                
                #para os botões de algoritmo (DDA e Bresenham)
                if i > 1 and i < 4:
                    self.buttons = [(text, rect, func, False) for text, rect, func, _ in self.buttons]
                    self.buttons[i] = (self.buttons[i][0], self.buttons[i][1], self.buttons[i][2], True)
                
                #para o botão de seleção, alterna o estado ativo
                if i == 4:
                    self.buttons[i] = (self.buttons[i][0], self.buttons[i][1], self.buttons[i][2], not self.buttons[i][3])
                
                function()  #chama a função correspondente do botao
                return False
        return True
    
class CampoTexto:
    def __init__(self, x, y, width, height, placeholder=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = LIGHT_GRAY
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        self.font = pygame.font.SysFont('Arial', 16)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
        # Ativa/desativa o campo ao clicar
            if self.rect.collidepoint(event.pos):
                self.active = True
                return True
            else:
                self.active = False
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            else:
                # Apenas aceita números, ponto decimal e sinal negativo
                if event.unicode.isnumeric() or event.unicode == '.' or event.unicode == '-':
                    self.text += event.unicode
            return True
        return False
    
    def draw(self, surface):
        # Define a cor do campo baseado no estado
        color = BLUE if self.active else GRAY
        pygame.draw.rect(surface, LIGHT_GRAY, self.rect)
        pygame.draw.rect(surface, color, self.rect, 2)
        
        # Renderiza o texto ou placeholder
        if self.text:
            text_surface = self.font.render(self.text, True, BLACK)
        else:
            text_surface = self.font.render(self.placeholder, True, (100, 100, 100))
        
        # Calcula a posição do texto
        text_rect = text_surface.get_rect(midleft=(self.rect.x + 5, self.rect.y + self.rect.height/2))
        
        # Limita o texto ao tamanho do campo
        surface.blit(text_surface, text_rect)
    
    def get_value(self):
        try:
            return float(self.text) if self.text else 0
        except ValueError:
            return 0
    

class Circulo:
    #construtor da classe Circulo
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.raio = int(np.sqrt((self.x2-self.x1)**2 + (self.y2-self.y1)**2))
    #função para plotar os pontos simétricos, aproveitando para processar apenas 1/8 do círculo
    def plotaSimetricos(self, surface, x, y, color):
        surface.set_at((x + self.x1, y + self.y1), color)
        surface.set_at((-x + self.x1, y + self.y1), color)
        surface.set_at((x + self.x1, -y + self.y1), color)
        surface.set_at((-x + self.x1, -y + self.y1), color)
        surface.set_at((y + self.x1, x + self.y1), color)
        surface.set_at((-y + self.x1, x + self.y1), color)
        surface.set_at((y + self.x1, -x + self.y1), color)
        surface.set_at((-y + self.x1, -x + self.y1), color)
    #algoritmo para desenhar o círculo
    def draw(self, surface, color):
        x, y, p = 0, self.raio, 3-2*self.raio
        self.plotaSimetricos(surface, x, y, color)
        while x < y:#2° OCTANTE
            x += 1
            if p < 0:
                p += 4*x + 6
            else:
                y -= 1
                p += 4*(x-y) + 10
            self.plotaSimetricos(surface, x, y, color)

        
#todos os algoritmos para desenhar retas estão na classe Reta
class Reta:
    #construtor da classe Reta
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    #algoritmo de Bresenham para desenhar a reta
    def drawBreseham(self, surface, color):
        dx = self.x2 - self.x1
        dy = self.y2 - self.y1
        x, y = self.x1, self.y1
        surface.set_at((int(np.round(x)), int(np.round(y))), color)
        if(dx>0):
            xInc = 1
        else:
            xInc = -1
            dx = -dx
        if(dy>0):
            yInc = 1
        else:
            yInc = -1
            dy = -dy
        if dx > dy:#1° CASO(reta varia mais em x)
            p = 2*dy-dx
            c1 = 2*dy
            c2 = 2*(dy-dx)
            for i in range(dx):
                x += xInc
                if p < 0:
                    p += c1
                else:
                    y += yInc
                    p += c2
                surface.set_at((x, y), color)
        else:#2° CASO(inverso do 1° caso)(reta varia mais em y)
            p = 2*dx-dy
            c1 = 2*dx
            c2 = 2*(dx-dy)
            for i in range(dy):
                y += yInc
                if p < 0:
                    p += c1
                else:
                    x += xInc
                    p += c2
                surface.set_at((x, y), color)     
    #algoritmo DDA para desenhar a reta
    def drawDDA(self, surface, color):
        dx = float(self.x2 - self.x1)
        dy = float(self.y2 - self.y1)
        x, y = float(self.x1), float(self.y1)
        if dx!=0 or dy!=0:
            if abs(dx) > abs(dy):
                steps = abs(dx)
            else:
                steps = abs(dy)
            xInc = dx / steps
            yInc = dy / steps
            for i in range(int(steps)):
                x += xInc
                y += yInc
                surface.set_at((int(np.round(x)), int(np.round(y))), color)

class ClippingWindow:
    def __init__(self, x_min=300, y_min=300, x_max=400, y_max=400):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.color = BLACK
        self.active = False

    def draw(self, surface, color):
        if self.active:
            pygame.draw.rect(surface, color, (self.x_min, self.y_min, 
                                              self.x_max - self.x_min, 
                                              self.y_max - self.y_min), 2)
    # Define as coordenadas da janela de recorte
    def set_coordinates(self, x1, y1, x2, y2):
        self.x_min = min(x1, x2)
        self.y_min = min(y1, y2)
        self.x_max = max(x1, x2)
        self.y_max = max(y1, y2)
    
    # Algoritmo de Cohen-Sutherland
    def cohen_sutherland(self, x1, y1, x2, y2):
        # Códigos de região
        if x1 == x2 and y1 == y2:
            if (self.x_min <= x1 <= self.x_max and self.y_min <= y1 <= self.y_max):
                return True, (x1, y1, x2, y2)
            return False, None
        
        accept = False
        done = False
        while not done:
            codA = self.calc_cod(x1, y1)
            codB = self.calc_cod(x2, y2)
            if codA == 0 and codB == 0:# segmento completamente dentro da janela
                accept = True
                done = True
            elif codA & codB != 0:#segmento completamente fora da janela
                done = True
            else:
                cod = codA if codA != 0 else codB
                if cod & 1:
                    x = self.x_min
                    y = y1 + (y2 - y1) * (self.x_min - x1) / (x2 - x1)
                elif cod & 2:
                    x = self.x_max
                    y = y1 + (y2 - y1) * (self.x_max - x1) / (x2 - x1)
                elif cod & 4:
                    y = self.y_min
                    x = x1 + (x2 - x1) * (self.y_min - y1) / (y2 - y1)
                elif cod & 8:
                    y = self.y_max
                    x = x1 + (x2 - x1) * (self.y_max - y1) / (y2 - y1)
                if cod == codA:
                    x1, y1 = x, y
                else:
                    x2, y2 = x, y
        if accept:
            return accept, (int(np.round(x1)), int(np.round(y1)), int(np.round(x2)), int(np.round(y2)))
        else:
            return accept, None

    # Calcula o código de região de um ponto
    def calc_cod(self,x,y):
        cod = 0
        if x < self.x_min:
            cod += 1
        if x > self.x_max:
            cod += 2
        if y < self.y_min:
            cod += 4
        if y > self.y_max:
            cod += 8
        return cod
    
    # Algoritmo de Liang-Barsky
    def liang_barsky(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            if (self.x_min <= x1 <= self.x_max and self.y_min <= y1 <= self.y_max):
                return True, (x1, y1, x2, y2)
            return False, None
        dx = x2 - x1
        dy = y2 - y1
        p = [-dx, dx, -dy, dy]
        q = [x1 - self.x_min, self.x_max - x1, y1 - self.y_min, self.y_max - y1]
        u1 = 0
        u2 = 1
        for i in range(4):
            # P = 0, linha paralela ao lado da janela
            if p[i] == 0:
                if q[i] < 0:
                    return False, None
            else:
                u = q[i] / p[i]
                if p[i] < 0:
                    if u > u2:
                        return False, None
                    u1 = max(u1, u)
                else:
                    if u < u1:
                        return False, None
                    u2 = min(u2, u)
        if u1 > u2:
            return False, None
        x1_clip = x1 + u1 * dx
        y1_clip = y1 + u1 * dy
        x2_clip = x1 + u2 * dx
        y2_clip = y1 + u2 * dy
        
        return True, (int(np.round(x1_clip)), int(np.round(y1_clip)), int(np.round(x2_clip)), int(np.round(y2_clip)))
        
    

if __name__ == "__main__":
    interface = Interface()
    interface.inicialize_tela()




