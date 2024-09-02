import os
import shutil
import yaml
import sysconfig
import time
import zipfile
import threading
from tqdm import tqdm
import comfy.utils


comfy_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
custom_nodes_path = os.path.join(comfy_path, "custom_nodes")

# 用户主目录
home_directory = os.path.expanduser("~")
python_install_path = sysconfig.get_path('platlib')

# 配置文件基础目录
config_file = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(config_file, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
    
basic_path = config['basic_path']

dividing_line = "----------------------------------------------"

# 自定义异常类
class Error(Exception):
    pass


# 路径输出 完成度100%
class PathOutput:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "base_dir": (
                    ["BasicPath", "ComfyUI",  "custom_nodes", "models", "checkpoints", "loras", "vae", "input", "output", "UserHome", "site-packages"], {"default": "BasicPath"}
                ),
                "subpaths": ("STRING", {"multiline": True})
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("paths",)

    FUNCTION = "_path_output"
    # OUTPUT_IS_LIST = (True,)
    #OUTPUT_NODE = False
    CATEGORY = "ToolBox/FileManager"

    def _path_output(self, base_dir, subpaths):
        subpaths = subpaths.strip().split('\n')
        # 过滤掉空行
        subpaths = [subpath.strip() for subpath in subpaths if subpath.strip()]
        
        if base_dir == "BasicPath":
            basic_dir_path = basic_path
        elif base_dir == "UserHome":
            basic_dir_path = home_directory
        elif base_dir == "ComfyUI":
            basic_dir_path = comfy_path
        elif base_dir in ["custom_nodes", "models", "input", "output"]:
            basic_dir_path = os.path.join(comfy_path, base_dir)
        elif base_dir == "site-packages":
            basic_dir_path = python_install_path
        else:
            basic_dir_path = os.path.join(comfy_path, "models", base_dir)
            
        if not subpaths:
            absolute_paths = basic_dir_path
        else:
            absolute_paths = []
            for subpath in subpaths:
                subpath = subpath.strip()
                target_absolute_path = os.path.join(basic_dir_path, subpath)
                absolute_paths.append(target_absolute_path)
            absolute_paths = "\n".join(absolute_paths)
        return (absolute_paths,)

# 创建路径 完成度95%
class CreatePaths:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_paths": ("STRING", {"forceInput": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_paths",)

    FUNCTION = "creat_paths"
    CATEGORY = "ToolBox/FileManager"

    def creat_paths(self, input_paths):
        input_paths = input_paths.strip().split('\n')
        # 过滤掉空行
        target_paths = [input_path.strip() for input_path in input_paths if input_path.strip()]
            
        if not target_paths:
            raise Error("Input path is empty, please enter the path")
        else:
            absolute_paths = []
            for target_path in target_paths:
                target_path = target_path.strip()
                if not os.path.exists(target_path):
                    os.makedirs(target_path)
                    print(f"{target_path} does not exist, automatically created")
                else:
                    print(f"{target_path} already exists, no need to create")
                absolute_paths.append(target_path)
            absolute_paths = "\n".join(absolute_paths)
        return (absolute_paths,)

NODE_CLASS_MAPPINGS = {
    "PathOutput": PathOutput,
    "CreatePaths": CreatePaths
}