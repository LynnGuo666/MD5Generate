import os
import hashlib
from tqdm import tqdm
import json  # Import the json module

import getopt
import sys

def calculate_md5(file_path, block_size=8192):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()

def generate_file_list_with_md5(directory, use_absolute_path):
    result = []
    total_files = sum([len(files) for _, _, files in os.walk(directory)])

    for root, dirs, files in tqdm(os.walk(directory), total=total_files, desc='Generating MD5'):
        for file in files:
            file_path = os.path.join(root, file)
            md5 = calculate_md5(file_path)
            size = os.path.getsize(file_path)

            # 根据用户选择生成绝对路径或相对路径
            if use_absolute_path:
                result.append({"file": file_path, "md5": md5, "size": size})
            else:
                result.append({"file": os.path.relpath(file_path, directory), "md5": md5, "size": size})
    return result

def save_to_txt(file_list, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in file_list:
            f.write("%s\n" % item)

def save_to_json(file_list, output_file):
    json_data = {"files": file_list}
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2)

def main():

    command_mode = False
    directory = ''
    use_absolute_path = False
    output_format = "JSON"

    # 命令行参数获取
    opts,args = getopt.getopt(sys.argv[1:],'cd:at',['command','directory=','absolute','txt'] )
    for opt_name,opt_value in opts:
        if opt_name in ('-c','--command'):
            command_mode=True
        if opt_name in ('-d','--directory'):
            directory = opt_value
        if opt_name in ('-a','--absolute'):
            use_absolute_path=True  
        if opt_name in ('-t','--txt'):
            output_format = "TXT"

    if command_mode != True:
        # 获取用户输入的文件夹目录
        directory = input("请输入文件夹目录：")

        # 询问用户是否生成绝对路径
        use_absolute_path = input("生成绝对路径(A)还是相对路径(R)？ (A/R): ").upper() == "A"

        # 询问用户选择生成JSON还是TXT
        output_format = input("生成文件格式 (JSON/TXT): ").upper()
        

    # 生成文件列表及MD5值
    file_list_with_md5 = generate_file_list_with_md5(directory, use_absolute_path)

    # 保存到相应格式的文件
    output_file = "output." + output_format.lower()
    if output_format == "JSON":
        save_to_json(file_list_with_md5, output_file)
    elif output_format == "TXT":
        save_to_txt(file_list_with_md5, output_file)

    print(f"文件列表及MD5值已保存到 {output_file}")

if __name__ == "__main__":
    main()
