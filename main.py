import pygame
import math
import numpy
import os
import time


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF)
clock = pygame.time.Clock()
running = True
restart = False
screenWidth, screenHeight = screen.get_size()
boat = pygame.image.load("boat.png")
boat = pygame.transform.scale(boat, (853 / 5, 404 / 5))
dPressed = False
aPressed = False
boatOperational = True

boxes = [
    [pygame.Rect(150, 150, 50, 50), False, False, 0, 0, 0]
]

levels = [
    {
        "obstacles": [],
        "objects": [],
        "buttonPos": ()
    },
    {
        "obstacles": [],
        "objects": [],
        "buttonPos": ()
    }
]

gravitationalConstant = 5 # Meters/Second^2
massOfEarth = 59 # Kilograms
radiusOfEarth = 6378 # Kilometers
boatRotation = 0

def blitRotate(surf, image, pos, originPos, angle):

    # offset from pivot to center
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    
    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

    # rotate and blit the image
    surf.blit(rotated_image, rotated_image_rect)
  
    # draw rectangle around the image
    # pygame.draw.rect(surf, (255, 0, 0), (*rotated_image_rect.topleft, *rotated_image.get_size()),2)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                boxes[0][4] += 20
                dPressed = True
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                running = False
                restart = True
            if event.key == pygame.K_a:
                boxes[0][4] -= 10
                aPressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                boxes[0][4] -= 20
                dPressed = False
            if event.key == pygame.K_a:
                boxes[0][4] += 10
                aPressed = False

    dt = clock.tick(60) / 1000
    if boatOperational:
        for i in boxes:
            box = i[0]
            bouyuancy = 0
            drag = 0.5 * 1 * abs(i[3]) ** 5 * 0.0001

            acceleration = box.y + (gravitationalConstant * massOfEarth / radiusOfEarth ** 2) / dt

            if box.y + 25 > screenHeight / 2:
                i[1] = True
                OldValue = box.y - screenHeight / 2
                OldMin = screenHeight / 2
                OldMax = screenHeight
                NewMin = 0
                NewMax = 1
                factor = 1 + ((((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin)
                factor = numpy.clip(factor, 0, 1)
                bouyuancy = -1 * acceleration * 30 * factor
                if i[3] < 0:
                    i[3] += drag * dt
                else:
                    i[3] -= drag * dt
            else:
                i[1] = False
                OldValue = -(box.y - screenHeight / 2)
                OldMin = 0
                OldMax = screenHeight / 2
                NewMin = 0
                NewMax = 1
                factor = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
                factor = numpy.clip(factor, 0, 1)
                i[3] += acceleration * factor * dt
                
            i[3] += bouyuancy * dt
            i[3] = numpy.clip(i[3], -400, 400)
            
            if i[1] == True and i[2] == False:
                i[3] *= 0.5
                i[3] = numpy.clip(i[3], 0, 400)
            
            i[2] = i[1]

            i[5] += i[4]

            if i[5] > 0:
                i[5] -= 5
                i[5] = numpy.clip(i[5], 0, 400)
            else:
                i[5] += 5
                i[5] = numpy.clip(i[5], -400, 0)

            box.y += i[3]
            box.x += i[5] * dt

    if boatOperational:
        if dPressed == True:
            boatRotation += 0.5
            if boxes[0][0].y + 25 > screenHeight / 2:
                boxes[0][3] -= 1.5
            if boatRotation > 30:
                boatOperational = False
        else:
            boatRotation -= 1
            boatRotation = numpy.clip(boatRotation, 0, 30)
    else:
        boatRotation += 5
        boatRotation = numpy.clip(boatRotation, 0, 180)
        boxes[0][0].y += 2
        if boxes[0][0].y >= screenHeight:
            running = False
            restart = True

    screen.fill("black")
    for box in boxes:
        # pygame.draw.rect(screen, (255, 255, 255), box[0])
        # screen.blit(boat, (box[0].x - 30, box[0].y - 404 / 10))
        w, h = boat.get_size()
        blitRotate(screen, boat, (box[0].x - 30, box[0].y - 404 / 10 + 35), (w / 2, h / 2), boatRotation)
    s = pygame.Surface((screenWidth, screenHeight / 2), pygame.SRCALPHA)
    s.fill((0, 50, 255, 128))
    screen.blit(s, (0, screenHeight / 2))

    pygame.display.flip()

    clock.tick(2320948230984)

pygame.quit()

if restart:
    os.system("python main.py")