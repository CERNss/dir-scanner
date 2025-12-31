# File Stats Scanner (文件统计工具)

这是一个基于 Python 的轻量级工具，用于扫描当前目录下的所有文件和文件夹，获取其名称、类型、大小（递归计算文件夹大小）及最后修改时间，并自动生成一份 Excel 统计报表。

## 功能特性

* **自动遍历**：扫描当前路径下的所有文件及文件夹。
* **智能统计**：
* 自动递归计算文件夹内的总大小。
* 将文件大小转换为易读格式（KB, MB, GB）。


* **自我过滤**：自动识别并忽略脚本本身（.py 或 .exe）以及生成的 Excel 文件，防止死循环。
* **格式输出**：生成标准的 `.xlsx` 文件，便于后续排序和筛选。

## 环境准备

* Python 3.8+
* Pip 包管理工具

## 安装与依赖

1. **克隆或下载项目代码**
2. **安装依赖库**
建议使用 `pip` 安装 `requirements.txt` 中的依赖：
```bash
pip install -r requirements.txt

```


*如果没有 requirements.txt，可以直接安装核心库：*
```bash
pip install pandas openpyxl pyinstaller

```



## 使用方法

### 方式一：直接运行 Python 脚本

适用于开发环境或已安装 Python 的机器。

1. 将 `scan_files.py` 放入你想要统计的目录。
2. 在终端运行：
```bash
python scan_files.py

```


3. 运行结束后，当前目录下会生成 **`文件统计清单.xlsx`**。

---

### 方式二：打包为 EXE (推荐)

适用于需要在没有 Python 环境的 Windows 电脑上运行。

#### 1. 执行打包命令

在项目根目录下运行以下命令，将脚本打包为单个可执行文件：

```bash
pyinstaller --onefile scan_files.py

```

* `--onefile`: 将所有依赖合并为一个单独的 `.exe` 文件。

#### 2. 获取 EXE 文件

打包完成后，可以在 `dist/` 文件夹中找到 `scan_files.exe`。

#### 3. 部署使用

1. 将 `dist/scan_files.exe` 复制到任何你想要统计的文件夹中。
2. 双击运行即可。
3. 程序会自动生成统计表格，并忽略 exe 自身。

## 📂 项目结构

```text
.
├── scan_files.py        # 主程序代码
├── requirements.txt     # 项目依赖列表
├── README.md            # 说明文档
├── .gitignore           # Git 忽略配置
├── build/               # (自动生成) 打包临时文件，可忽略
├── dist/                # (自动生成) 最终 EXE 存放位置
│   └── scan_files.exe
└── scan_files.spec      # (自动生成) PyInstaller 配置文件

```

## 📝 注意事项

1. **权限问题**：如果在系统盘（如 C:\Windows）下运行，可能会因为权限不足导致无法写入 Excel，建议以管理员身份运行。
2. **文件占用**：如果 `文件统计清单.xlsx` 已经被打开，再次运行脚本会报错，请先关闭 Excel 文件。

---