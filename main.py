import pygame
import math
import random
from pygame import mixer



# Initialize pygame

pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))


# background
background = pygame.image.load('C:/Users/Administrator/Pictures/5471985.jpg')
# Title and Icon
pygame.display.set_caption("Space invaders")
icon = pygame.image.load('C:/Users/Administrator/Downloads/extraterrestrial.png')
pygame.display.set_icon(icon)

# background sound
mixer.music.load('C:/Users/Administrator/Downloads/background.wav')
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('C:/Users/Administrator/Downloads/space-invaders (2).png')
# Postions
playerX = 365
playerY = 480
playerX_change = 0


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6 

for i in range(num_of_enemies):
	enemyImg.append(pygame.image.load('C:/Users/Administrator/Downloads/cthulhu.png'))
	# Postions
	enemyX.append(random.randint(0, 735)) #RANDOM POSITION
	enemyY.append(random.randint(50, 150))
	enemyX_change.append(0.3)
	enemyY_change.append(40)


# Bullet
# ready - you cant see the bullet on the screen
# fire - the bullet is currenly moving
bulletImg = pygame.image.load('C:/Users/Administrator/Downloads/bullet (1).png')
# Postions
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = 'ready'

# Score

# Score
score_value = 0
font = pygame.font.Font('C:/Users/Administrator/Downloads/nervous/fonts/Nervous.ttf', 32)

textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('C:/Users/Administrator/Downloads/nervous/fonts/Nervous.ttf', 64)

def show_score(x, y):
	score = font.render("Score :" + str(score_value), True, (240, 248, 255))
	screen.blit(score, (x, y))

def game_over_text():
	over_text = over_font.render("GAME OVER", True, (240, 248, 255))
	screen.blit(over_text, (200, 250))


# .blit means draw
def player(x, y):
	screen.blit((playerImg), (x, y))
	#To draw the image in that position

def enemy(x, y, i):
	screen.blit((enemyImg[i]), (x, y))
	#To draw the image in that position

def fire_bullet(x, y):
	global bullet_state
	bullet_state = 'fire'
	screen.blit(bulletImg, (x+20, y +10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
	distance = math.sqrt((math.pow(enemyX-enemyY, 2)) + (math.pow(enemyY - bulletY, 2)))
	if distance < 27:
		return True
	else:
		return False


# Game loop
running = True
while running:
	#playerY -= 0.1 #Moving space ship, move it on right side by adding, and move it left side by subtracting
	for event in pygame.event.get(): #Store here the keys
		if event.type == pygame.QUIT:
			running = False
		# If key strokes is pressed check whether its right or left.
		if 	event.type == pygame.KEYDOWN: #While pressing
			print("Keystrokes is pressed.")
			if event.key == pygame.K_LEFT:
				"""print("Left arrow is pressed.")"""
				playerX_change = -0.3
			if event.key == pygame.K_RIGHT:
				playerX_change = 0.3
			if event.key == pygame.K_SPACE:
				if bullet_state is "ready":
					bullet_sound = mixer.Sound('C:/Users/Administrator/Downloads/laser.wav')
					bullet_sound .play()
					bulletX = playerX
					fire_bullet(bulletX, bulletY)
					"""print("Right arrow is pressed.")"""
		if event.type == pygame.KEYUP: #If key strokes has been released
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				"""print("Keystrokes has been released.")"""
				playerX_change = 0



	# Change screen
	# RGB = Red, green, blue
	screen.fill((180, 176, 173))

	#background image
	screen.blit((background), (0, 0))
	#LAyer rules

	#Checking for boundaries of spaceship so it doesn't go out of the screen boundary.
	playerX += playerX_change

	if playerX <=0:
		playerX = 0 
	elif playerX >= 736:
		playerX = 736

	# enemy Movement
	for i in range(num_of_enemies):

		#game over
		if enemyY[i] > 200:
			for j in range(num_of_enemies):
				enemyY[j] = 2000
			game_over_text()
			break


		enemyX[i] += enemyX_change[i]

		if enemyX[i] <=0:
			enemyX_change[i] = 0.5 #BOUNDARIES
			enemyY[i] += enemyX_change[i]
		elif enemyX[i] >= 736:
			enemyX_change[i] = -0.5
			enemyY[i] += enemyY_change[i]

		#collision
		collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
		if collision:
			explosion_sound = mixer.Sound('C:/Users/Administrator/Downloads/explosion.wav')
			explosion_sound.play()
			bulletY = 480
			bullet_state = "ready"
			score_value  += 1
			enemyX[i] = random.randint(0, 735)
			enemyY[i] = random.randint(50, 150)

		enemy(enemyX[i], enemyY[i], i)
	# bullet movement
	if bulletY <=0:
		bulletY = 480
		bullet_state = 'ready'

	if bullet_state is "fire":
		fire_bullet(bulletX, bulletY)
		bulletY -= bulletY_change





	player(playerX, playerY) # To show the function player
	show_score(textX, textY)
	pygame.display.update() #To update the screen

