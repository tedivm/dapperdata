import os
import sys
from typing import List

from pydantic import BaseSettings

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

default_data = {}
if os.path.exists("pyproject.toml"):
    with open("pyproject.toml", "rb") as f:
        toml_data = tomllib.load(f)
    default_data.update(toml_data.get("tool", {}).get("pretty-config", {}))


if os.path.exists(".gitignore"):
    gitignore_directories = set([])
    with open(".gitignore", "rb") as f:
        for line in f.readlines():
            line = line.decode("utf-8")
            if "*" in line:
                continue
            if line.startswith("#"):
                continue
            if "#" in line:
                line = line.split("#")[0]
            line = line.strip().strip("/")
            if len(line) == 0:
                continue
            gitignore_directories.add(line)
    if len(gitignore_directories) > 0:
        default_data["exclude_paths"] = set(default_data.get("exclude_paths", [])) | gitignore_directories


class Settings(BaseSettings):

    project_name: str = "pretty-config"
    debug: bool = False

    exclude_paths: List[str] = default_data.get("exclude_paths", [])

    class Config:
        env_prefix = "PRETTY_CONFIG_"
