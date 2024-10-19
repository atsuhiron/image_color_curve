import glob
import dataclasses

import yaml

from models.img_template import Portfolio
from models.img_template import ImgProfile


def _load(path: str) -> Portfolio:
    with open(path, "r") as f:
        d = yaml.safe_load(f)
    return Portfolio.from_json_dict(d["portfolio"])


def init_from_default_template(default_template_path: str, new_path: str, image_glob_pattern: str):
    default_temp = _load(default_template_path)
    profiles = []
    for i_path in glob.iglob(image_glob_pattern):
        profiles.append(
            ImgProfile(i_path, default_temp.default_templates)
        )

    new_port = Portfolio(default_temp.default_templates, profiles)
    new_dict = dataclasses.asdict(new_port)
    with open(new_path, "w") as fw:
        yaml.dump(new_dict, fw)


if __name__ == "__main__":
    init_from_default_template(
        "portfolio_def2.yaml",
        "portfolio.yaml",
        "feet/*.JPG"
    )
