# -*- coding: utf-8 -*-
"""
***************************************************************************
*   Copyright (c) 2013, 2014, 2015                                        *
*   Original code by:                                                     *
*   Ulrich Brammer <ulrich1a[at]users.sourceforge.net>                    *
*                                                                         *
*   This file is a supplement to the FreeCAD CAx development system.      *
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU Lesser General Public License (LGPL)    *
*   as published by the Free Software Foundation; either version 2 of     *
*   the License, or (at your option) any later version.                   *
*   for detail see the LICENCE text file.                                 *
*                                                                         *
*   This software is distributed in the hope that it will be useful,      *
*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
*   GNU Library General Public License for more details.                  *
*                                                                         *
*   You should have received a copy of the GNU Library General Public     *
*   License along with this macro; if not, write to the Free Software     *
*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
*   USA                                                                   *
*                                                                         *
***************************************************************************
"""
from screw_maker import *

# negative-threaded rod for tapping holes

def makeScrewTap(self): # dynamically loaded method of class Screw
    ThreadType = self.fastenerDiam
    if ThreadType != 'Custom':
        dia = self.getDia(ThreadType, True)
        if self.fastenerType == "ScrewTap":
            P, tunIn, tunEx = FsData["tuningTable"][ThreadType]
        elif self.fastenerType == 'ScrewTapInch':
            P = FsData["asmeb18.3.1adef"][ThreadType][0]
    else:  # custom pitch and diameter
        P = self.customPitch
        if self.sm3DPrintMode:
            dia = self.smNutThrScaleA * self.customDia + self.smNutThrScaleB
        else:
            dia = self.customDia
    residue, turns = math.modf(self.fastenerLen / P)
    # FreeCAD.Console.PrintMessage("turns:" + str(turns) + "res: " + str(residue) + "\n")
    if residue > 0.00001:
        turns += 1.0
    if self.rThread:
        screwTap = self.makeInnerThread_2(dia, P, int(turns), None, 0.0)
        # screwTap.translate(Base.Vector(0.0, 0.0, (1-residue)*P))
    else:
        H = P * math.cos(math.radians(30))  # Thread depth H
        r = dia / 2.0

        # points for inner thread profile
        adjusted_l = turns * P
        Pnt0 = Base.Vector(0.0, 0.0, 0)
        Pnt1 = Base.Vector(r - H * 5.0 / 8.0, 0.0, 0)
        Pnt2 = Base.Vector(r - H * 5.0 / 8.0, 0.0, -adjusted_l)
        Pnt3 = Base.Vector(0.0, 0.0, -adjusted_l)

        edge1 = Part.makeLine(Pnt0, Pnt1)
        edge2 = Part.makeLine(Pnt1, Pnt2)
        edge3 = Part.makeLine(Pnt2, Pnt3)
        aWire = Part.Wire([edge1, edge2, edge3])
        headShell = aWire.revolve(Base.Vector(0.0, 0.0, 0.0), Base.Vector(0.0, 0.0, 1.0), 360.0)
        screwTap = Part.Solid(headShell)
    return screwTap