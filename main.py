#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Name: LaSimulation
# Desc: Simulation du traffic autoroutier interactive
# Repo: https://github.com/Kakise/LaSimulation
# Author: Kakise
# License: GPL-3.0
# Path: -

import Lib.model as mdl
import random as rd
import os as os
import numpy as np

rd.seed(os.urandom(1024))

# Initialisation of the model
CarModel = mdl.IDM(130/3.6, 1.8, 78, 0.3, 2)
Util = mdl.Math()

# Consts
t=0
dt=0.01
end=60

# Run a simulation for (end - t) seconds.
# @param t:   Start                                       [s]
# @param dt:  Simulation interval (the lesser the better) [s]
# @param end: End of the simulation                       [s]
def finishedSim(t,dt,end):
    CarArr = [mdl.Vehicle(1, 1, 100, 0, 130/3.6, "car"), mdl.Vehicle(1, 1, 200, 0, 130/3.6, "car")]
    while t<end:
        t+=dt
        if float(np.ceil(t)) == float(t): # Ne fonctionne pas mdr
            CarArr = [mdl.Vehicle(1, 1, 0, 0, 130/3.6, "car")] + CarArr
        # Last car is handled separately
        CarArr[len(CarArr)-1].acc   = CarModel.acceleration(10**10, CarArr[len(CarArr)-1].speed, 10**10, 10**10)
        CarArr[len(CarArr)-1].speed = CarArr[len(CarArr)-1].speed + CarArr[len(CarArr)-1].acc * dt
        CarArr[len(CarArr)-1].u     = CarArr[len(CarArr)-1].u + CarArr[len(CarArr)-1].speed * dt + 1/2 * CarArr[len(CarArr)-1].acc * (dt**2)
        for i in reversed(range(len(CarArr)-1)):
            CarArr[i].acc   = CarModel.acceleration(CarArr[i+1].u-CarArr[i].u, CarArr[i].speed, CarArr[i+1].speed, CarArr[i+1].acc)
            CarArr[i].speed = CarArr[i].speed + CarArr[i].acc * dt
            CarArr[i].u     = CarArr[i].u + CarArr[i].speed * dt + 1/2 * CarArr[i].acc * (dt**2)
    # Très lent
    for car in CarArr:
        print ("Position", car.u, "Vitesse", car.speed*3.6, "km/h")

finishedSim(t, dt, end)

# TODO: Implement graphical sim
# -> remove vehicles when out of screen
# -> handle turns etc.
# -> Vehicle.u to coordinates

# TODO: Move everything to a python lib