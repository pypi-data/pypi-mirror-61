#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 23:33:33 2019

@author: jkl
"""

def sum(num1, num2):
    return num1 + num2


def sum_only_positive(num1, num2):
    if num1 > 0 and num2 > 0:
        return num1 + num2
    else:
        return None