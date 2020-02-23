import pygame
import random

#colors, width and height
white = (255, 255, 255)
red = (255, 000, 00)
black = (0, 0, 0)
w,h = 600,700

# suface
tela = pygame.display.set_mode((w,h))

# loading the images
invader_img = pygame.image.load('assets/invader.png')
player_img = pygame.image.load('assets/player.png')
bullet = pygame.image.load('assets/heart.png')
heart = pygame.image.load('assets/heart.png')

# init of the module
pygame.init()

# the main loop variable
run = True

# function to create the invaders, here r all they properties, like width, height, quantity...
def setupinvaders():
	invaderlist = []

	y = 50
	num_rows = 4
	num_invaders_per_row = 10

	while y <= 50 * num_rows:
		x = 85
		while x <= 50 * num_invaders_per_row:
			invaderlist.append(pygame.Rect(x, y, 30, 30))
			x += 50
		y += 50
	return invaderlist


# funciton to put on the surface the image of the invaders
def drawinvaders(invaderlist, tela):
	for i in invaderlist:
		tela.blit(invader_img, i)

# function to move the invaders by a Dx variable of velocity and define the edges
def movealiens(invaderslist, dx):
	for i in invaderslist:
		if i.right > w or i.left < 0:
			dx = dx * -1
			for alien in invaderslist:
				alien.move_ip(0,50)
			break
	for i in invaderslist:
		i.move_ip(dx, 0)
	return dx

# setting up the player
px = 0
player = pygame.Rect(297,560,43,30)
lives = 5

# setting up the invaders
fc = 0
invaderslist = setupinvaders()
dx = 1

# setting the player's bullets
playerbullets = []

# setting the enemy's bullets and how they will be fired
enemybullets = []
probabilitytofire = 0.0006
maxenemybullets = 8


# main loop
while run:

	# getting the events on the pygame
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		#moving and actions of the player only in key-down
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				px = -3
			elif event.key == pygame.K_RIGHT:
				px = 3
			if event.key == pygame.K_SPACE:
				if len(playerbullets) < 4:
					playerbullets.append(pygame.Rect(player.x + 19.5 , player.y, 5, 20))
		# on the key-up movment, the player stop
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				px = 0
	# framecount for better moving appearence
	if fc >= 400:
		dx = movealiens(invaderslist, dx)
		fc = 0
	fc = fc + 1
	# defining the edges for player
	if player.left + px < 0 or player.right + px > w :
		px = 0
	# function to chance the place of player and the invaders by Px and Dx variables of velocity
	player.move_ip(px, 0)
	dx = movealiens(invaderslist, dx)


	# defining the bullets on the list like 'b' and getting the colisions
	for b in playerbullets:
		b.move_ip(0, -8)
		if b.y < 0: playerbullets.remove(b)
		for i in invaderslist:
			if i.colliderect(b):
				invaderslist.remove(i)
				# i put that try to fix the bug thats the loop cant find the bullets on the list
				try:
				 playerbullets.remove(b)
				except:
					pass

	# setting the enemys bullets with the random module
	for i in invaderslist:
		firechance = random.random()
		if firechance <= probabilitytofire and len(enemybullets) <= maxenemybullets:
			enemybullets.append(pygame.Rect(i.x, i.y, 5, 20))


	for b in enemybullets:
		b.move_ip(0,2)
		if b.colliderect(player):
			lives -= 1
			enemybullets.remove(b)


			if lives == 0:  run = False

		if b.y > h: enemybullets.remove(b)

	for a in invaderslist:

		if a.colliderect(player):
			lives -= 1

			if lives == 0: run = False

	tela.fill(black)

	# draw the bullets of the player and the invaders
	for b in playerbullets:
		pygame.draw.rect(tela, pygame.Color("cyan"), b)
	for b in enemybullets:
		pygame.draw.rect(tela, pygame.Color(220, 20, 60), b)

	count = 0
	while count < lives:
		tela.blit(heart, (count * heart.get_width(), 0))
		count += 1



	# draw the invaders with the functin that i created
	drawinvaders(invaderslist, tela)
	# put the spaceship of the player on the surface
	tela.blit(player_img, player)

	# loop control
	pygame.display.flip()
	pygame.time.delay(10)

# end of the game, if the main loop be ignored
pygame.quit()
