import webbrowser
import os
import json 

commentSeperator = "\n" + "*" * 100
seperator = "-" * 100
def inputSummary(c):
    print(seperator)
    found = f' (found: "{c.summary}")' if c.summary else ''
    summary = input(f"Set FUNCTION SUMMARY{found}: \n-> ")
    c.summary = summary if summary else c.summary

def inputResponses(c):
    print(seperator)
    description = " "
    number = " "
    while description != "" and number != "":
        number = input("Set RESPONSE NUMBER: ")
        if number == "": break
        description = input("Set RESPONSE DESCRIPTION: ")
        if description == "": break
        c.responses.append((number, description))
        print()

def inputParamTypes(c):
    print(seperator)
    i = 0
    for param in c.parameters:
        foundType = c.parameters[param][2]
        found = f' (found: "{foundType}")' if foundType else ""
        pType = input(f"Set PARAMETER TYPE for \"{param}\"{found}: ")
        c.parameters[param][2] = pType if pType else foundType
        i += 1
    print("\nSet QUERY parameters ")
    pType = " "
    param = " "
    while param != "" and pType != "":
        param = input("Set PARAMETER NAME: ")
        if param == "": break
        description = input("Set PARAMETER TYPE: ")
        if pType == "": break
        c.parameters[param] = ["true", "query", pType]
        print()
    print(seperator)

def clearComment(c):
    c.summary = ""
    for param in c.parameters:
        c.parameters[param][2] = None
    c.responses = [c.responses[0]]
    c.commentStr = ""



def confirmWrite(c, routesCount):
    confirm = input("Post (p) or Redo (r)? ")
    if confirm == "r":
        clearComment(c)
        formComment(c, routesCount)
    elif confirm == "p":
        return True
    else:
        return confirmWrite(c, routesCount)

def formComment(c, routesCount):
    print(commentSeperator)
    print(f"Index at {routesCount}")
    print(f"Entry for \"{c.fileName}@{c.funcName}\"\n{c.path}")
    inputSummary(c)
    inputResponses(c)
    inputParamTypes(c)
    c.buildComment()
    print(c.commentStr)
    print(commentSeperator)
    confirmWrite(c, routesCount)


def setApiFile(path):
    if (os.path.exists(path)):
        with open(path, 'r', encoding='utf-8') as apiFile:
            return apiFile.readlines()
    else:
        print("Error: Couldn't find api.php file")


