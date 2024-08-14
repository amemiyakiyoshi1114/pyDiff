from collections import defaultdict

import pandas
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget


# 告诉qtable如何加载表格，需要表格有多少个sheet，每个sheet对应一个tab
# 告诉qtable如何上色，（Sheet,x,y,color)


def find_diif(df1, df2):
    # 获取行列数
    rows1, cols1 = df1.shape
    rows2, cols2 = df2.shape

    differences = []
    # 比较单元格
    for i in range(max(rows1, rows2)):
        for j in range(max(cols1, cols2)):
            value1 = df1.iat[i, j] if i < rows1 and j < cols1 else "nan"
            value2 = df2.iat[i, j] if i < rows2 and j < cols2 else "nan"
            #详细比较逻辑
            if value1 == 'nan' and value2  == 'nan':continue
            if value1 == 'nan' and value2 != 'nan':
                differences.append((i, j, 'add'))  # 增加
            elif value1 != 'nan' and value2 == 'nan':
                differences.append((i, j, 'delete'))  # 删除
            elif  value1 != 'nan' and value2 != 'nan' and value1 != value2:
                differences.append((i, j, 'modify'))  # 修改

    return differences


def print_color(old_directory, new_directory):
    old_table = pandas.ExcelFile(old_directory)
    old_sheets = old_table.sheet_names
    new_table = pandas.ExcelFile(new_directory)
    new_sheets = new_table.sheet_names


    count = len(old_sheets) if len(old_sheets) < len(new_sheets) else len(new_sheets)
    i = 0
    all_differences = {}
    while i < count:
        df_old = old_table.parse(old_sheets[i])
        df_old = df_old.astype(str)
        df_new = new_table.parse(new_sheets[i])
        df_new = df_new.astype(str)
        differences = find_diif(df_old, df_new)
        if differences:  # 只在有差异时添加
            all_differences[i] = differences  # 使用 i 作为键
        i += 1

    return all_differences

def load_table(table_directory, table):
    excel_file = pandas.ExcelFile(table_directory)
    sheet_names = excel_file.sheet_names
    for sheet in sheet_names:
        add_sheet_to_tab(sheet, excel_file.parse(sheet), table)


def add_sheet_to_tab(sheet_name, df, table):
    table_widget = QTableWidget()
    table_widget.setRowCount(df.shape[0])
    table_widget.setColumnCount(df.shape[1])
    # table_widget.setHorizontalHeaderLabels(df.columns)
    table_widget.setHorizontalHeaderLabels([str(col) for col in df.columns])

    for row in range(df.shape[0]):
        for col in range(df.shape[1]):
            item = QTableWidgetItem(str(df.iat[row, col]))
            table_widget.setItem(row, col, item)

    table.addTab(table_widget, sheet_name)

def create_dataframe(data):
    sheets = []  # 用于存储不同的 DataFrame

    for index, entries in data.items():
        columns = defaultdict(list)
        valid_columns = ['add', 'delete', 'modify']

        for entry in entries:
            row, col, action = entry
            if action in valid_columns:
                columns[action].append((row, col))

        # 确保所有列的长度一致
        max_length = max(len(v) for v in columns.values())
        for key in columns.keys():
            while len(columns[key]) < max_length:
                columns[key].append((None, None))  # 填充 None 以保持长度一致

        # 创建 DataFrame
        df = pandas.DataFrame.from_dict(columns, orient='index').transpose()
        df.sheet_key = index
        sheets.append(df)  # 将 DataFrame 添加到列表中
        #print(df.sheet_key)

    return sheets


if __name__ == '__main__':
    data = print_color("D:/words/培训/组内培训记录/测试账号信息.xlsx","D:/words/培训/组内培训记录/测试账号信息 - 副本.xlsx")
    table = create_dataframe(data)
    for i, sheet in enumerate(table):
        print(f"Sheet {i}:\n{sheet}\n")