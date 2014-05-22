#!/usr/bin/python

import pygame
from pygame.locals import *
import time, os, math

def load_png(name):
        """ Load image and return image object"""
        fullname = os.path.join('images', name)
        try:
                image = pygame.image.load(fullname)
                if image.get_alpha is None:
                        image = image.convert()
                else:
                        image = image.convert_alpha()
        except pygame.error, message:
                print 'Cannot load image:', fullname
                raise SystemExit, message
        return image, image.get_rect()

class Ball(pygame.sprite.Sprite):
        """A ball that will move across the screen
        Returns: ball object
        Functions: update, calcnewpos
        Attributes: area, vector"""

        def __init__(self, (x,y), vector):
                pygame.sprite.Sprite.__init__(self)
                self.image, self.rect = load_png('progress.png')
                screen = pygame.display.get_surface()
                self.area = screen.get_rect()
                self.vector = vector
		self.hit = 0
		self.rect.x, self.rect.y = x, y

        def update(self):
                newpos = self.calcnewpos(self.rect,self.vector)
                self.rect = newpos
		(angle,z) = self.vector
		self.vector = (angle,z)

        def calcnewpos(self,rect,vector):
                (angle,z) = vector
                (dx,dy) = (z*math.cos(angle),z*math.sin(angle))
                return rect.move(dx,dy)
def main():
 # Initialise screen
 pygame.init()
 size = w,h = (1280, 720)
 screen = pygame.display.set_mode(size)
 pygame.display.set_caption('Basic Pygame program')     

 # Fill background
 background = pygame.Surface(screen.get_size())
 background = background.convert()
 background.fill((250, 250, 250))

 # Display some text 
 font = pygame.font.Font(None, 36)
 text = font.render("Hello There", 1, (10, 10, 10))
 textpos = text.get_rect()
 textpos.centerx = background.get_rect().centerx
 textpos.centery = background.get_rect().h*0.9
 background.blit(text, textpos) 

 # Blit everything to the screen
 screen.blit(background, (0, 0))
 pygame.display.flip()

 prog = Ball( (int(0.02*w),int(0.85*h)), (0, 19))
 progsprite = pygame.sprite.RenderPlain(prog)

 # Event loop
 progress = 0
 while 1:
  if progress >=100: break
  for event in pygame.event.get():
    if event.type == QUIT:
      return

  screen.blit(background, (0, 0))
  screen.blit(background, prog.rect, prog.rect)
  progsprite.update()
  progsprite.draw(screen)

  text = font.render(str(int(progress))+"%", 1, (10, 10, 10))
  textpos = text.get_rect()
  textpos.centerx, textpos.centery = prog.rect.centerx, prog.rect.centery-15
  screen.blit(text, textpos)
  progress += 2.6

  pygame.display.flip()
  time.sleep(1)

 while 1:
    pass

if __name__ == '__main__': main()

