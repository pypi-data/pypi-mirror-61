#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 22:31:02 2019

@author: jkl
"""

from api.R2 import R2

k = R2()
k.createSurvey('./api/test/syscalFile.csv')

def test_sycalParser():
    if len(k.surveys) == 1:
        assert k.surveys[0].df.shape[0] == 345
    else:
        print('hole !')

k.linfit()
k.pwlfit()

def test_errorColum():
    assert 'resError' in k.surveys[0].df.columns
