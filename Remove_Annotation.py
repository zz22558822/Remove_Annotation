import regex as re
import os
import sys

# 獲取執行文件所在的文件夾路徑
executable_dir = os.path.dirname(sys.executable)

# 正則表達式
default_comment_pattern = re.compile(r'\/\*[\s\S]*?\*\/|(?<!http:|https:)\/\/[^\n]*(?![\s\S]*http:|[\s\S]*https:)|<!--[\s\S]*?-->|(?<!http:|https:)\/\/[^\n]*')
# 正則表達式 (含Python)
python_comment_pattern = re.compile(r'\/\*[\s\S]*?\*\/|(?<!http:|https:)\/\/[^\n]*(?![\s\S]*http:|[\s\S]*https:)|<!--[\s\S]*?-->|(?<!http:|https:)\/\/[^\n]*|\#.*')

# 移除註解
def remove_comments(content, pattern):
    return re.sub(pattern, '', content)

# 移除空行和僅有空白的行
def remove_blank_lines(content):
    # 使用正則表達式匹配完全空白或僅有空白的行
    return re.sub(r'^\s*\n', '', content, flags=re.MULTILINE)

def process_file(file_path):
    try:
        # 判斷檔案副檔名以選擇正確的正則表達式
        file_extension = os.path.splitext(file_path)[1]
        if file_extension == '.py':
            comment_pattern = python_comment_pattern
        else:
            comment_pattern = default_comment_pattern

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 移除註解
        content = remove_comments(content, comment_pattern)
        
        # 移除空行和僅有空白的行
        cleaned_content = remove_blank_lines(content)

        # 檔案名稱加上 "_min"
        new_file_path = os.path.splitext(file_path)[0] + '_min' + os.path.splitext(file_path)[1]
        
        # 將處理後的內容寫回新檔案
        with open(new_file_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)

        print(f"處理完成，已儲存為: {os.path.basename(new_file_path)}")
        
    except FileNotFoundError:
        print(f"錯誤：找不到 {file_path}。")
    except IOError:
        print(f"錯誤：處理檔案 {file_path} 時發生 I/O 錯誤。")
    except Exception as e:
        print(f"發生錯誤：{e}")

def main():
    try:
        if len(sys.argv) > 1:
            # 取得拖曳進來的檔案路徑
            file_paths = sys.argv[1:]
        else:
            # 提示使用者手動輸入檔案路徑
            file_paths = input("請輸入檔案路徑: ").split()

        for file_path in file_paths:
            process_file(file_path)
        
    except Exception as e:
        # 處理所有未處理的異常
        print(f"程式出現錯誤：{e}")

if __name__ == "__main__":
    main()
    print()
    os.system('pause')
    sys.exit()
