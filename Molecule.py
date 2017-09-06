#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 20:46:21 2017

@author: csousasilva
"""
import math
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
import cPickle as pickle
import re

boltzmann = 1.38064852 * (10**(-23))
light_speed = 2.998 * 10**8
plank = 6.626070040 * (10**(-34))
cm1_joules = 5.03445 * 10**(22)

temperature = 300.0

class Molecule:
    def __init__(self, code):
        self.code = code
        self.functionals = []

    def addFunctional(self, functional, number):
        self.functionals.append((functional, number))

    def contains(self, element_name):
        return self.code.contains(elements[element_name])

    def line_shapes(self):
        lines = []

        for functional_tuple in self.functionals:
            functional = functional_dictionary[functional_tuple[0]]
            for symmetry in functional.symmetries:
                for property in symmetry.properties:
                    x = np.linspace(property.low, property.high)
                    y = functional.line_function(x, property.frequency_average(), property.intensity.value)
                    lines.append((x, y))

        return lines

    def branches(self):
        branches = []

        for functional_tuple in self.functionals:
            functional = functional_dictionary[functional_tuple[0]]
            for symmetry in functional.symmetries:
                for property in symmetry.properties:
                    branches.append(self.prBranches(property))

        return branches

    def atom_count(self):
        atoms = len(re.sub(r"[^A-Z]+",'',self.code))

        return atoms

    def prBranches(self, property):
        pr_branch_x = []
        pr_branch_y = []

        bcon = float(plank / (8 * math.pi * math.pi * light_speed * self.atom_count() * 10**(-44)))
        jmax = int(np.sqrt((boltzmann * temperature)/(2 * plank * light_speed * bcon)) - 0.5)

        for j in range(0, jmax):
            dcon = (bcon * 10 ** (-3)) / (j + 1)
            dcon_plus = (bcon * 10 ** (-3)) / (j + 2)
            spacing = 2 * bcon - ((4 * dcon_plus) * ((j + 2) ** 3)) + ((4 * dcon) * ((j + 1) ** 3))
            intensity_j = property.intensity.value * ((2* j) + 1) * np.e**(-((plank * light_speed * bcon * j * (j + 1))/(boltzmann * temperature)))

            position_j_pbranch = property.frequency_average() - spacing
            position_j_rbranch = property.frequency_average() + spacing
            pr_branch_x.append(position_j_pbranch)
            pr_branch_y.append(intensity_j)
            pr_branch_x.append(position_j_rbranch)
            pr_branch_y.append(intensity_j)

        return (pr_branch_x, pr_branch_y)

    def average_points(self):
        points = []

        for functional_tuple in self.functionals:
            functional_code = functional_tuple[0]
            if functional_code in functional_dictionary.keys():
                functional = functional_dictionary[functional_code]
                for symmetry in functional.symmetries:
                    for property in symmetry.properties:
                        points.append((property.frequency_average(), property.intensity.value))
                    

        return points
    
    def high_and_low_frequencies(self):
        frequencies = []

        for functional_tuple in self.functionals:
            functional_code = functional_tuple[0]
            if functional_code in functional_dictionary.keys():
                functional = functional_dictionary[functional_code]
                for symmetry in functional.symmetries:
                    for property in symmetry.properties:
                        frequencies.append((property.low, property.high, property.intensity.value))
                    

        return frequencies
    