# 简述

写这小程序的初衷是为了方便当时写线代作业...(果然偷懒是第一生产力....)

然后也没有太多复杂的功能, 不能对变量进行运算, 只能对常数矩阵做运算... 搞得我现在算那个$\Large \lambda$矩阵的时候又只能手算..现在打算在给这东西做一个更新, 使之能够支持对变量做运算...

# 功能和相应命令

目前实现的功能和相应命令如下:

 ```python
-add r1 r2 -1   第二行*-1后加至第一行
-swi r1 r2      第一行第二行互换
-mul r2 1/3     第二行乘以1/3
-hst            矩阵行拓展
-vst            矩阵列拓展
-bac            撤销上一步
-det            计算矩阵对应行列式的值
-eig            计算特征值和特征向量,一列为一个特征向量
-tra -y         将原矩阵转置, 并保存
-tra -n         显示原矩阵的转置矩阵, 不保存
-ran            计算矩阵的秩
-rev            计算矩阵的逆矩阵
-tmm            化成最简矩阵, 并保存
-ini            重新初始化矩阵
-exi            退出
 ```

# 注意点

-   `-eig`得到的特征向量是列向量的格式, 同一列才是一个特征向量, 同一行不是同一个特征向量.
-   暂不支持变量参与运算

# functions and its commands

```python
-add r1 r2 -1   -1*(r2) + r1 -> r1
-swi r1 r2      switch r1 and r2
-mul r2 1/3     1/3 * r2
-hst            extend new row to the matrix 
-vst            extend new col to the matrix
-bac            undo the latest operation
-det            calculate the determinant of the nxn matrix
-eig            eigen-decomposition
-tra -y         calculate transaction and save
-tra -n         show transaction(no save)
-ran            rank
-rev            reverse
-tmm            change to simplest form matrix
-ini            re-initial matrix
-exi            exit
```

# notices

-   `-eig`returns the $\Large \lambda$ and its vectors, but vectors are ordered by cols, not by rows.
-   so far, only matrix of constant value is supported, initialization with variables will raise exception.