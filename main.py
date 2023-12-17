import os
import hashlib
from tqdm import tqdm

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

            # 根据用户选择生成绝对路径或相对路径
            if use_absolute_path:
                result.append(f'{file_path} [MD5: {md5}]')
            else:
                result.append(f'{os.path.relpath(file_path, directory)} [MD5: {md5}]')
    return result

def save_to_txt(file_list, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in file_list:
            f.write("%s\n" % item)


def main():
    # 获取用户输入的文件夹目录
    directory = input("请输入文件夹目录：")

    # 询问用户是否生成绝对路径
    use_absolute_path = input("生成绝对路径(A)还是相对路径(R)？ (A/R): ").upper() == "A"

    # 生成文件列表及MD5值
    file_list_with_md5 = generate_file_list_with_md5(directory, use_absolute_path)

    # 保存到文本文件
    output_file = "output.txt"
    save_to_txt(file_list_with_md5, output_file)

    print(f"文件列表及MD5值已保存到 {output_file}")

if __name__ == "__main__":
    main()
