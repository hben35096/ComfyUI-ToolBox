import os
import shutil
import codewithgpu as cg

basic_path = '/root'

# AutoDL 文件下载
class AutoDLDownload:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "download_link": ("STRING", {"multiline": True}),
                "save_path": ("STRING", {"multiline": True}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "move_files": ("BOOLEAN", {"default": False, "label_on": "enable", "label_off": "disable"}),
            },
        }

    RETURN_TYPES = ("STRING",)

    FUNCTION = "cg_download"

    #OUTPUT_NODE = False
    CATEGORY = "ToolBox"

    def cg_download(self, download_link, save_path, seed, move_files):
        download_link = download_link.strip()
        save_path = save_path.strip()
        target_path = os.path.join(basic_path, save_path)
        
        subfolder_name = download_link.split('/')[1]
        subfolder_path = os.path.join(target_path, subfolder_name)
        if not download_link:
            hint = "下载失败, 请填写下载链接"
        else:
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            os.chdir(target_path)
            cg.model.download(download_link)
            
            if move_files:
                try:
                    for item in os.listdir(subfolder_path):
                        if not item.startswith("."): 
                            shutil.move(os.path.join(subfolder_path, item), target_path)
                    shutil.rmtree(subfolder_path)
                    hint = f"下载已成功下载到 {subfolder_path}, 并迁移至 {target_path}"
                except Exception as e:
                    hint = f"迁移失败, 错误信息: {str(e)}"
            else:
                hint = f"文件已下载到: {subfolder_path} 目录下!"
        
        return (hint, int(seed), )

# 查看目录下的文件
class FolderViewe:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "target_path": ("STRING", {"multiline": True}),
                "include_hidden": ("BOOLEAN", {"default": False, "label_on": "enable", "label_off": "disable"}),
            },
        }

    RETURN_TYPES = ("STRING",)

    FUNCTION = "check_folder"
    # OUTPUT_IS_LIST = (True,)
    #OUTPUT_NODE = False
    CATEGORY = "ToolBox"

    def check_folder(self, target_path, include_hidden):
        target_path = target_path.strip()
        target_absolute_path = os.path.join(basic_path, target_path)
        
        if not os.path.exists(target_absolute_path):
            hint = f"{target_path} 不是有效的路径，请核实后再从新输入"
        else:
            try:
                files_list = os.listdir(target_absolute_path)
                files_to_show = []
                for file in files_list:
                    if include_hidden or not file.startswith('.'):
                        files_to_show.append(file)
                files_to_show = "\n".join(files_to_show)
                hint = files_to_show
            except Exception as e:
                hint = f"无法查看文件：{e}"

        return (hint,)
    
class FolderDeleter:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "target_path": ("STRING", {"multiline": True}),
                "file_name": ("STRING", {"multiline": True}),
            },
        }

    RETURN_TYPES = ("STRING",)

    FUNCTION = "file_deleter"
    # OUTPUT_IS_LIST = (True,)
    #OUTPUT_NODE = False
    CATEGORY = "ToolBox"

    def file_deleter(self, target_path, file_name):
        target_path = target_path.strip()
        target_absolute_path = os.path.join(basic_path, target_path)
        
        file_name = file_name.strip()
        files_to_delete = file_name.split('\n')  # 按行分割
        
        results = []
        
        if not os.path.exists(target_absolute_path):
            results.append(f"{target_path} 不是有效的路径，请核实后再重新输入")
        elif not file_name:
            results.append("请填写目标路径下的文件名/文件夹名")
        else:
            for file_or_dir in files_to_delete:
                if not file_or_dir:  # 跳过空行
                    continue
                full_path = os.path.join(target_absolute_path, file_or_dir)
                try:
                    if os.path.islink(full_path): 
                        os.unlink(full_path)
                        results.append(f"成功删除符号链接: {file_or_dir}")
                    elif os.path.isfile(full_path): 
                        os.remove(full_path)
                        results.append(f"成功删除文件: {file_or_dir}")
                    elif os.path.isdir(full_path):  # 目录（含子文件/子目录）
                        shutil.rmtree(full_path)
                        results.append(f"成功删除文件夹: {file_or_dir}")
                    else:
                        results.append(f"{full_path} 不是有效的文件或目录")
                except Exception as e:
                    results.append(f"删除文件 {file_or_dir} 出错: {e}")
        
        return ("\n".join(results),)

NODE_CLASS_MAPPINGS = {
    "AutoDLDownload": AutoDLDownload,
    "FolderViewe": FolderViewe,
    "FolderDeleter": FolderDeleter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AutoDLDownload": "AutoDL下载工具",
    "FolderViewe": "查看文件",
    "FolderDeleter": "删除文件"
}
