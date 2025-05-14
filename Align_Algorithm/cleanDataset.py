import sys

def replace_tabs_with_spaces(file_path):
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 将所有的制表符替换为空格
        content = content.replace('\t', ' ')
        
        # 将修改后的内容写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"成功将 {file_path} 中的制表符替换为空格。")
    except Exception as e:
        print(f"处理文件时出错: {e}")

if __name__ == "__main__":
    replace_tabs_with_spaces('D:\GraphAlignment-Visualization\Align_Algorithm\GTCAlign\data\ppi\ppi_s_edge.txt')
    replace_tabs_with_spaces('D:\GraphAlignment-Visualization\Align_Algorithm\GTCAlign\data\ppi\ppi_t_edge.txt')