# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 20:05:50 2021

@author: matip
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Fractal:
    
    def __init__(self, width=640, height=480, radius=0.7885, frames=60, zoom=1, iterations=50, cmap = 'afmhot', caption = False):
        self.width   = width  # x plane resolution
        self.height  = height # y plane resolution
        self.radius  = radius # magnitude of vector that is gonna be rotating
        self.frames  = frames # how much frames are gonna be generated to reach full rotation
        self.zoom    = zoom
        self.cmap    = cmap   # colors of map, default one is really pretty, I also reccomend 'inferno'
        self.caption = caption
        self.animation = None
        self.iterations = iterations # how many iterations before we decide that a point has a stable orbit or has converged
        self.radians = np.linspace(0, 2*np.pi, self.frames)

    # regular stationary figure, but animation is much cooler, this setting is good to generate a nice animation
    def SetFigure(self):
        self.fig = plt.figure(figsize=(10,8))
        self.ax  = plt.axes()
        self.ax.axis('off')
        self.ax.set(frame_on=False)
        
    
    def JuliaSet(self, c, x=0, y=0):
        boxWidth     = 1.5
        boxHeight    = 1.5
        xLeftBorder  = x - boxWidth /self.zoom
        xRightBorder = x + boxWidth /self.zoom
        yBotBorder   = y - boxHeight/self.zoom
        yTopBorder   = y + boxHeight/self.zoom
        
        x = np.linspace(xLeftBorder, xRightBorder, self.width ).reshape(1, self.width )
        y = np.linspace(yBotBorder,  yTopBorder,   self.height).reshape(self.height, 1)
        
        z = x + 1.0j*y
        
        c = np.full(z.shape, c)
        
        divergenceTime = np.zeros(c.shape, dtype=int)
        
        m = np.full(z.shape, True, dtype=bool)
        
        # algorirthm starts here
        for i in range(self.iterations):
            z[m] = z[m]**2 + c[m]
            
            #if a point is further than 2 from the plane's origin it's gonna blow up so there's no point tracking it any longer 
            m[np.abs(z) > 2] = False
            
            divergenceTime[m] = i
        
        return divergenceTime
    
    def GetVectorComponents(self, i):
        cx = self.radius * np.cos(self.radians[i])
        cy = self.radius * np.sin(self.radians[i])
        return cx, cy
    
    def Animate(self, i):
        cx, cy = self.GetVectorComponents(i)
        img = self.ax.imshow(self.JuliaSet(c = complex(cx, cy)), interpolation ='bilinear', cmap = self.cmap)
        return [img]
    
    def DisplayAnimation(self):
        self.SetFigure()
        self.animation = animation.FuncAnimation(self.fig, self.Animate, frames=self.frames, interval=50, blit=True)
        return self.animation
            
    def DisplayFigure(self, cx=0, cy=0):
        self.SetFigure()
        X = np.empty((self.width, self.height))
        X = self.JuliaSet(c=complex(cx, cy))
        if self.caption:                                                 # there's a way better way of doing this, but it will suffice for a few days
            self.ax.text(0, 0, 'c = ' + str(cx) + ' + ' + 'i' + str(cy)) #
        self.ax.imshow(X, interpolation = 'bilinear', cmap=self.cmap)
        
        

        