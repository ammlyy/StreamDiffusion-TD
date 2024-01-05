from OpenGL.GL import *
import numpy as np
import pygame
from pygame.locals import *

def setupGL(window_w, window_h):
    # window details
    width = window_w
    height = window_h
    display = (width,height)
    
    # window setup
    pygame.init() 
    pygame.display.set_caption('Spout IN/OUT')
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    # OpenGL init
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0,width,height,0,1,-1)
    glMatrixMode(GL_MODELVIEW)
    glDisable(GL_DEPTH_TEST)
    glClearColor(0.0,0.0,0.0,0.0)
    glEnable(GL_TEXTURE_2D)


def initReceiver(id, w, h):
    glBindTexture(GL_TEXTURE_2D, id)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    glBindTexture(GL_TEXTURE_2D, id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)

def copyToTexture(data:np.ndarray, textureId:any)->void:
        glBindTexture(GL_TEXTURE_2D, textureId);
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        # copy output into texture
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGB, data.shape[0], data.shape[1], 0, GL_RGB, GL_UNSIGNED_BYTE, data )
        

def draw(spoutReceiverWidth, spoutReceiverHeight):
        glClear(GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT )
        glLoadIdentity()
        glBegin(GL_QUADS)

        glTexCoord(0,0)        
        glVertex2f(0,0)

        glTexCoord(1,0)
        glVertex2f(spoutReceiverWidth,0)

        glTexCoord(1,1)
        glVertex2f(spoutReceiverWidth,spoutReceiverHeight)

        glTexCoord(0,1)
        glVertex2f(0,spoutReceiverHeight)
        glEnd()


