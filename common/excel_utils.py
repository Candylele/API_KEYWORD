# 读写excel操作封装

import xlrd3 #xlrd主要用于读取.xls文件。如果处理.xlsx文件，使用openpyxl或pandas

class ExcelUtils:
    def __init__(self,excel_file_path,sheet_name): #__init__方法是一个特殊的方法，被称为类的构造函数或初始化方法。当创建这个类的实例时，此方法会自动被调用
        self.excel_file_path = excel_file_path
        self.sheet_name = sheet_name  #将外部传入的参数保存到类的实例中，在类的其他方法中能够使用这些参数
        self.sheet = self.get_sheet()

    def get_sheet(self):  # 根据文件路径和sheet名称打开数据
        work_book = xlrd3.open_workbook(self.excel_file_path)
        sheet = work_book.sheet_by_name(self.sheet_name)
        return sheet

    def get_row_count(self):  # 获取表格的总行数
        row_count = self.sheet.nrows
        return row_count

    def get_column_count(self):  # 获取表格的总列数
        column_count = self.sheet.ncols
        return column_count

    """
        def get_merged_cell_value(self, row_index, col_index):
            # 遍历电子表格中所有的合并单元格范围
            for (min_row_index, max_row_index, min_col_index, max_col_index) in self.sheet.merged_cells:
                # 检查目标单元格是否在当前遍历到的合并单元格范围内（行）
                if row_index >= min_row_index and row_index < max_row_index:
                    # 进一步检查目标单元格是否在当前遍历到的合并单元格范围内（列）
                    if col_index >= min_col_index and col_index < max_col_index:
                        # 如果目标单元格确实在合并单元格范围内，则获取合并单元格左上角的值
                        cell_value = self.sheet.cell_value(min_row_index, min_col_index)
                        # 找到值后，立即退出循环
                        break
                    else:
                        # 如果目标单元格不在合并单元格的列范围内，但可能在行范围内（实际上这个else分支在逻辑上是多余的）
                        # 因为如果不在列范围内，上面的if条件已经判断过不在整个合并范围内了，这里又单独对列进行判断并赋值
                        # 这个赋值操作会被下面的else分支覆盖，除非在上面的if条件中break跳出循环
                        cell_value = self.sheet.cell_value(row_index, col_index)
                else:
                    # 如果目标单元格不在当前遍历到的合并单元格的行范围内
                    # 则直接获取目标单元格的值（这个else分支也是多余的，因为上面的if已经涵盖了所有情况）
                    cell_value = self.sheet.cell_value(row_index, col_index)
            # 返回获取到的单元格值
            return cell_value  #标黄可能是因为会抛出异常但没有try-except处理
    """

    # merged_cells是一个属性，它包含了工作表中所有合并单元格的信息
    # 每个合并单元格区域由一个四元组(min_row, max_row, min_col, max_col)表示
    # 检查指定的行索引row_index和列索引col_index是否位于某个合并单元格区域内
    # 指定的单元格位于某个合并单元格区域内，则返回该合并区域左上角单元格的值（即合并前的原始数据）
    def get_merged_cell_value(self, row_index, col_index):
        for (min_row, max_row, min_col, max_col) in self.sheet.merged_cells: #判断是否有合并单元格
            if min_row <= row_index < max_row and min_col <= col_index < max_col:
                return self.sheet.cell_value(min_row, min_col)
        # 如果没有找到合并单元格，或者目标单元格不在任何合并单元格范围内，则直接获取目标单元格的值
        return self.sheet.cell_value(row_index, col_index)

    ''' 把excel转换成如下格式：
                [{'列1名称':列1的值,'列2名称':列2的值,'列3名称':列3的值..},
                {'列1名称':列1的值,'列2名称':列2的值,'列3名称':列3的值..},
                .....]
    '''
    def get_excel_data_by_list(self):
        excel_data = []
        first_row_data = self.sheet.row_values(0)
        for row_index in range(1, self.get_row_count()):
            row_dict = {}
            for col_index in range(self.get_column_count()):
                row_dict[first_row_data[col_index]] = self.get_merged_cell_value(row_index, col_index)
            excel_data.append(row_dict)
        return excel_data

if __name__=='__main__':
    import os
    # excel_path = os.path.join( os.path.dirname(os.path.abspath(__file__)),'..','samples','test_data.xlsx' )
    # excel_utils = ExcelUtils(excel_path,'Sheet1')
    # print(excel_utils.get_row_count())
    # print(excel_utils.get_column_count())
    # print(excel_utils.get_merged_cell_value(3, 0))
    # print(excel_utils.get_merged_cell_value(1, 2))
    # print(excel_utils.get_excel_data_by_list())

    # 构建出一个指向当前脚本所在目录的上一级目录中的test_data子目录下的testcase_infos.xlsx文件的完整路径
    # os.path.abspath(__file__)的作用是获取当前脚本的绝对路径
    # os.path.join(...)：这个函数用于将多个路径组件合并成一个完整的路径
    # os.path.dirname函数的作用是获取一个路径中的目录部分，去掉文件名

    excel_path = os.path.join( os.path.dirname(os.path.abspath(__file__)),'..','test_data','testcase_infos.xlsx' )
    excel_utils = ExcelUtils(excel_path,'Sheet1')

    for case_step in excel_utils.get_excel_data_by_list():
        print( case_step )

    list = excel_utils.get_excel_data_by_list()
    print(list)

