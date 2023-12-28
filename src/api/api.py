import sys, os
sys.path.insert(0,"..")

from PIL import Image
import matplotlib.pyplot as plt

from src.config import CONFIG
from src.scoring.metrics import WeightedSum
from src.scoring.scorer import Scorer

import ipywidgets as widgets
from IPython.display import display, clear_output

class Interface:
    def __init__(self):
        
        self.combinations = open(os.path.join(CONFIG.DATA_PATH,"combinations.txt")).read().splitlines()
        self.options = ["wei","acc","trac","spd","han"]
        
        self.sliders = [widgets.FloatSlider(
                            value=7.5,
                            min=0,
                            max=1.0,
                            step=0.1,
                            description=option,
                            disabled=False,
                            continuous_update=False,
                            orientation='horizontal',
                            readout=True,
                            readout_format='.1f',
                        ) for option in self.options]
        
        self.button = widgets.Button(description="Lancer le calcul")
        self.button.on_click(self.on_button_click)
        
        self.output_area = widgets.Output()
        display(widgets.VBox(self.sliders))
        display(self.button)
        display(self.output_area)

    def on_button_click(self, b):
        with self.output_area:
            clear_output(wait=True)
            weights = {option :slider.value for option, slider in zip(self.options, self.sliders)}
            scorer = Scorer(self.combinations,weights)
            res = scorer.get_optimum(WeightedSum)
            print("Level values : ", res["stats"])
            possibility = res['possibilities'][0]
            fig, axes = plt.subplots(1,4,figsize=(15,4))
            components = ["driver","body","tire","glider"]
            for k,component in enumerate(possibility.split("/")):
                axes[k].imshow(Image.open(os.path.join(CONFIG.IMAGES_PATH,f"{component}.png")))
                axes[k].set_axis_off()
                axes[k].set_title(components[k])
            plt.show()

    def run_interface(self):
        display(self)