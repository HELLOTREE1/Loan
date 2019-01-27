# -*- coding: utf-8 -*-

from scipy.optimize import minimize
import numpy as np
import pandas as pd

def sumAndMul2List(list1, list2):
    result = sum([a * b for a, b in zip(list1, list2)])
    return result

def toWX(vec):
    return list(vec[:6]), list(vec[6:])

def fun(x):
    list2, list4 = toWX(x)
    Z = sumAndMul2List(list1, list2) + sumAndMul2List(list3, list4)
    return 1/Z


"""
变量
w15,w25,w35,w45,w55,w65
y0,y1,y2,y3,y4,y5

x15,x25,x35,x45,x55,x65,x75
y6,y7,y8,y9,y10,y11,y12

list1:r
list2:w
list3:R
list4:x
"""


def con1(x):
    """
    VaR约束
    """
    list2, list4 = toWX(x)
    return (1e10 * (list4[0] * list4[3])) ** 2 / (1.65 ** 2) - ((227376 * list2[2] ** 2) ** 2)


def con2(x):
    """
    代存款比重约束
    """
    return 0.75 - np.sum(toWX(x)[1])

def con3(x):
    """
    备付金比重约束
    """
    list2, list4 = toWX(x)
    return list2[0] + list2[3] - 0.05 * np.sum(list4)

def con4(x):
    list2, list4 = toWX(x)
    return 0.08 * (1 - list2[1] - list2[2] - list2[3]) - list2[4] - list2[5]

def con5(x):
    """
    比重和为1
    """
    list2, list4 = toWX(x)
    return np.sum(list2) + np.sum(list4) - 1

def con():
    # 约束条件 分为eq 和ineq
    # eq表示 函数结果等于0 ； ineq 表示 表达式大于等于0
    cons = ({'type': 'eq', 'fun': lambda x: con5(toWX(x))},
            {'type': 'ineq', 'fun': con2},
            {'type': 'ineq', 'fun': con3},
            {'type': 'ineq', 'fun': con4})
    return cons

if __name__ == "__main__":
    r_i_path = '/home/szu/PycharmProjects/Navajoa/data/IR.csv'
    r_i = list(pd.read_csv(r_i_path)['r_i'])

    R_k5_path = '/home/szu/PycharmProjects/Navajoa/data/R_k5.csv'
    R_k5 = list(pd.read_csv(R_k5_path)['R_k5'])

    list1 = r_i
    list3 = R_k5

    # 设置参数范围/约束条件
    b = [0.0, 1.0]
    x35 = [0.0, 0.15]
    w15 = [0.0006, 0.015]
    w25 = [0.06,0.06]
    w35 = [0.07,0.07]
    bnds = (w15, w25, w35, b, b, b, b, b, x35, b, b, b, b)

    # 设置初始猜测值
    n = 13
    x0 = np.zeros(n)
    x0[0] = 0.0
    x0[1] = 0.06
    x0[2] = 0.07
    x0[3] = 0.0
    x0[4] = 0.0
    x0[5] = 0.0
    x0[6] = 0.0
    x0[7] = 0.0
    x0[8] = 0.0
    x0[9] = 0.0
    x0[10] = 0.0
    x0[11] = 0.0
    x0[12] = 0.0

    cons = con()
    res = minimize(fun, x0, method='CG', bounds=bnds, constraints=cons)
    print(res.fun)
    print(res.success)
    print(res.x)
