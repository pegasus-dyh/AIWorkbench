
import os
import matplotlib.pyplot as plt
import pandas as pd
import io

# 设置matplotlib支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

def read_dat_files(directory):
    """
    读取指定目录下的所有 .dat 文件，返回以 DataFrame 为值的字典。

    参数:
        directory (str): 目标文件夹路径

    返回:
        data_dict (dict): 键为文件名（不带路径），值为 pandas.DataFrame
    """
    data_dict = {}

    for filename in os.listdir(directory):
        if filename.endswith('.dat'):
            filepath = os.path.join(directory, filename)
            try:
                # 读取文件内容
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()

                # 转换为DataFrame并设置列名
                df = pd.read_csv(io.StringIO(content), sep='\s+', header=None)
                df.columns = [f'var{i+1}' for i in range(df.shape[1])]
                data_dict[filename] = df

            except Exception as e:
                print(f"无法读取文件 {filename}，错误：{e}")

    return data_dict

def preview_data(data_dict, filename, rows=5):
    """
    预览指定文件的数据内容。

    参数:
        data_dict (dict): 数据字典
        filename (str): 文件名
        rows (int): 显示的行数，默认为5
    """
    if filename not in data_dict:
        print(f"错误：找不到文件 {filename}")
        return

    df = data_dict[filename]
    print(f"\n文件名: {filename}")
    print(f"数据形状: {df.shape}")
    print(f"列名: {list(df.columns)}")
    print("\n数据预览:")
    print(df.head(rows))

def plot_data(data_dict, filename, variables=None, figsize=(12, 6)):
    """
    可视化指定文件的数据。

    参数:
        data_dict (dict): 数据字典
        filename (str): 文件名
        variables (list): 要绘制的变量列表，默认为None（绘制所有变量）
        figsize (tuple): 图表大小
    """
    try:
        # 数据有效性检查
        if not isinstance(data_dict, dict):
            raise ValueError("data_dict必须是字典类型")
        if not isinstance(filename, str):
            raise ValueError("filename必须是字符串类型")
        if filename not in data_dict:
            raise KeyError(f"错误：找不到文件 {filename}")

        df = data_dict[filename]
        if not isinstance(df, pd.DataFrame):
            raise ValueError(f"文件 {filename} 的数据不是DataFrame类型")
        if df.empty:
            raise ValueError(f"文件 {filename} 的数据为空")

        # 数据预处理
        df_clean = df.copy()
        # 处理缺失值
        df_clean = df_clean.fillna(method='ffill').fillna(method='bfill')
        # 处理异常值（使用3倍标准差法）
        for col in df_clean.columns:
            mean = df_clean[col].mean()
            std = df_clean[col].std()
            df_clean[col] = df_clean[col].clip(mean - 3*std, mean + 3*std)

        # 确定要绘制的变量
        if variables is None:
            variables = df_clean.columns
        elif not isinstance(variables, (list, tuple)):
            variables = [variables]

        # 创建图表
        plt.figure(figsize=figsize)
        valid_vars = []
        for var in variables:
            if var in df_clean.columns:
                plt.plot(df_clean[var], label=var, linewidth=1.5)
                valid_vars.append(var)
            else:
                print(f"警告：变量 {var} 不存在于数据中")

        if not valid_vars:
            raise ValueError("没有有效的变量可以绘制")

        # 优化图表显示
        plt.title(f"数据可视化 - {filename}", fontsize=12, pad=15)
        plt.xlabel("样本点", fontsize=10)
        plt.ylabel("数值", fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
        plt.tight_layout()

        # 自动调整坐标轴范围
        plt.margins(x=0.01)

        plt.show()

    except Exception as e:
        print(f"绘图过程中出现错误：{str(e)}")
        plt.close()  # 确保错误发生时关闭图形

# 示例使用
if __name__ == "__main__":
    # 读取数据
    data = read_dat_files("D:\数据集文件初步\田纳西数据集\ieee\Tennessee\TE DATASETS\TE数据\训练集")

    print(data.keys())
    first_file = next(iter(data.keys()))# 获取第一个文件名
    print(first_file)
    first_file = 'd11.dat'
    
    # 预览数据
    preview_data(data, first_file)
    
    # 可视化数据
    plot_data(data, first_file, variables=['var2'])