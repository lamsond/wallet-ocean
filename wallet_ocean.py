#Cora's Wallet Ocean
import pygame, sys, random

#game constants
WIN_WIDTH = 987
WIN_HEIGHT = 610
FPS = 30
WAVE_RAD = 30
WAVE_FACTOR = 1.6
WAVE_SPEED = 1
WAVE_LENGTH = int(WAVE_RAD * WAVE_FACTOR)
CHILL_TIME = 120 #let water height unchanged
SINK_SOURCE_TIME = 180 #raise or lower time
PHI = 1.618 #golden ratio
MAX_WATER_HEIGHT = -15
MIN_WATER_HEIGHT = WIN_HEIGHT/2 + 34 
SHARK_THRESHOLD = 40 #triggers shark_bait mode
COLOR_FRAMES = 5 #how often color updates

#rgb color constants
NIGHT = (11, 22, 33)
OCEAN = (0, 153, 202)
BLOOD_OCEAN = (153, 0, 49)

#game vars
water_height = int(WIN_HEIGHT/(PHI+1))
wave_x = 0
sink_count = 0
sink_dir = 0
water_color = OCEAN
shark_bait = False
color_counter = 0

#init game spacetime
pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Cora's Wallet Ocean")
clock = pygame.time.Clock()

#return image to given file path and scale factor
def init_image(path, sf):
	img = pygame.image.load(path)
	(w, h) = img.get_size()
	img = pygame.transform.scale(img, (int(sf*w), int(sf*h)))
	return img

#draw waves and night sky
def draw_ocean(surf, x, clr):
	surf.fill(clr)
	n = int(WIN_WIDTH/WAVE_LENGTH)+3
	for i in range(n):
		pygame.draw.circle(surf, NIGHT, (WAVE_LENGTH*(i-1) + x, water_height), WAVE_RAD)
	pygame.draw.rect(surf, NIGHT, (0, 0, WIN_WIDTH, water_height))

#creates scrolling wave effect
def move_wave(x):
	if x > 0:
		x -= WAVE_SPEED
	else:
		x = WAVE_LENGTH
	return x

#randomized water height
def update_water_height(y):
	global sink_count, sink_dir
	if sink_count >= SINK_SOURCE_TIME:
		sink_count = 0
		sink_dir = 0
	elif sink_count == CHILL_TIME:
		if water_height < MAX_WATER_HEIGHT:
			sink_dir = 1
		elif water_height > MIN_WATER_HEIGHT:
			sink_dir = -1
		else:
			sink_dir = random.choice([-1, 0, 1])
		sink_count += 1
	else:
		sink_count += 1
	y += sink_dir
	return y
	
#randomized water color and shark bait trigger
def update_water_color(clr):
	global shark_bait
	reset = False
	r = random.choice([-2, -1, 0, 1, 2])
	if shark_bait and clr[0] < BLOOD_OCEAN[0]:
		r = 1
	elif shark_bait and clr[0] >= BLOOD_OCEAN[0]:
		r = -1
		shark_bait = False
		reset = True
	elif not shark_bait and clr[0] <= OCEAN[0]+1:
		r = 1
	elif not shark_bait and clr[0] >= SHARK_THRESHOLD:
		r = 1
		shark_bait = True
	red = clr[0]+r
	green = clr[1]-r
	blue = clr[2]-r
	new_color = (red, green, blue)
	if reset:
		new_color = OCEAN
	return new_color

HAPPY_SQUID = init_image("SquidPink.png", 0.2)
CRAZY_SQUID = init_image("SquidOrange.png", 0.2)
GATOR_CORN = init_image("GatorCorn.png", 0.2)
SHARK = init_image("GatorCorn.png", 0.2)

class HappySquid():
	def __init__(self, x, y):
		self.img = HAPPY_SQUID
		self.x = x
		self.y = y
		self.dir_y = -1
		self.speed_x = 3
		self.speed_y = 5
		
	def draw(self, surf):
		surf.blit(self.img, (self.x, self.y))
	
	def move(self):
		if self.x < 0 - 50:
			self.x = WIN_WIDTH
		self.x -= self.speed_x
		if self.y > WIN_HEIGHT - 250 or self.y <= water_height+13:
			self.dir_y *= -1
		self.y += self.speed_y * self.dir_y

class CrazySquid():
	def __init__(self, x, y):
		self.img = CRAZY_SQUID
		self.x = x
		self.y = y
		self.dir_y = -1
		self.speed_x = 3
		self.speed_y = 5
		
	def draw(self, surf):
		surf.blit(self.img, (self.x, self.y))
	
	def move(self):
		if self.x < 0 - 50:
			self.x = WIN_WIDTH
		self.x -= self.speed_x
		if self.y > WIN_HEIGHT - 250 or self.y <= water_height+13:
			self.dir_y *= -1
		self.y += self.speed_y * self.dir_y
		
bob = HappySquid(WIN_WIDTH, WIN_HEIGHT/2)		
crazy_bob = CrazySquid(WIN_WIDTH/2, WIN_HEIGHT-300)

#game loop
while True:
	draw_ocean(screen, wave_x, water_color)
	bob.draw(screen)
	crazy_bob.draw(screen)
	wave_x = move_wave(wave_x)
	water_height = update_water_height(water_height)
	if color_counter >= COLOR_FRAMES:
		water_color = update_water_color(water_color)
		color_counter = 0
	else:
		color_counter += 1
	bob.move()
	crazy_bob.move()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
			
	pygame.display.update()
	clock.tick(FPS)

