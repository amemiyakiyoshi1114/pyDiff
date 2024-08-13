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
                differences.append((i, j, 'green'))  # 增加
            elif value1 != 'nan' and value2 == 'nan':
                differences.append((i, j, 'red'))  # 删除
            elif  value1 != 'nan' and value2 != 'nan' and value1 != value2:
                differences.append((i, j, 'yellow'))  # 修改

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


if __name__ == '__main__':
    print(print_color("D:/words/培训/组内培训记录/测试账号信息.xlsx","D:/words/培训/组内培训记录/测试账号信息 - 副本.xlsx"))
