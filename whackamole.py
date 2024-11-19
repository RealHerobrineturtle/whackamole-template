import pygame
import random
posX = 0
posY = 0
mole_image = pygame.image.load("mole.png")

def movement():
    #I HAD WANTED TO USE A FUNCTION FOR MOVEMENT AND HAD TO LOOK UP WHY MY CODE WASN'T WORKING
    #I don't like this
    global posX, posY
    posX = random.randrange(0, 20) * 32
    posY = random.randrange(0, 16) * 32

def main():
    try:
        pygame.init()
        # You can draw the mole with this snippet:
        # screen.blit(mole_image, mole_image.get_rect(topleft=(x,y)))
        screen = pygame.display.set_mode((640, 512))
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    xPosMouse, yPosMouse = event.pos
                    #The User might miss the mole, but clicks the square. I am accounting for that
                    if posX <= xPosMouse < posX + 32 and posY <= yPosMouse < posY + 32:
                        movement()
            screen.fill("light green")
            for x in range(0, 640, 32):
                pygame.draw.line(screen, "black", (x, 0), (x, 512))
            for y in range(0, 512, 32):
                pygame.draw.line(screen, "black", (0, y), (640, y))
            screen.blit(mole_image, mole_image.get_rect(topleft= (posX,posY)))
            pygame.display.flip()
            clock.tick(60)
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
