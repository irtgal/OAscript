import re
import os
import ntpath

class Comment:
    controllersDir = "C:/Users/Student/Desktop/result/backend/app/Http/Controllers/"


    def __init__(self, methodType, path, fileName, funcName = False):
        self.path = path
        self.methodType = methodType
        self.fileName = fileName.replace("\\", "/")
        self.funcName = funcName

        self.responses = [(200, "OK")]
        self.parameters = {} # {name: [req, in, type], ...}
        self.commentStr = ""
        self.summary = None

        self.getPathParameters()
        self.setOperationId()
        self.setLines()
        self.findExistingComment()

    def __str__(self):
        return "Comment: " + self.path

    def getPathParameters(self):
        parameters = re.findall("\{(.*?)\}", self.path)
        for param in parameters:
            self.parameters[param] = ["true", "path", None]
    
    def setOperationId(self):
        name = ntpath.basename(self.fileName).replace("Controller", "")
        self.operationId = self.funcName + name
    
    def setLines(self):
        filePath = self.controllersDir + self.fileName + ".php"
        if (os.path.exists(filePath)):
            funcFile = open(filePath, 'r', encoding='utf-8')
            self.lines = funcFile.readlines()
        else:
            raise Exception(f"Couldn't find \"{self.fileName}\"")

    def addResponse(self, response, description):
        self.responses.append((response, description))


    def createHead(self):
        result = (
            "\t/**\n"
            f"\t* @OA\\{self.methodType}(\n"
            f'\t*\tpath="{self.path}",\n'
            f'\t*\toperationId="{self.operationId}",\n'
            f'\t*\tsummary="{self.summary}",\n'
            )
        self.commentStr += result

    def createParameters(self):
        result = ""
        for param in self.parameters:
            req, where, pType = self.parameters[param]
            result += (
                "\t*\t@OA\Parameter(\n"
                    f"\t*\t\tname=\"{param}\",\n"
                    f"\t*\t\trequired={req},\n"
                    f"\t*\t\tin=\"{where}\",\n"
                    "\t*\t\t@OA\Schema(\n"
                        f"\t*\t\t\ttype=\"{pType}\"\n"
                    "\t*\t\t)\n"
                "\t*\t),\n"
            )
        self.commentStr += result

    def createResponses(self):
        result = ""
        for response in self.responses:
            result += (
                f'\t*\t@OA\\Response(\n'
                f'\t*\t\tresponse={response[0]},\n'
                f'\t*\t\tdescription="{response[1]}",\n'
                f'\t*\t)'
            )
            result += ",\n" if response != self.responses[-1] else "\n"
        self.commentStr += result

    def close(self):
        self.commentStr += "\t* )\n\t*/\n"

    def buildComment(self):
        self.commentStr = ""
        self.createHead()
        self.createParameters()
        self.createResponses()
        self.close()   

    def writeComment(self):
        filePath = self.controllersDir + self.fileName + ".php"
        if (self.lines and self.commentStr != ""):
            funcIndex = self.findFunctionIndex()
            lines = self.lines
            lines.insert(funcIndex, self.commentStr)
            lines = "".join(lines)
            funcFile = open(filePath, "w", encoding='utf-8')
            funcFile.write(lines)
            funcFile.close()
            print("\n"*20)
        else:
            raise Exception(f"Couldn't write \"{self.fileName}@{self.funcName}\"")


    def findFunctionIndex(self):
        for lineCount, line in enumerate(self.lines):
            if re.search(r"[public|private][\s]+function[\s]+"+self.funcName, line):
                return lineCount 
        raise Exception(f"Couldn't find function \"{self.funcName}\"")

    def removeExistingComment(self):
        for indx in self.existingCommentIndexes:
            del self.lines[indx]
        self.existingCommentIndexes = []

    def findExistingComment(self):
        self.existingCommentIndexes = []
        funcIndex = self.findFunctionIndex()
        beforeFunc = self.lines[funcIndex-1].strip()
        lines = self.lines.copy()
        if beforeFunc == "*/": #check if there is a comment
            for i in range(funcIndex-1, funcIndex-15, -1):
                if "@OA" in lines[i]:
                    raise Exception("OpenAPI comment already exists")
                    break
                self.existingCommentIndexes.append(i)
                if lines[i].strip() == "/**":
                    break
                line = re.sub(r'\*|\$','', lines[i]).strip()
                if "@param" in line:
                    try:
                        y, pType, name = line.split()
                        if name in self.parameters:
                            self.parameters[name][2] = pType 
                    except Exception:
                        raise Exception("Couldn't find parameter information")
                elif re.match("[\w.,:-]+", line):
                    self.summary = line
            self.removeExistingComment()
                




