import CustomDataStructures as DataS
import copy

class path():
    def __init__(self,path,startNode,endNode):
        self.path = path
        self.endNode = endNode
        self.startNode = startNode
        self.cacheID = 0

class cache:
    def __init__(self):
        self.dict = {}
        self.cacheID = 0

    def add(self,path):
        self.dict[self.hashPath(path.startNode,path.endNode)] = path
        path.cacheID = self.cacheID
    def reset(self):
        self.cacheID +=1

    def hashPath(self,startNode,endNode):
        return (startNode,endNode)

    def get(self,startNode,endNode):
        hash = self.hashPath(startNode,endNode)
        reverseHash = self.hashPath(endNode,startNode)
        if hash in self.dict and self.dict[hash].cacheID == self.cacheID:
            return (self.dict[hash].path, 0)

        if reverseHash in self.dict and self.dict[reverseHash].cacheID == self.cacheID:
            reversed_path = copy.deepcopy(self.dict[reverseHash].path)[::-1]
            return (reversed_path, 1)
        return None
