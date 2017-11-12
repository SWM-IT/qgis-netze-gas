# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Branches Helper
                                 Helper to handle hierarchy of branches
                             -------------------
        begin                : 2017-11-12
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Markus Hesse / Mettenmeier GmbH
        email                : markus.hesse@mettenmeier.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

class BranchesHelper(object):
    MASTER_BRANCH_NAME = "master"
    
    def __init__(self, brancheNames):
        self.brancheNames = brancheNames
    
    
    def subBranchNameFor(self, branchName, parentBranchName):
        if parentBranchName == self.MASTER_BRANCH_NAME:
            return branchName
        else:
            return branchName + "_($%s$)" % (parentBranchName) 
        
        
    def displayName(self, branchName):
        index = branchName.find("($")
        
        if index > -1:
            return branchName[:index-1]
        else:
            return branchName
                
        
    def parentName(self, branchName):
        # The master branch has no parent
        if branchName == self.MASTER_BRANCH_NAME:
            return None
        
        index = branchName.find("($")
        if index > -1:
            return branchName[index + 2:-2]
        else:
            return self.MASTER_BRANCH_NAME

        
    def childrenOfBranch(self, parentBranchName):
        children = []
        for branchName in self.brancheNames:
            if self.parentName(branchName) == parentBranchName:
                children.append(branchName)
                
        return children
            