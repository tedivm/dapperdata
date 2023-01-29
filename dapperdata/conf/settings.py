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
            line_string = line.decode("utf-8")
            if "*" in line_string:
                continue
            if line_string.startswith("#"):
                continue
            if "#" in line_string:
                line_string = line_string.split("#")[0]
            line_string = line_string.strip().strip("/")
            if len(line_string) == 0:
                continue
            gitignore_directories.add(line_string)
    if len(gitignore_directories) > 0:
        default_data["exclude_paths"] = set(default_data.get("exclude_paths", [])) | gitignore_directories


class Settings(BaseSettings):

    project_name: str = "pretty-config"
    debug: bool = False

    exclude_paths: List[str] = default_data.get("exclude_paths", [])

    class Config:
        env_prefix = "dapperdata_"
