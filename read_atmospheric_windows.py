#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 11:09:43 2017

@author: csousasilva
"""


def window_loader(filename):
    
    with open(filename) as f:
        data = f.read().split("\n")
        
        windows = []
        for i in data:
            try:
                a,b = i.split("-")
                windows.append((a,b))
            except:
                pass
            
        return windows