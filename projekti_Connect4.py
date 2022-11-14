import numpy as np
import pygame
import sys  #Moduli sys në Python ofron funksione dhe variabla të ndryshme që përdoren për të manipuluar
# pjesë të ndryshme të mjedisit të ekzekutimit të Python. Ai lejon funksionimin në përkthyes pasi 
# siguron akses në variablat dhe funksionet që ndërveprojnë fuqishëm me interpretuesin.
import math

Bardhe= (255,255,255)
Zi = (0,0,0)
Kuqe = (255,0,0)
Kalter = (0,0,255)

Nr_rreshtave = 6
Nr_kolonave = 7

def create_tabela(): # krijohet tabela me nr specifik te rreshtave dhe kolonave
	tabela = np.zeros((Nr_rreshtave,Nr_kolonave))
	return tabela

def drop_pjese(tabela, rreshti, kolona, pjese):
	tabela[rreshti][kolona] = pjese

def is_valid_location(tabela, kolona):
	return tabela[Nr_rreshtave-1][kolona] == 0

def get_next_open_rreshti(tabela, kolona):
	for r in range(Nr_rreshtave):
		if tabela[r][kolona] == 0:
			return r

def print_tabela(tabela):
	print(np.flip(tabela, 0))

def winning_move(tabela, pjese):
	# Kontrollo pjesen horizontale per fituesin
	for c in range(Nr_kolonave-3):
		for r in range(Nr_rreshtave):
			if tabela[r][c] == pjese and tabela[r][c+1] == pjese and tabela[r][c+2] == pjese and tabela[r][c+3] == pjese:
				return True

	# Kontrollo pjesen vertikale per fituesin
	for c in range(Nr_kolonave):
		for r in range(Nr_rreshtave-3):
			if tabela[r][c] == pjese and tabela[r+1][c] == pjese and tabela[r+2][c] == pjese and tabela[r+3][c] == pjese:
				return True

	# Me i kontrollu diagonale qe jane pjerret pozitiv
	for c in range(Nr_kolonave-3):
		for r in range(Nr_rreshtave-3):
			if tabela[r][c] == pjese and tabela[r+1][c+1] == pjese and tabela[r+2][c+2] == pjese and tabela[r+3][c+3] == pjese:
				return True

	# Kontrollo diagonalet qe jane pjerret negativ
	for c in range(Nr_kolonave-3):
		for r in range(3, Nr_rreshtave):
			if tabela[r][c] == pjese and tabela[r-1][c+1] == pjese and tabela[r-2][c+2] == pjese and tabela[r-3][c+3] == pjese:
				return True

def draw_tabela(tabela):
	for c in range(Nr_kolonave):
		for r in range(Nr_rreshtave):
			pygame.draw.rect(screen, Bardhe, (c*MadhesiaD, r*MadhesiaD+MadhesiaD, MadhesiaD, MadhesiaD))
			pygame.draw.circle(screen, Zi, (int(c*MadhesiaD+MadhesiaD/2), int(r*MadhesiaD+MadhesiaD+MadhesiaD/2)), radiusi)
	
	for c in range(Nr_kolonave):
		for r in range(Nr_rreshtave):		
			if tabela[r][c] == 1:
				pygame.draw.circle(screen, Kuqe, (int(c*MadhesiaD+MadhesiaD/2), height-int(r*MadhesiaD+MadhesiaD/2)), radiusi)
			elif tabela[r][c] == 2: 
				pygame.draw.circle(screen, Kalter, (int(c*MadhesiaD+MadhesiaD/2), height-int(r*MadhesiaD+MadhesiaD/2)), radiusi)
	pygame.display.update()


tabela = create_tabela()
print_tabela(tabela)
mbarimi_lojes = False
radhe = 0

pygame.init()

MadhesiaD = 130

width = Nr_kolonave * MadhesiaD
height = (Nr_rreshtave+1) * MadhesiaD

size = (width, height)

radiusi = int(MadhesiaD/2 - 5)

screen = pygame.display.set_mode(size)
draw_tabela(tabela)
pygame.display.update()

myfont = pygame.font.SysFont("arial.ttf", 60)

while not mbarimi_lojes:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, Zi, (0,0, width, MadhesiaD))
			posx = event.pos[0]
			if radhe == 0:
				pygame.draw.circle(screen, Kuqe, (posx, int(MadhesiaD/2)), radiusi)
			else: 
				pygame.draw.circle(screen, Kalter, (posx, int(MadhesiaD/2)), radiusi)
		pygame.display.update()
 
		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, Zi, (0,0, width, MadhesiaD))
			#print(event.pos)
			# kekro nga lojtari 1 per te luajtur, filluar, per input
			if radhe == 0:
				posx = event.pos[0]
				kolona = int(math.floor(posx/MadhesiaD))

				if is_valid_location(tabela, kolona):
					rreshti = get_next_open_rreshti(tabela, kolona)
					drop_pjese(tabela, rreshti, kolona, 1)

					if winning_move(tabela, kolona):
						rezultati = myfont.render("Lojtari pare ka fituar!!", 1, Kuqe)
						screen.blit(rezultati, (30,5))
						mbarimi_lojes = True


			# Pytet lojtari i dyte per inputet
			else:				
				posx = event.pos[0]
				kolona = int(math.floor(posx/MadhesiaD))

				if is_valid_location(tabela, kolona):
					rreshti = get_next_open_rreshti(tabela, kolona)
					drop_pjese(tabela, rreshti, kolona, 2)

					if winning_move(tabela, 2):
						rezultati = myfont.render("Lojtari i dyte ka fituar!", 1, Kalter)
						screen.blit(rezultati, (30,5))
						mbarimi_lojes = True

			print_tabela(tabela)
			draw_tabela(tabela)

			radhe += 1
			radhe = radhe % 2

			if mbarimi_lojes:
				pygame.time.wait(3000)

