import os
import site
site.addsitedir(r"C:\Python27\Lib\site-packages")
site.addsitedir(r"\\vt_server1\ANIMATION\global\Lib\site-packages")
from P4 import P4, P4Exception


class VT_P4Class():
    def __init__(self):
        self.p4 = P4()
        self.p4.connect()

    def getLatestFile(self, fileState):
        latestFile = None
        latestTime = 0
        for filename in fileState:
            clientFile = fileState[filename]["clientFile"]
            # modTime = int(fileState[filename]["headModTime"])
            # headTime = int(fileState[clientFile]["headModTime"])
            # print filename, modTime, headTime
            modTime = os.path.getctime(clientFile)
            if latestTime < modTime:
                latestTime = modTime
                latestFile = filename
        return latestFile

    def getChangedFiles(self):
        changes = self.p4.fetch_change()
        if "Files" not in changes.keys():
            return None
        changedFiles = changes["Files"]
        fbxFiles = list()
        for cf in changedFiles:
            if cf.endswith("FBX") or cf.endswith("fbx"):
                fbxFiles.append(cf)
        return fbxFiles

    def getChangedFileInfo(self):
        fileState = dict()
        fbxFiles = self.getChangedFiles()
        if fbxFiles:
            for fbxfile in fbxFiles:
                fileState[fbxfile] = self.p4.run_fstat(fbxfile)[0]
        return fileState



# cls = VT_P4Class()
# fileInfo = cls.getChangedFileInfo()
# print cls.getLatestFile(fileInfo)