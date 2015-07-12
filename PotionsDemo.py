"""
Potion Mixing Minigame Demo
"""

#imports
import random

import pygame
from pygame import *

pygame.init() #initialize pygame here so i can use the modules in classes and functions

class Ingredient:	#class to represent ingredients

	def __init__(self):

		#self.name = name #name of ingredient (do i need this? let's say no.)

		self.flavour = [] #flavor is an rgb value for now, stored as ints in a list
		for i in range(3): #create a random rgb value and append each R G and B values to the self.flavour
			self.flavour.append(int(random.random()*255))
		
	def get_flavour(self):
		return (self.flavour[0], self.flavour[1], self.flavour[2])

class Text:
	font = pygame.font.SysFont("Arial", 16)

	def __init__(self):
		#prepare permatext to render
		self.lbl_thickness = self.font.render("Thickness:", 1, (0,0,0))
		self.lbl_flavour = self.font.render("Flavour:", 1, (0,0,0))
	
	def new_label(self, text): #for rendering text on the fly
		return self.font.render(text, 1, (0, 0, 0))

def main(): # The main program

	SCREEN_RES = (640, 480)
	screen = pygame.display.set_mode((SCREEN_RES[0], SCREEN_RES[1])) #main window
	clock = pygame.time.Clock() #a clock?? :P
	# let's make a subsurface to blit ingredient buttons on
	# let's say 4 ingredients so a 4 button menu
	# each button.. 64x64 in size, including border?
	inventory = pygame.Surface.subsurface(screen, (0, 0, 64*4, 64)) #subsurface to blit inventory on
	statsText = pygame.Surface.subsurface(screen, (30, SCREEN_RES[1]/2, 80, 53)) #subsurfaces to blit stats on
	statsData = pygame.Surface.subsurface(screen, (110, SCREEN_RES[1]/2, 50, 53)) #subsurfaces to blit stats on
	cauldron = pygame.image.load("img/cauldron.png")
	#text manager
	textManager = Text()

	#game data
	ingredients = []
	for i in range(4):
		ingredients.append(Ingredient())
	thickness = 0.0 #the higher the better?
	flavour = [0, 0, 0] #will probably be updated continuously

	running = True
	while running: #main loop
		clock.tick(60)

		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		#render code here
		#fill the screen with white
		screen.fill((255,255,255))
		#blit the cauldron sprite (ewww..)
		screen.blit(cauldron, (((SCREEN_RES[0]/2)-128), ((SCREEN_RES[1]/2)-128)))

		# make the ingredient menu appear
		for i in range(len(ingredients)):
			pygame.draw.rect(inventory, (0,0,0), (i*64, 0, 64, 64))
			pygame.draw.rect(inventory, ingredients[i].get_flavour(), (i*64+1, 1, 62, 62))

		#blit potion status text
		statsText.blit(textManager.lbl_flavour, (0, 5))
		statsText.blit(textManager.lbl_thickness, (0, 29))
		#blit potion status data
		numberThickness = textManager.new_label(str(thickness))
		pygame.draw.circle(statsData, (0, 0, 0), (9, 12), 9)
		pygame.draw.circle(statsData, (flavour[0], flavour[1], flavour[2]), (10, 13), 8)
		statsData.blit(numberThickness, (0, 29))

		pygame.display.update()

	pygame.quit()

if __name__ == "__main__":
	main()