from Library.PySpout import SpoutReceiver, SpoutSender
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.framebufferobjects import *
from OpenGL.GLU import *

SCREEN_ID = 0

def draw(spoutReceiverWidth, spoutReceiverHeight):
        # clean start
        glClear(GL_COLOR_BUFFER_BIT  | GL_DEPTH_BUFFER_BIT )
        # reset drawing perspective
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

def main():
    # window details
    width = 512
    height = 512
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

    spoutReceiver = SpoutReceiver("imgConditions", 512, 512)
    spoutSender = SpoutSender("SD", 512, 512, GL_RGB)

    # init spout receiver
    spoutReceiverWidth = 512
    spoutReceiverHeight = 512

    # create textures for spout receiver and spout sender 
    textureSendID, textureReceiveID = glGenTextures(2)

    print("SEND ID: ", textureSendID, "Receive ID: ", textureReceiveID)
    # initalise receiver texture
    glBindTexture(GL_TEXTURE_2D, textureReceiveID)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    glBindTexture(GL_TEXTURE_2D, textureReceiveID)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, spoutReceiverWidth, spoutReceiverHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)
    glBindTexture(GL_TEXTURE_2D, SCREEN_ID)

    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("exiting")
                spoutReceiver.release()
                pygame.quit()
                quit()
        
        glBindTexture(GL_TEXTURE_2D, textureReceiveID)

        if not spoutReceiver.receiveTexture(textureReceiveID, GL_TEXTURE_2D):
            print("texture not received. closing")
            break
        
        data = glGetTexImage(GL_TEXTURE_2D, 0, GL_RGB, GL_UNSIGNED_BYTE, outputType=None)
        
        glBindTexture(GL_TEXTURE_2D, textureSendID);
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        # copy output into texture
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGB, 512, 512, 0, GL_RGB, GL_UNSIGNED_BYTE, data )
        
        # setup window to draw to screen
        glActiveTexture(GL_TEXTURE0)
        draw(spoutReceiverWidth, spoutReceiverHeight)
        
        # update window
        pygame.display.flip()        
        if not spoutSender.sendTexture(textureSendID, GL_TEXTURE_2D):
            print("Send failed. Exiting")
            break

if __name__ == '__main__':
    main()