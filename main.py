import multiprocessing
import time
import numpy as np
import pygame
from pythonosc import osc_server
from Library.PySpout import SpoutReceiver, SpoutSender
from pygame.locals import *
from OpenGL.GL import *
from pipeline import Pipeline
from glUtils import copyToTexture, initReceiver, setupGL, draw

DEBUG_FPS = False
MAX_LENGTH = 100
SCREEN_ID = 0

def osc_manager(prompt):
    def update_prompt(address, shm, *args):
        new_value   = str(args[0])
        shm[0].value = new_value.encode('utf-8').ljust(MAX_LENGTH)
        return
        
    dispatcher = osc_server.Dispatcher()
    dispatcher.map('/update_prompt', update_prompt, prompt)

    server = osc_server.ThreadingOSCUDPServer(
        ('127.0.0.1', 8000), dispatcher)
    
    print("Serving on {}".format(server.server_address))
    server.serve_forever()


def main(prompt):
    w:int= 512
    h:int = 512
    setupGL(w, h)
    pipeline = Pipeline(w, h)
    spoutReceiver = SpoutReceiver("imgCondition", w, h)
    spoutSender = SpoutSender("SD", w, h, GL_RGB)

    # create textures for spout receiver and spout sender 
    textureSendID, textureReceiveID = glGenTextures(2)
    print("SEND ID: ", textureSendID, "Receive ID: ", textureReceiveID)

    # initalise receiver texture
    initReceiver(textureReceiveID, w, h)
    
    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("exiting")
                spoutReceiver.release()
                pygame.quit()
                quit()
        
        #receive
        glBindTexture(GL_TEXTURE_2D, textureReceiveID)
        if not spoutReceiver.receive_texture(textureReceiveID, GL_TEXTURE_2D):
            print("texture not received. closing")
            break
        data = glGetTexImage(GL_TEXTURE_2D, 0, GL_RGB, GL_UNSIGNED_BYTE)
        data = np.frombuffer(data, dtype=np.uint8).reshape((1, 3, h, w)).copy() # 1 x channels x w x h
        
        #generate
        start_time = time.time() # start time of the loop
        result = pipeline.draw(prompt, data)
        copyToTexture((result * 255).astype(np.uint8), textureSendID)
        
        
        if DEBUG_FPS:
            print("FPS: ", 1.0 / (time.time() - start_time)) # FPS = 1 / time to process loop
        
        # setup window to draw to screen
        glActiveTexture(GL_TEXTURE0)
        draw(w, h)
        pygame.display.flip()        
        
        #send
        if not spoutSender.send_texture(textureSendID, GL_TEXTURE_2D):
            print("Send failed. Exiting")
            break

if __name__ == "__main__":
    prompt = multiprocessing.Array('c', b'a cat'.ljust(MAX_LENGTH))

    # Create an OSC server
    osc_server_process = multiprocessing.Process(target=osc_manager, args=(prompt,))
    osc_server_process.start()

    # Create a separate process for the task
    separate_task_process = multiprocessing.Process(target=main, args=(prompt,))
    separate_task_process.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        osc_server_process.terminate()
        separate_task_process.terminate()
