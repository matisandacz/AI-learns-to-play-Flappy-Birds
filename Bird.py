import pygame
import os

bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]

class Bird:

    MAX_ROTATION = 25
    ROT_VEL = 20
    JUMP_VELOCITY = -10.5
    ANIMATION_TIME = 5
    IMGS = bird_images

    def __init__(self, x, y):
        """
        x : starting x pos (int)
        y : starting y pos (int)
        """
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        """
        Makes bird jump
        """
        self.tick_count = 0
        self.vel = self.JUMP_VELOCITY
        self.height = self.y #records height from where bird jumped.
    
    def move(self):

        """
        Calculates bird new position based on velocity and tick_count.
        """

        self.tick_count += 1
        displacement = self.vel*(self.tick_count) + (3/2)*(self.tick_count)**2

        if displacement < 0:
            displacement -= 2

        if displacement >= 16:
            displacement = 16

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50: #tilt up
            self.tilt = self.MAX_ROTATION 
        else: #tilt down
            if self.tilt > -85:
                self.tilt -= self.ROT_VEL

    def draw(self, win):

        """
        Draws flapping animation and tilt
        """

        self.img_count += 1

        # makes the bird flap
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # if diving, it does not flap. 
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2


        # draw and tilt bird
        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


def blitRotateCenter(surf, image, topleft, angle):
    """
    Rotate a surface and blit it to the window
    :param surf: the surface to blit to
    :param image: the image surface to rotate
    :param topLeft: the top left position of the image
    :param angle: a float value for angle
    :return: None
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)
