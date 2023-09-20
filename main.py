import pygame
import button
from random import choice, randrange

def poziom_trudnosci(zmienna):

    class Cell:

        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
            self.visited = False
            self.thickness = 4

        def draw(self, sc):
            x, y = self.x * KAFELEK, self.y * KAFELEK

            if self.walls['top']:
                pygame.draw.line(sc, pygame.Color('black'), (x, y), (x + KAFELEK, y),
                                self.thickness)
            if self.walls['right']:
                pygame.draw.line(sc, pygame.Color('black'), (x + KAFELEK, y),
                                (x + KAFELEK, y + KAFELEK), self.thickness)
            if self.walls['bottom']:
                pygame.draw.line(sc, pygame.Color('black'), (x + KAFELEK, y + KAFELEK),
                                (x, y + KAFELEK), self.thickness)
            if self.walls['left']:
                pygame.draw.line(sc, pygame.Color('black'), (x, y + KAFELEK), (x, y),
                                self.thickness)

        def get_rects(self):
            rects = []
            x, y = self.x * KAFELEK, self.y * KAFELEK
            if self.walls['top']:
                rects.append(pygame.Rect((x, y), (KAFELEK, self.thickness)))
            if self.walls['right']:
                rects.append(pygame.Rect((x + KAFELEK, y), (self.thickness, KAFELEK)))
            if self.walls['bottom']:
                rects.append(pygame.Rect((x, y + KAFELEK), (KAFELEK, self.thickness)))
            if self.walls['left']:
                rects.append(pygame.Rect((x, y), (self.thickness, KAFELEK)))
            return rects

        def spr_poprawnosc_komorki(self, x, y):
            find_index = lambda x, y: x + y * cols
            if (x < 0) or (x > cols - 1) or (y < 0) or (y > rows - 1):
                return False
            return self.grid_cells[find_index(x, y)]

        def sprawdz_sasiadujace_komorki(self, grid_cells):
            self.grid_cells = grid_cells
            neighbors = []
            top = self.spr_poprawnosc_komorki(self.x, self.y - 1)
            right = self.spr_poprawnosc_komorki(self.x + 1, self.y)
            bottom = self.spr_poprawnosc_komorki(self.x, self.y + 1)
            left = self.spr_poprawnosc_komorki(self.x - 1, self.y)
            if top and not top.visited:
                neighbors.append(top)
            if right and not right.visited:
                neighbors.append(right)
            if bottom and not bottom.visited:
                neighbors.append(bottom)
            if left and not left.visited:
                neighbors.append(left)
            return choice(neighbors) if neighbors else False

	#koniec cell
					
    def usun_sciany(current, next):
        dx = current.x - next.x
        if dx == 1:
            current.walls['left'] = False
            next.walls['right'] = False
        elif dx == -1:
            current.walls['right'] = False
            next.walls['left'] = False
        dy = current.y - next.y
        if dy == 1:
            current.walls['top'] = False
            next.walls['bottom'] = False
        elif dy == -1:
            current.walls['bottom'] = False
            next.walls['top'] = False


    def generuj_labirynt():
        grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
        current_cell = grid_cells[0]
        array = []
        break_count = 1

        while break_count != len(grid_cells):
            current_cell.visited = True
            next_cell = current_cell.sprawdz_sasiadujace_komorki(grid_cells)
            if next_cell:
                next_cell.visited = True
                break_count += 1
                array.append(current_cell)
                usun_sciany(current_cell, next_cell)
                current_cell = next_cell
            elif array:
                current_cell = array.pop()
        return grid_cells


