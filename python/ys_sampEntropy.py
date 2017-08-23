# -*- coding: utf-8 -*-
'''
求样本熵 author by YangSong 2010.11.16 C230
Python Implementation by Matthew McAteer
'''

import math
import numpy as np

def ys_sampEntropy(xdata):
    m = 2
    n = len(xdata)
    r = 0.2 * np.std(xdata) # r = 0.05 匹配模板数的阈值
    cr = []
    gn = 1
    gnmax = m
    
    while gn <= gnmax:
        d = np.zeros(((n-m+1), (n-m))) # 存放距离结果的矩阵
        x2m = np.zeros((n-m+1, m)) # 存放变换后的向量 
        cr1 = np.zeros((1, n-m+1)) # 存放结果的矩阵
        k = 1
        
        for i in range(1, (n-m+1)):
            for j in range(1, m):
                x2m[i,j] = xdata[i+j-1]
        
        x2m
        
        for i in range(1, n-m+1):
            for j in range(1, n-m+1):
                if i != j:
                    d[i, k] = np.max(abs(x2m[i,:] - x2m[j,:])) # 计算各个元素和相应元素的距离
                    k += 1
            
            k = 1
        
        d
        
        for i in range(1, n-m+1):
            [k, l] = size(np.where(d[i,:] < r))   #将比R小的个数传送给L
            cr1[1, i] = l
        
        cr1
        
        cr1 = (1/(n - m)) * cr1
        sum1 = 0
        
        for i in range(1, n-m+1):
            if cr1[i] != 0:
                # sum1 = sum1 + log(cr1[i])
                sum1 += cr1[i]
            
        cr1 = 1/(n-m+1) * sum1
        cr[1, gn] = cr1
        gn += 1
        m += 1
    
    cr
    
    sampEntropy = math.log(cr[1, 1]) - math.log(cr[1, 2])
    return sampEntropy