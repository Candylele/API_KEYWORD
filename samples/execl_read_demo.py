
import xlrd3

work_books = xlrd3.open_workbook( 'test_data.xlsx' )
# sheet = work_books.sheet_by_name('Sheet1')
sheet = work_books.sheet_by_index(0)
print( sheet.cell_value(0,2) )
print( sheet.cell_value(1,0) )
print( sheet.cell_value(7,0) )
# 需求：合并单元格后，里面每个单元格都能取出对应的值

print( sheet.merged_cells ) # 起始行下标,（结束行-1）,起始列下标,结束列

# 判断一个下标是否是合并单元格合并过的  (4,0) 是否是合并过的
x = 4 ;  y = 0
if x>=1 and x<5:
    if y>=0 and y<1:
        print( '单元格是在一个大的合并单元内' )
    else:
        print('单元格不在一个大的合并单元内')
else:
    print('单元格不在一个大的合并单元内')
print('****************************')

# 优化上述判断合并单元格情况
# for (min_row_index,max_row_index,min_col_index,max_col_index) in [(1,5,0,1),(5, 9, 0, 1)]:
#     print( min_row_index,max_row_index,min_col_index,max_col_index )

x = 7 ;  y = 0
for (min_row_index,max_row_index,min_col_index,max_col_index) in sheet.merged_cells:
    print( min_row_index,max_row_index,min_col_index,max_col_index )
    if x>=min_row_index and x<max_row_index:
        if y>=min_col_index and y<max_col_index:
            print('单元格是在一个大的合并单元内')
            break
        else:
            print('单元格不在一个大的合并单元内')
    else:
        print('单元格不在一个大的合并单元内')

# 合并单元格中 任何一个被合并的单元格 值都等于 合并单元格 左上角第一个单元格的值

x = 3 ;  y = 3
for (min_row_index,max_row_index,min_col_index,max_col_index) in sheet.merged_cells:
    print( min_row_index,max_row_index,min_col_index,max_col_index )
    if x>=min_row_index and x<max_row_index:
        if y>=min_col_index and y<max_col_index:
            cell_value = sheet.cell_value( min_row_index,min_col_index )
            break
        else:
            cell_value = sheet.cell_value( x , y )
    else:
        cell_value = sheet.cell_value( x , y )
print( cell_value )

def get_merged_cell_value(row_index,col_index):
    for (min_row_index, max_row_index, min_col_index, max_col_index) in sheet.merged_cells:
        if row_index >= min_row_index and row_index < max_row_index:
            if col_index >= min_col_index and col_index < max_col_index:
                cell_value = sheet.cell_value(min_row_index, min_col_index)
                break
            else:
                cell_value = sheet.cell_value(row_index, col_index)
        else:
            cell_value = sheet.cell_value(row_index, col_index)
    return cell_value

for i in range(0,9):
    for j in range(0,4):
        cell_value = get_merged_cell_value( i,j )
        print( cell_value ,end=' ' )
    print()