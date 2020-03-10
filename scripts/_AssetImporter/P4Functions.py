import os
import site
site.addsitedir(r"C:\Python27\Lib\site-packages")
site.addsitedir(r"\\vt_server1\ANIMATION\global\Lib\site-packages")
from P4 import P4, P4Exception
import history;reload(history)

class VT_P4Class():
    def __init__(self):
        self.p4 = P4()
        self.p4.connect()
        self.CHARSET = ["utf8",
                   "none"]
        self.charsetIndex = self.CHARSET.index(self.p4.charset)

    def fetchChange(self):
        try:
            changes = self.p4.fetch_change()
        except P4Exception as e:
            self.p4.charset = self.CHARSET[int(not self.charsetIndex)]
            changes = self.p4.fetch_change()
        return changes

    def getLatestFile(self, project, fileState):
        latestFile = list()
        latestTime = 0
        for filename in fileState:
            imported_time = history.getImportedTime(project, filename)
            clientFile = fileState[filename]["clientFile"]
            # modTime = int(fileState[filename]["headModTime"])
            # headTime = int(fileState[clientFile]["headModTime"])
            # print filename, modTime, headTime
            modTime = os.path.getctime(clientFile)
            # if latestTime < modTime:
            #     latestTime = modTime
            if not imported_time:
                latestFile.append(filename)
            elif imported_time and modTime > imported_time:
                latestFile.append(filename)
        return latestFile

    def getChangedFiles(self):
        changes = self.fetchChange()
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