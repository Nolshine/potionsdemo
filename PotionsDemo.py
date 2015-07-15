"""
Potion Mixing Minigame Demo
"""

#imports
import random

import pygame
from pygame import *

pygame.init() #initialize pygame here so i can use the modules in classes and functions

#######################################################################

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
		self.lbl_timer = self.font.render("Time Remaining:", 1, (0,0,0))
	
	def new_label(self, text): #for rendering text on the fly
		return self.font.render(text, 1, (0, 0, 0))

#######################################################################

def drag(inventory, inventoryButton, pos, ingredients):
	if inventoryButton.collidepoint(pos):
		print "picked up ingredient!"
		return ingredients[pos[0]/64].get_flavour()
	else:
		print "nothing to drag!"
		return 0

def drop(inHand):
	result = []
	for i in inHand:
		result.append(i/5)
	return result


def main(): # The main program

	SCREEN_RES = (640, 480)
	screen = pygame.display.set_mode((SCREEN_RES[0], SCREEN_RES[1])) #main window
	clock = pygame.time.Clock() #a clock?? :P
	# let's make a subsurface to blit ingredient buttons on
	# let's say 4 ingredients so a 4 button menu
	# each button.. 64x64 in size, including border?
	inventory = pygame.Surface.subsurface(screen, (0, 0, 64*4, 64)) #subsurface to blit inventory on
	inventoryButton = inventory.get_rect() #rect to detect clicking in
	statsText = pygame.Surface.subsurface(screen, (30, SCREEN_RES[1]/2, 80, 53)) #subsurfaces to blit stats on
	statsData = pygame.Surface.subsurface(screen, (110, SCREEN_RES[1]/2, 50, 53)) #subsurfaces to blit stats on
	timerData = pygame.Surface.subsurface(screen, (SCREEN_RES[0]-150, 10, 143, 53)) #subsurface to blit timer on
	cauldron = pygame.image.load("img/cauldron.png")
	cauldronButton = pygame.Rect((((SCREEN_RES[0]/2)-128), ((SCREEN_RES[1]/2)-128)), cauldron.get_size())

	#text manager
	textManager = Text()

	#game data
	ingredients = []
	for i in range(4):
		ingredients.append(Ingredient())
	thickness = 0.0 #the higher the better?
	flavour = [0, 0, 0] #will probably be updated continuously
	maxThickness = 100 #this will drop with each ingredient added, making spamming ingredients unrewarding
	numIngredients = 0 #increases with each ingredient added - each removes 5% from max thickness,
	#					down to a minumim of 20%.

	running = True
	lmbDown = False
	isDragging = False
	dragCounter = 0
	inHand = 0
	timer = 30
	timePassed = 0
	while running: #main loop
		timePassed += clock.tick(60)
		if timePassed >= 1000:
			timePassed = 0
			timer -= 1
			if timer == 0:
				print "minigame over" #todo actual stuff happening when this happens


		#game logic here.
		if thickness > 0:
			thickness -= 0.25
			#no need to make sure it's not below zero, since that can't happen with current logic.

		#event processing code here.
		for event in pygame.event.get():
			if event.type == QUIT:
				running = False
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				running = False
			if event.type == MOUSEBUTTONDOWN and event.button == 1:
				lmbDown = True
				mousepos = event.pos
				if cauldronButton.collidepoint(mousepos):
					if thickness < maxThickness:
						thickness += 5
					if thickness > maxThickness:
						thickness = maxThickness
			if event.type == MOUSEBUTTONUP and event.button == 1:
				mousepos = event.pos
				lmbDown = False

		if lmbDown:
			dragCounter += 1
		else: #if lmb isn't down, and we started dragging already, perform drop logic
			if isDragging and inHand != 0 and cauldronButton.collidepoint(mousepos):
				# if we're dragging and holding an ingredient and we dropped it in the cauldron, perform this logic
				dropping = drop(inHand)
				print dropping
				for i in range(len(dropping)):
					flavour[i] += dropping[i]
				inHand = 0
				print flavour
				# recalculate the maximum thickness
				numIngredients += 1 #dont' really need it right now but it seems like a fun stat to track
				maxThickness -= 5
				if maxThickness < 20:
					maxThickness = 20
				# NOTE: could probably only do this logic is maxThickness is above 20, saving a few cycles in the process?

			else: # under any other conditions perform this logic
				inHand = 0
			# and reset drag mechanism
			dragCounter = 0
			isDragging = False

		if dragCounter >= 10 and not isDragging: #start dragging if lmb is down, we haven't started, and the counter is done
			isDragging = True
			inHand = drag(inventory, inventoryButton, mousepos, ingredients)

		for i in range(len(flavour)):
			if flavour[i] > 255:
				print "oversaturated!"
				flavour[i] = 255


		#render code here
		#fill the screen with white
		screen.fill((255,255,255))
		#blit the cauldron sprite (ewww..)
		screen.blit(cauldron, cauldronButton)

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
		pygame.draw.circle(statsData, (flavour[0], flavour[1], flavour[2]), (9, 12), 8)
		statsData.blit(numberThickness, (0, 29))
		#blit time remaining
		numberTimeRemaining = textManager.new_label(str(timer))
		timerData.blit(textManager.lbl_timer, (0, 0))
		timerData.blit(numberTimeRemaining, (textManager.lbl_timer.get_width(), 0))
		#if holding an ingrediet, blit its flavour
		if inHand != 0:
			pos = pygame.mouse.get_pos()
			color = (inHand[0], inHand[1], inHand[2])
			pygame.draw.circle(screen, (0,0,0), pos, 11)
			pygame.draw.circle(screen, color, pos, 10)
		pygame.display.update()

	pygame.quit()

if __name__ == "__main__":
	main()