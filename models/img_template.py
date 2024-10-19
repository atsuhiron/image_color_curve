from __future__ import annotations
import dataclasses


@dataclasses.dataclass(frozen=True)
class ImgTemplate:
    name: str
    role: str
    ullr: list[int]

    def __post_init__(self):
        if len(self.ullr) != 4:
            raise ValueError("The length of ullr must be 4")

    @property
    def upper(self) -> int:
        return self.ullr[0]

    @property
    def lower(self) -> int:
        return self.ullr[1]

    @property
    def left(self) -> int:
        return self.ullr[2]

    @property
    def right(self) -> int:
        return self.ullr[3]

    @staticmethod
    def from_json_dict(d: dict) -> ImgTemplate:
        return ImgTemplate(d["name"], d["role"], d["ullr"])


@dataclasses.dataclass(frozen=True)
class ImgProfile:
    path: str
    templates: list[ImgTemplate]

    def get_name_set(self) -> set[str]:
        return set(temp.name for temp in self.templates)

    @staticmethod
    def from_json_dict(d: dict) -> ImgProfile:
        return ImgProfile(d["path"], [ImgTemplate.from_json_dict(temp) for temp in d["templates"]])


@dataclasses.dataclass(frozen=True)
class Portfolio:
    default_templates: list[ImgTemplate]
    profiles: list[ImgProfile]

    @staticmethod
    def from_json_dict(d: dict) -> Portfolio:
        default_templates = [ImgTemplate.from_json_dict(temp) for temp in d["default_templates"]]
        temp_name_set = set(temp.name for temp in default_templates)

        profile_d_list = d.get("profile")
        if profile_d_list is None:
            return Portfolio(default_templates, [])

        profiles = []
        for prof_json in profile_d_list:
            prof = ImgProfile.from_json_dict(prof_json)
            name_set = prof.get_name_set()
            if temp_name_set != name_set:
                raise ValueError(f"Invalid template name in the ImgProfile(path={prof.path})")
            profiles.append(prof)

        return Portfolio(default_templates, profiles)