###### koniec generacji labiryntu #######


    RES = SZEROKOSC, WYSOKOSC = 500, 500
    KAFELEK = zmienna
    cols, rows = SZEROKOSC // KAFELEK, WYSOKOSC // KAFELEK

    def gracz_uderzyl_w_sciane(x, y):
        tmp_rect = player_rect.move(x, y)
        if tmp_rect.collidelist(lista_kolizji_ze_ścianami) == -1:
            return False
        return True

    koniec_x=(SZEROKOSC - KAFELEK//2)
    koniec_y=(WYSOKOSC - KAFELEK//2)
	
    def win():
        if (player_rect.center == (koniec_x,koniec_y)):
            return True

    FPS = 60
    pygame.init()
    game_surface = pygame.Surface(RES)
    surface = pygame.display.set_mode((SZEROKOSC_EKRANU , WYSOKOSC_EKRANU ))
    clock = pygame.time.Clock()

    maze = generuj_labirynt()

    player_speed = 5
    player_img = pygame.image.load('images/postac.png').convert_alpha()
    player_img = pygame.transform.scale(
    player_img, (KAFELEK - 2 * maze[0].thickness, KAFELEK - 2 * maze[0].thickness))
    player_rect = player_img.get_rect()
    player_rect.center = KAFELEK // 2, KAFELEK // 2
    directions = {
    'a': (-player_speed, 0),
    'd': (player_speed, 0),
    'w': (0, -player_speed),
    's': (0, player_speed)
    }
    keys = {'a': pygame.K_a, 'd': pygame.K_d, 'w': pygame.K_w, 's': pygame.K_s}
    direction = (0, 0)


    lista_kolizji_ze_ścianami = sum([cell.get_rects() for cell in maze], [])

    pygame.time.set_timer(pygame.USEREVENT, 1000)
    time = 60

    while True:
            screen.fill((200, 78, 91))
            zak_button = button.Button(150, 710, zak_img, 1)
            if zak_button.draw(screen):
                    exit()
            
            surface.blit(game_surface, (50, 50))
            game_surface.fill(pygame.Color("white"))
            pygame.draw.rect(game_surface, pygame.Color("green"),
                            pygame.Rect(2, 2, KAFELEK - 2, KAFELEK - 2))
            pygame.draw.rect(game_surface, pygame.Color("red"),
                            pygame.Rect(SZEROKOSC - KAFELEK, SZEROKOSC - KAFELEK, KAFELEK - 2, KAFELEK - 2))
            draw_text("Poruszaj się klawiszami WSAD ", pygame.font.SysFont("arialblack", 40), TEXT_COL, 80, 580)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.USEREVENT:
                    time -= 1

            pressed_key = pygame.key.get_pressed()

            for key, key_value in keys.items():
                if pressed_key[key_value] and not gracz_uderzyl_w_sciane(*directions[key]):
                    direction = directions[key]
                    break
            if not gracz_uderzyl_w_sciane(*direction):
                player_rect.move_ip(direction)

            #labirynt
            [cell.draw(game_surface) for cell in maze]
            # gracz
            game_surface.blit(player_img, player_rect)

            #print(koniec_x,koniec_y)
            #print(player_rect.center)
            if(win() == True):
                draw_text("ZNALAZŁEŚ  WYJŚCIE ! ! !", pygame.font.SysFont("arialblack", 60), TEXT_COL, 60, 630)
            pygame.display.flip()
            clock.tick(FPS)   

#################################################################
pygame.init()

SZEROKOSC_EKRANU = 600
WYSOKOSC_EKRANU = 800

screen = pygame.display.set_mode((SZEROKOSC_EKRANU, WYSOKOSC_EKRANU))
pygame.display.set_caption("Labirynt")

font = pygame.font.SysFont("arialblack", 40)
TEXT_COL = (255, 255, 255)

p_img = pygame.image.load('images/P.png').convert_alpha()
s_img = pygame.image.load('images/S.png').convert_alpha()
t_img = pygame.image.load('images/T.png').convert_alpha()
zak_img = pygame.image.load('images/Z.png').convert_alpha()
m_img = pygame.image.load('images/M.png').convert_alpha()

p_button = button.Button(150, 210, p_img, 1)
s_button = button.Button(150, 310, s_img, 1)
t_button = button.Button(150, 410, t_img, 1)
zak_button = button.Button(150, 710, zak_img, 1)
m_button = button.Button(150, 610, m_img, 1)

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#główna pętla
run = True
menu_state = 'main'
while run:

  screen.fill((200, 78, 91))
  if menu_state == "main":
        draw_text("L A B I R Y N T", pygame.font.SysFont("arialblack", 80), TEXT_COL, 110, 30)
        draw_text("Wybierz poziom trudnosci", font, TEXT_COL, 120, 120)
        if p_button.draw(screen):
                menu_state = "prosty"
        if s_button.draw(screen):
                menu_state = "sredni"
        if t_button.draw(screen):
                menu_state = "trudny"
        if zak_button.draw(screen):
                    run = False

  if menu_state == "prosty":
        poziom_trudnosci(100)
  if menu_state == "sredni":
        poziom_trudnosci(50)    
  if menu_state == "trudny":
        poziom_trudnosci(10)    

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

pygame.quit()










