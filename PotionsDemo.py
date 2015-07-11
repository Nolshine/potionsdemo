"""
Potion Mixing Minigame Demo
"""

#imports
import random

import pygame
from pygame import *

class Ingredient:	#class to represent ingredients

	def __init__(self):

		#self.name = name #name of ingredient (do i need this? let's say no.)

		self.flavour = [] #flavor is an rgb value for now, stored as ints in a list
		for i in range(3): #create a random rgb value and append each R G and B values to the self.flavour
			self.flavour.append(int(random.random()*255))
		
	def get_flavour(self):
		return (self.flavour[0], self.flavour[1], self.flavour[2])

def main(): # The main program

	pygame.init()

	screen = pygame.display.set_mode((640, 480)) #main window
	clock = pygame.time.Clock() #a clock?? :P
	# let's make a subsurface to blit ingredient buttons on
	# let's say 4 ingredients so a 4 button menu
	# each button.. 64x64 in size, including border?
	inventory = pygame.Surface.subsurface(screen, (0, 0, 64*4, 64))
	cauldron = pygame.image.load("img/cauldron.png")

	ingredients = []
	for i in range(4):
		ingredients.append(Ingredient())

	running = True
	while running: #main loop
		clock.tick(60)

		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False

		screen.fill((255,255,255))
		screen.blit(cauldron, (((640/2)-128), ((480/2)-128)))

		# make the ingredient menu appear
		for i in range(len(ingredients)):
			rect = (i*64, 0, 64, 64)
			pygame.draw.rect(inventory, (0,0,0), rect)
			pygame.draw.rect(inventory, ingredients[i].get_flavour(), rect)

		pygame.display.update()

	pygame.quit()

if __name__ == "__main__":
	main()