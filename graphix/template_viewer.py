import dataclasses

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from models.img_template import Portfolio
from models.img_template import ImgProfile
from models.img_template import ImgTemplate
from models.img_template import load_portfolio


@dataclasses.dataclass(frozen=True)
class ViewSetting:
    color_map: dict[str, str]
    show: bool


def show_profile(prof: ImgProfile, view_setting):
    img = Image.open(prof.path)

    arr = np.asarray(img)
    print(arr)


if __name__ == "__main__":
    path = "portfolio.yaml"
    port = load_portfolio(path)
    show_profile(port.profiles[0], None)
