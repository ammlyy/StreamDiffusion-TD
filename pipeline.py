import sys
import PIL
import numpy as np

import torch
from StreamDiffusion.utils.wrapper import StreamDiffusionWrapper
from OpenGL.GL import *

import sys
import os

base_model = "stabilityai/sd-turbo"
taesd_model = "madebyollin/taesd"
    
class Pipeline():
    def __init__(self, width=512, height=512):
        self.prompt = "a black and white illustration"
        
        self.stream = StreamDiffusionWrapper(
            model_id_or_path=base_model,
            use_tiny_vae=taesd_model,
            t_index_list=[0],
            frame_buffer_size=1,
            width=width,
            height=height,
            use_lcm_lora=False,
            output_type="np",
            warmup=10,
            vae_id=None,
            mode="img2img",
            use_denoising_batch=True,
            cfg_type="none",
        )

        self.stream.prepare(
            prompt=self.prompt,
            num_inference_steps=1,
        )


    def updatePrompt(self, new_prompt):
        if self.prompt != new_prompt.value.decode('utf-8'):
            self.prompt = new_prompt.value.decode('utf-8')
        
        return

    def draw(self, prompt, conditional_image:np.ndarray) -> PIL.Image:
        self.updatePrompt(prompt)
        tensor = (torch.from_numpy(conditional_image).to(device='cuda', dtype=torch.float16)) / 255.
        return self.stream(tensor, self.prompt)
    
