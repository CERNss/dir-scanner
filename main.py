import os
import sys
import pandas as pd
from datetime import datetime

# --- 配置项 ---
OUTPUT_FILENAME = "list.xlsx"


def get_size_recursive(path):
    """
    递归计算文件夹大小
    """
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # 跳过不可访问的链接
                if not os.path.islink(fp):
                    total_size += os.path.getsize(fp)
    except Exception as e:
        print(f"读取大小出错: {path} - {e}")
    return total_size


def format_size(size_bytes):
    """
    将字节大小转换为易读格式 (KB, MB, GB)
    """
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(0)
    p = 1024
    import math
    if size_bytes > 0:
        i = int(math.floor(math.log(size_bytes, p)))
    s = round(size_bytes / math.pow(p, i), 2)
    return f"{s} {size_name[i]}"


def main():
    # 获取脚本所在的当前路径
    current_path = os.getcwd()

    # --- 修改开始 ---
    # 智能判断当前是 "脚本运行" 还是 "Exe运行"
    if getattr(sys, 'frozen', False):
        # 如果是打包后的 exe，sys.executable 就是那个 exe 的完整路径
        this_script_name = os.path.basename(sys.executable)
    else:
        # 如果是 py 脚本运行，__file__ 是脚本名字
        this_script_name = os.path.basename(__file__)
    # --- 修改结束 ---

    file_data = []
    print(f"正在扫描路径: {current_path} ...")
    print(f"当前运行程序（将被忽略）: {this_script_name}")  # 打印一下确认

    # 遍历当前目录下的所有项目
    try:
        items = os.listdir(current_path)
    except PermissionError:
        print("错误：没有权限读取当前目录。")
        return

    for item in items:
        # 这里的判断逻辑也不变，只是变量名统一了
        if item == this_script_name or item == OUTPUT_FILENAME:
            continue

        # 跳过临时文件（以 ~$ 开头的通常是打开的 Office 临时文件）
        if item.startswith("~$"):
            continue

        full_path = os.path.join(current_path, item)

        # 1. 名称
        name = item

        # 2. 类型 & 3. 大小
        if os.path.isdir(full_path):
            ftype = "文件夹"
            # 计算文件夹总大小（如果不想要递归计算，可以直接设为 0）
            raw_size = get_size_recursive(full_path)
        else:
            # 获取文件后缀
            _, ext = os.path.splitext(item)
            ftype = ext if ext else "文件"
            raw_size = os.path.getsize(full_path)

        readable_size = format_size(raw_size)

        # 4. 最后更新时间
        mtime = os.path.getmtime(full_path)
        last_modified = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')

        # 添加到数据列表
        file_data.append({
            "名称": name,
            "类型": ftype,
            "大小 (易读)": readable_size,
            "最后更新时间": last_modified
        })

    # 生成 DataFrame
    if file_data:
        df = pd.DataFrame(file_data)

        # 重新排序一下列的顺序
        df = df[["名称", "类型", "大小 (易读)", "最后更新时间"]]

        # 导出到 Excel
        try:
            output_path = os.path.join(current_path, OUTPUT_FILENAME)
            df.to_excel(output_path, index=False)
            print("-" * 30)
            print(f"成功！统计完成。")
            print(f"文件已保存为: {OUTPUT_FILENAME}")
            print(f"共统计了 {len(file_data)} 个项目。")
        except PermissionError:
            print(f"错误：无法写入 {OUTPUT_FILENAME}。请检查文件是否已被打开。")
    else:
        print("当前目录下没有其他文件或文件夹。")


if __name__ == "__main__":
    main()