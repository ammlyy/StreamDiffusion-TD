from StreamDiffusion.utils.wrapper import StreamDiffusionWrapper
from typing import List
import numpy as np

base_model = "stabilityai/sd-turbo"
taesd_model = "madebyollin/taesd"
    
class Pipeline():
    def __init__(self, width=512, height=512, mode="img2img"):
        self.prompt = "a black and white, illustration"
        self.mode = mode
        self.stream = StreamDiffusionWrapper(
            model_id_or_path=base_model,
            use_tiny_vae=taesd_model,
            t_index_list=[25,35],
            frame_buffer_size=1,
            width=width,
            height=height,
            use_lcm_lora=True,
            output_type="np",
            warmup=10,
            vae_id=None,
            mode=mode,
            use_denoising_batch=True,
            cfg_type="none",           
            seed=1

        )

        self.stream.prepare(
            prompt=self.prompt,
            num_inference_steps=50,
        )
    def updateTList(self, t_list:List[int]):
        self.stream.t_index_list = t_list

    def updatePrompt(self, new_prompt):
        if self.prompt != new_prompt.value.decode('utf-8'):
            self.prompt = new_prompt.value.decode('utf-8')
        
        return

    def predict(self, prompt, conditional_image:any) -> np.array:
        self.updatePrompt(prompt)
        if self.mode == "img2img":
            self.stream.preprocess_image(conditional_image)
            return self.stream(conditional_image, self.prompt)
        elif self.mode == "txt2img":
            self.stream(self.prompt)
