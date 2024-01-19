# StreamDiffusion-TD
### TouchDesigner x StreamDiffusion Integration via Spout2
This project provides a TouchDesigner workflow for seamless integration with Streamdiffusion using Spout2 texture sharing. StreamdDiffusion enhance the diffusion process by making it almost real time, and this integration allows users to incorporate it directly into their TouchDesigner projects.

## Prerequisites
Before using this integration, ensure that you have the following software installed:

- TouchDesigner (tested using 2023.11280)
- Spout2 SDK (https://spout.zeal.co/)


## Setup Instructions
1. Clone the repository
```
git clone https://github.com/ammlyy/StreamDiffusion-TD.git
cd StreamDiffusion-TD
git submodule update --init
```

2. Setup StreamDiffusion environment.
   Please follow instructions on their github page.

   After having installed them, the additional libraries needed:
   ```
   conda activate YOUR_JUST_CREATED_ENV
   pip install PyOpenGL PyOpenGL_accelerate
   pip install pygame
   ```

4. Open the .toe project

4. Launch the main.py script


## Additional info
This projects make use of a custom Spout2-Python binding. There were alternatives, such as [Python-SpoutGL]([https://github.com/jlai/Python-SpoutGL), but I preferred starting from a simplest solution originally released as [PySpout](https://github.com/Off-World-Live/pyspout) and added missing bindings to have a look of what were going on under the hood.

## Contributing
If you encounter issues or have suggestions for improvements, feel free to open an issue or submit a pull request. Your contributions are welcome!

## License
This project is licensed under the Apache 2.0 License, allowing for open collaboration and sharing.

