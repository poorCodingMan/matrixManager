# encoding: utf-8

"""
@author: Hengyu Jiang
@file: app.py
@time: 2019/7/7 20:05
"""

from MatrixManager import MatrixTransformer, MT
from MainUI import mainUI




if __name__ == '__main__':
    matrix =  [[1, -2, 1],
               [-2, 1, 1],
               [1, 1, -2]]
    MT = MatrixTransformer(matrix=None)

    mainUI(MT)
