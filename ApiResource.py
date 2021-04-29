from Comment import *
import os 
import re
class ApiResource:
    methodTypes = {"index": "get", "create": "get", "store": "post", "show": "get", "edit": "get", "update": "patch", "destroy": "delete"}

    def __init__(self, path, fileName):
        self.path = path
        self.fileName = fileName

        self.setLines()
        self.createComments()


    def __str__(self):
        return f"ApiResource: {self.fileName}"
    
    def setLines(self):
        filePath = f"{self.controllersDir}/{self.fileName}.php"
        if (os.path.exists(filePath)):
            funcFile = open(filePath, 'r', encoding='utf-8')
            self.lines = funcFile.readlines()
        else:
            self.lines = None
    
    def findFunctions(self):
        functionNames = []
        methodTypesStr = "|".join([methodType for methodType in self.methodTypes ])
        regex = re.compile(f"[public|private][\s]+function[\s]+({methodTypesStr})\(")
        for line in self.lines:
            funcMatch = re.search(regex, line)
            if funcMatch:
                funcName = funcMatch.group(1)
                functionNames.append(funcName)
        return functionNames

    def createComments(self):
        self.commentsDict = {}
        if self.lines:
            functionNames = self.findFunctions()
            for funcName in functionNames:
                methodType = self.methodTypes.get(funcName)
                self.commentsDict[funcName] = methodType








