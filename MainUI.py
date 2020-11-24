# encoding: utf-8

"""
@author: Hengyu Jiang
@file: MainUI.py
@project: matrixManager
@time: 2020/1/11 20:14
"""

from MatrixManager import generateMatrix, analysisNumber, display


def mainUI(MT):
    while True:
        print("""
        ***************输入样例***************
        *  -add r1 r2 -1   第二行*-1后加至第一行
        *  -swi r1 r2      第一行第二行互换
        *  -mul r2 1/3     第二行乘以1/3
        *  -hst            矩阵行拓展
        *  -vst            矩阵列拓展
        *  -bac            撤销上一步
        *  -det            计算矩阵对应行列式的值
        *  -eig            计算特征值和特征向量,一列为一个特征向量
        *  -tra -y         将原矩阵转置, 并保存
        *  -tra -n         显示原矩阵的转置矩阵, 不保存
        *  -ran            计算矩阵的秩
        *  -rev            计算矩阵的逆矩阵
        *  -tmm            化成最简矩阵, 并保存
        *  -ini            重新初始化矩阵
        *  -exi            退出
        *************************************
        """)
        print()
        print('当前矩阵为:')
        display(MT.matrix)
        print()
        print('>> Input: ', end='')
        string = input()
        operator = None
        if string in ['-exi', '-EXI']:
            print('>> 退出')
            print('--------------------------------------------------------------------------------------------------')
            return
        str_list = string.split()
        try:
            operator = str_list[0]
        except:
            print('>> 操作出错')
        if operator is None:
            continue
        elif operator in ['-ini', '-INI']:
            MT.__init__(matrix=generateMatrix())
        elif operator in ['-add', '-ADD']:
            try:
                row1 = int(str_list[1][1:])
                row2 = int(str_list[2][1:])
                try:
                    num_str = str_list[3]
                except:
                    num_str = '1'

                k = analysisNumber(num_str)
                print('>> 第 {} 行的 {} 倍加至第 {} 行'.format(row2, num_str, row1))
                MT.rowAddtoRow(row1 - 1, row2 - 1, k)
            except:
                print('>> 操作出错')
        elif operator in ['-swi', '-SWI']:
            try:
                row1 = int(str_list[1][1:])
                row2 = int(str_list[2][1:])
                print('>> 交换第 {} 行和第 {} 行'.format(row1, row2))
                MT.switchRow(row1 - 1, row2 - 1)
            except:
                print('>> 操作出错')
        elif operator in ['-mul', '-MUL']:
            try:
                row1 = int(str_list[1][1:])
                num_str = str_list[2]
                k = analysisNumber(num_str)
                print('>> 第 {} 行乘 {}'.format(row1, num_str))
                MT.rowMulNumber(row1 - 1, k)
            except:
                print('>> 操作出错')
        elif operator in ['-hst', '-HST']:
            try:
                extendMatrix = generateMatrix()
                success = MT.rowExtend(extendMatrix)
                if not success:
                    print('>> 拓展失败, 输入矩阵与原矩阵行数不等')
            except:
                print('>> 操作出错')
        elif operator in ['-vst', '-VST']:
            try:
                extendMatrix = generateMatrix()
                success = MT.colExtend(extendMatrix)
                if not success:
                    print('>> 拓展失败, 输入矩阵与原矩阵列数不等')
            except:
                print('>> 操作出错')
        elif operator in ['-det', '-DET']:  # 求矩阵的行列式值
            try:
                success, det = MT.calDeterminant()
                if success:
                    print('>> 行列式值为 {}'.format(det))
                else:
                    print('>> 该矩阵不是方阵, 无法计算行列式')
            except:
                print('>> 操作出错')
        elif operator in ['-ran', '-RAN']:
            try:
                rank = MT.calRank()
                print('>> 矩阵的秩为 {}'.format(rank))
            except:
                print('>> 操作出错')
        elif operator in ['-tra', '-TRA']:
            try:
                if str_list[1] in ['-y', '-Y']:
                    need_save = True
                else:
                    need_save = False
                trans_matrix = MT.calTransMatrix(backup=need_save)
                print('>> 转置矩阵为:')
                display(trans_matrix)
            except:
                print('>> 操作出错')
        elif operator in ['-eig', '-EIG']:
            try:
                success, value, vector = MT.calEigen()
                if success:
                    print('>> 特征值为 {}'.format(value))
                    print('>> 特征向量为 {}'.format(vector))
                else:
                    print('>> 该矩阵不是方阵, 无法计算特征值和特征向量')
            except:
                print('>> 操作出错')
        elif operator in ['-tmm', 'TMM']:
            MT.toMiniMatrix()
        elif operator in ['-rev', '-REV']:
            try:
                success, rev_matrix = MT.calReverseMatrix()
                if success:
                    print('逆矩阵为:')
                    display(rev_matrix)
                else:
                    print('>> 该矩阵不是方阵, 或者不可逆')
            except:
                print('>> 操作出错')
        elif operator in ['-bac', '-BAC']:
            try:
                print('>> 撤销上一步操作')
                MT.goBack()
            except:
                print('>> 操作出错')
        print()
        input('>> 回车继续')
        print('--------------------------------------------------------------------------------------------------')
        print()
if __name__ == '__main__':
    mainUI()
