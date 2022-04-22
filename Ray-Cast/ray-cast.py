from Wall import Wall
import pygame
import random
import sys
import math
pygame.init()

WIDTH = 1600
HEIGHT = 900
framerate = 60 # 0 -> as fast as possible, n -> n/second
window = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

controlStyle = 0

eye = (WIDTH/2,HEIGHT/2)
fovDeg = (150, 210)
maxDist = 1000
move = (0,0)
moveSpeed = 3
rotate = 0
fovChange = 0

walls = []
walls.append(Wall(0,0,WIDTH,0))
walls.append(Wall(WIDTH,0,WIDTH,HEIGHT))
walls.append(Wall(WIDTH,HEIGHT,0,HEIGHT))
walls.append(Wall(0,HEIGHT,0,0))
for _ in range(5):
	walls.append(Wall(WIDTH,HEIGHT))

def main():
	while True:
		pygame.draw.rect( window, (0,0,0), (0,0,WIDTH,HEIGHT)) # update bg

		draw3DWalls()
		drawBirdView()
		controls()

		# update window
		clock.tick(framerate)
		pygame.display.update()

def offSet(rad):
	return (math.cos(rad) * maxDist, math.sin(rad) * maxDist)

def drawBirdView():
	for n in range(fovDeg[0],fovDeg[1]):
		circ = offSet(math.radians(n))
		endpoint = (eye[0] + circ[0], eye[1] + circ[1])
		for w in walls:
			check = w.hit(eye, endpoint)
			if check:
				if math.dist(check, eye) < math.dist(endpoint, eye):
					endpoint = check
		pygame.draw.aaline( window, (255,255,100), eye, endpoint, 10)

	for w in walls:
		pygame.draw.aaline( window, (255,100,100), w.p1, w.p2)

def draw3DWalls():
	r = fovDeg[1] - fovDeg[0]
	subAngle = math.ceil(WIDTH/r)

	for n in range(fovDeg[0],fovDeg[1]):
		for i in range(subAngle):
			circ = offSet(math.radians(n+i/subAngle))
			endpoint = (eye[0] + circ[0], eye[1] + circ[1])
			dist = maxDist
			wallEdge = False
			for w in walls:
				check = w.hit(eye, endpoint)
				if check:
					if math.dist(check, eye) <= dist:

						endpoint = check
						
						if math.dist(endpoint, w.p1) < 1 or math.dist(endpoint, w.p2) < 1 or dist < 1:
							wallEdge = True
						else:
							wallEdge = False

						dist = math.dist(endpoint, eye)
						

			dAngled = dist * math.cos(math.radians((n-fovDeg[0])))
			dAngled = abs(dAngled)
			if dAngled > maxDist:
				dAngled = maxDist
			dRatio = ( maxDist - dAngled ) / maxDist * 255
			if wallEdge:
				dRatio = 255

			

			x = ( n - fovDeg[0] ) * subAngle + i
			y = HEIGHT / 2 - ( maxDist - dAngled ) / 2
			h = ( maxDist - dAngled )

			pygame.draw.rect( window, (dRatio,dRatio,dRatio), (x,y,1,h))

def controls():
	global eye
	global move
	global fovDeg
	global rotate
	global fovChange

	horz = move[0]
	vert = move[1]
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		
		if controlStyle == 0:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w:
					vert = -moveSpeed
				if event.key == pygame.K_a:
					horz = -moveSpeed
				if event.key == pygame.K_s:
					vert = moveSpeed
				if event.key == pygame.K_d:
					horz = moveSpeed

				if event.key == pygame.K_UP:
					rotate = -1
				if event.key == pygame.K_DOWN:
					rotate = 1

				if event.key == pygame.K_LEFT:
					fovChange = 1
				if event.key == pygame.K_RIGHT:
					fovChange = -1

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_w:
					vert = vert + moveSpeed
				if event.key == pygame.K_a:
					horz = horz + moveSpeed
				if event.key == pygame.K_s:
					vert = vert - moveSpeed
				if event.key == pygame.K_d:
					horz = horz - moveSpeed

				if event.key == pygame.K_UP:
					rotate = 0
				if event.key == pygame.K_DOWN:
					rotate = 0
				if event.key == pygame.K_LEFT:
					fovChange = 0
				if event.key == pygame.K_RIGHT:
					fovChange = 0

	if controlStyle == 1:
		eye = pygame.mouse.get_pos()
		fovDeg = (fovDeg[0]+1, fovDeg[1]+1)

	move = (horz,vert)
	eye = (eye[0] + move[0], eye[1] + move[1])

	fovDeg = (fovDeg[0]+rotate, fovDeg[1]+fovChange+rotate)

	if fovDeg[1] <= fovDeg[0]:
		fovDeg = (fovDeg[0],fovDeg[0]+1)


main()