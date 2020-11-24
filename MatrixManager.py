# encoding: utf-8

"""
@author: Hengyu Jiang
@file: MatrixManager.py
@project: matrixManager
@time: 2020/1/11 20:12

------------------------------requirement------------------------------
- numpy                                                               -
-----------------------------------------------------------------------

"""
import numpy as np
from copy import deepcopy
from fractions import Fraction

FRAC_LEN_LIMIT = 999999    # 小数转换成分数的精确度
MT = None


class MatrixTransformer(object):
    matrix = None     # 矩阵, 用以计算, np.array
    back_matrix = []  # 后退一步,这里相当于一个栈
    shape = None      # 矩阵形状, tuple

    def __init__(self, matrix):
        """
        求转置矩阵
        :param matrix:
        """
        if matrix is not None:
            self.matrix = np.array(matrix, dtype=float)
        else:
            self.matrix = np.array(generateMatrix())
        self.shape = self.matrix.shape

    def backUp(self):
        """
        保存当前矩阵
        """
        self.back_matrix.append(deepcopy(self.matrix))

    def goBack(self):
        try:
            self.matrix = self.back_matrix.pop()
            return True
        except:
            return False

    def calRank(self):
        """
        计算矩阵的秩
        """
        return np.linalg.matrix_rank(self.matrix)

    def calEigen(self):
        """
        计算特征值和特征向量
        :return: bool, list, np.matrix
        """
        # 非方阵没有特征值和特征向量
        if not self.shape[0] == self.shape[1]:
            return False, None, None
        eigenValues, eigenVector = np.linalg.eig(self.matrix)
        return True, eigenValues, eigenVector

    # 计算矩阵的行列式的值
    def calDeterminant(self):
        """
        计算矩阵的行列式的值
        :return:   bool,  fraction
        """
        # 非方阵没有行列式
        if not self.shape[0] == self.shape[1]:
            return False, 0
        return True, Fraction(np.linalg.det(self.matrix)).limit_denominator(FRAC_LEN_LIMIT)

    def calReverseMatrix(self):
        """
        求逆矩阵
        :return: bool, np.matrix
        """
        # 非方阵均不可逆
        if not self.shape[0] == self.shape[1]:
            return False, None
        # 行列式值为0, 不可逆
        elif 0 == self.calDeterminant():
            return False, None
        return True, np.linalg.inv(self.matrix)

    def calTransMatrix(self, backup=True):
        """
        求转置矩阵
        :param backup:   bool      是否保存
        :return      :   np.array
        """
        if backup:
            self.backUp()
            self.__init__(deepcopy(self.matrix.transpose()))
            return self.matrix
        else:
            temp_matrix = deepcopy(self.matrix)
            return temp_matrix.transpose()

    def rowExtend(self, extendMatrix, backup=True):
        """
        行拓展成增广矩阵
        :param extendMatrix: np.array    n*m 的列向量, n为self.matrix的行数
        :param backup:       bool 是否保存
        :return:             bool
        """
        # 行数不相等, 不可拓展
        if not self.shape[0] == extendMatrix.shape[0]:
            return False
        if backup:
            self.backUp()
        temp_matrix = np.hstack((self.matrix, extendMatrix))
        self.__init__(deepcopy(temp_matrix))
        return True

    def colExtend(self, extendMatrix, backup=True):
        """
        列拓展成增广矩阵
        :param backup:       bool 是否保存
        :param extendMatrix: np.array    m*n 的行向量, n为self.matrix的列数
        :return:             bool
        """
        # 列数不相等, 不可拓展
        if not self.shape[1] == extendMatrix.shape[1]:
            return False
        if backup:
            self.backUp()
        temp_matrix = np.vstack((self.matrix, extendMatrix))
        self.__init__(deepcopy(temp_matrix))
        return True

    def rowMulNumber(self, row_index, k, backup=True):
        """
        某一行元素乘上非零实数k
        :param backup:      bool      是否保存
        :param row_index:   int,      行下标
        :param k:           float,    非零实数
        :return:            bool
        """
        if 0 == k:
            return False
        if backup:
            self.backUp()  # 备份
        temp_matrix = [x * k for x in self.matrix[row_index]]
        self.matrix[row_index] = temp_matrix
        return True

    def rowAddtoRow(self, row1, row2, k, backup=True):
        """
        row2的k倍加到row1
        :param backup:  bool 是否保存
        :param row1:    int
        :param row2:    int
        :param k   :    float
        :return    :    bool
        """
        row_num = self.shape[0]
        if row1 > row_num or row2 > row_num:  # 下标越界
            return False
        if backup:
            self.backUp()  # 备份
        col_num = self.shape[1]
        for i in range(col_num):
            self.matrix[row1][i] += self.matrix[row2][i] * k
        return True

    def toMiniMatrix(self, backup=True):
        """
        将矩阵化成eye形式
        :param backup:  bool  是否保存
        :return:        bool
        """
        if self.feature.get('is_rmm'):  # 已经是eye形式
            return True
        if backup:
            self.backUp()
        rows = self.shape[0]
        cols = self.shape[1]
        if rows > cols:  # 若行数多于列数, 转置后再转换成行最简
            self.coltoMiniMatrix()
        else:
            self.rowtoMiniMatrix()

        self.feature['is_rmm'] = True
        return True

    def coltoMiniMatrix(self):
        """
        列数多于行数的矩阵转换成eye
        :return:  bool
        """
        # 转置之后, 行数多余列数, 化成eye之后再转置回来,期间不能保存,否则会破坏back_matrix
        self.calTransMatrix(backup=True)
        self.back_matrix.pop()

        self.rowtoMiniMatrix()

        self.calTransMatrix(backup=True)
        self.back_matrix.pop()
        return True

    def rowtoMiniMatrix(self):
        """
        行数多于列数的矩阵转换成eye
        :return:
        """
        rows, cols = self.shape[0], self.shape[1]
        # 将每行主元化成1
        for i in range(rows):
            if 0 == self.matrix[i][i]:
                continue
            k = 1 / self.matrix[i][i]
            self.rowMulNumber(i, k, backup=False)
            for j in range(i, rows):
                if i == j:
                    pass
                else:
                    kk = -self.matrix[j][i]
                    self.rowAddtoRow(j, i, kk, backup=False)

        # 将主元所在列的其他元素化成0
        for i in range(rows - 2, -1, -1):
            for j in range(rows - 1, i, -1):
                if i == j:
                    pass
                else:
                    k = -self.matrix[i][j]
                    self.rowAddtoRow(i, j, k, backup=False)
        return True

    def switchRow(self, row1, row2, backup=True):
        """
        row1互换row2
        :param backup:  bool 是否保存
        :
        :param row1:  int
        :param row2:  int
        :return    :  bool
        """
        row_num = self.shape[0]
        if row1 > row_num or row2 > row_num:  # 行下标越界检查
            return False
        if backup:
            self.backUp()  # 备份
        temp_row = deepcopy(self.matrix[row1])
        self.matrix[row1] = deepcopy(self.matrix[row2])
        self.matrix[row2] = deepcopy(temp_row)
        return True


def generateMatrix():
    data2D = []
    print('>> 输入矩阵(空格隔开):')
    while True:
        userInput = input('Input:').split(' ')  # 输入数组，数据间用空格隔开即可
        if userInput is None or userInput == [] or userInput == ['']:
            break
        else:
            temp_list = []
            for x in userInput:
                if x is not None and x != '':
                    temp_list.append(analysisNumber(x))
            data2D.append(temp_list)

    print('>> 输入的矩阵为: ')
    display(data2D)
    return np.array(data2D, dtype=float)


def display(disp_matrix):
    """
    显示矩阵
    """
    row = len(disp_matrix)
    col = len(disp_matrix[0])
    for i in range(row):
        for j in range(col):
            # 将小数转换成分数
            print("\t{:^6s}\t".format(str(Fraction(disp_matrix[i][j]).limit_denominator(FRAC_LEN_LIMIT))), end='')
        print()
    return


def analysisNumber(string):
    """
    处理控制台输入的分数, 例如1/3
    :param string: str    输入的分数
    :return :      float
    """
    div_index = string.find('/')
    if -1 == div_index:
        return float(string)
    else:
        num1 = float(string[:div_index])
        num2 = float(string[div_index + 1:])
        return num1 / num2
