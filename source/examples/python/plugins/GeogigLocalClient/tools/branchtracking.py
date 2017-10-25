# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Branch Tracking
                                 Keep track on created branches and last 
                                 selected branch
                             -------------------
        begin                : 2017-10-25
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

# FIXME: Some parts are copied from geogig.tools.layertracking. Wouldbe nice to 
# merge that together

import os
import json

from json.decoder import JSONDecoder
from json.encoder import JSONEncoder

from geogig.tools.utils import userFolder


class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def decoder(jsonobj):
    if 'repoUrl' in jsonobj:
        return TrackedRepository(jsonobj['repoUrl'],
                                 jsonobj['brancheHierarchy'],
                                 jsonobj['lastBranchPath'])
    else:
        return jsonobj
    
class TrackedRepository(object):
    def __init__(self, repoUrl, brancheHierarchy = None, lastBranchPath = None):
        self.repoUrl = repoUrl
        self.brancheHierarchy = brancheHierarchy
        self.lastBranchPath = lastBranchPath
        
class BranchesTracker(object):
    
    fileName = "trackedBranches"
    
    def __init__(self):
        self.trackedRepositories = self.readTrackedBranches() 
        
        if self.trackedRepositories == None:
            self.trackedRepositories = []
    
    def fullFileName(self):
        """Full file name including folders etc."""
        return os.path.join(userFolder(), self.fileName)
    
    def saveTrackedBranches(self):
        """Save branch tracking information in file"""
        filename = self.fullFileName()
        with open(filename, "w") as f:
            f.write(json.dumps(self.trackedRepositories, cls = Encoder))
        
    def readTrackedBranches(self):
        """Read branch tracking information from file"""
        tracked = None
        try:
            filename = self.fullFileName()
            if os.path.exists(filename):
                with open(filename) as f:
                    lines = f.readlines()
                    jsonstring = "\n".join(lines)
                    if jsonstring:
                        tracked = JSONDecoder(object_hook = decoder).decode(jsonstring)
        except KeyError:
            pass
        
        return tracked
    
    def addBranchInfo(self, repo, BranchPath):
        currentRepo = None
        
        for trackedRepo in self.trackedRepositories:
            if trackedRepo.repoUrl == repo.url:
                currentRepo = trackedRepo
                break
            
        if not currentRepo:
            currentRepo = TrackedRepository(repo.url)
            self.trackedRepositories.append(currentRepo)
            
        currentRepo.lastBranchPath = BranchPath
        self.saveTrackedBranches()
        
    
    def getCurrentBranchPath(self, repo):
        if not repo:
            return 
        
        currentRepo = None
        for trackedRepo in self.trackedRepositories:
            if trackedRepo.repoUrl == repo.url:
                currentRepo = trackedRepo
                break        
            
        if currentRepo:
            return currentRepo.lastBranchPath
            
    