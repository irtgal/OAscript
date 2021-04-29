import os
import re
from scripts import *
from Comment import *
from ApiResource import *


#directories 
baseDir = "C:/Users/Student/Desktop/result/backend"
Comment.haveSecurity = ["client"]

controllersDir = baseDir + "/app/Http/Controllers"

Comment.controllersDir = controllersDir
ApiResource.controllersDir = controllersDir
routePath = baseDir + "/routes/api.php"
routeLines = setApiFile(routePath)


normalPattern = re.compile(r"^Route::(post|get|patch|delete|any)\(\'(.*)\'\,[\s]*\'(.*)@(.*)\'\)\;")
resourcePattern = re.compile(r"^Route::apiResource\(\'(.*)\'\,[\s]*\'(.*)\'\)\;")
routesCount = otherCount =  0
startIndex = int(input("Select starting index: "))
for line in routeLines:
    normalMatch = normalPattern.search(line)
    resourceMatch = resourcePattern.search(line)
    if normalMatch:
        if routesCount >= startIndex:
            try:
                methodType, path, fileName, funcName = normalMatch.groups()
                c = Comment(methodType, path, fileName, funcName)
                webbrowser.open(f'{c.controllersDir}/{c.fileName}.php')
                formComment(c, routesCount)
                c.writeComment()
            except Exception as error:
                print(f"ERROR: {error} - {line}")
        routesCount += 1

    elif resourceMatch:
        if routesCount >= startIndex:
            try:
                path, fileName = resourceMatch.groups()
                apiresource = ApiResource(path, fileName)
                for funcName, methodType in apiresource.commentsDict.items():
                    c = Comment(methodType, path, fileName, funcName)
                    webbrowser.open(f'{c.controllersDir}/{c.fileName}.php')
                    formComment(c, routesCount)
                    c.writeComment()
            except Exception as error:
                 print(f"ERROR: {error} - {line}")
        routesCount += 1
    else:
        otherCount += 1

print(f"Routes: {routesCount}, other: {otherCount}")