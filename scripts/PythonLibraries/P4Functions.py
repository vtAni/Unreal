import site
site.addsitedir(r"C:\Python27\Lib\site-packages")
from P4 import P4, P4Exception


class VT_P4Class():
    def __init__(self):
        self.p4 = P4()
        self.p4.connect()

    def getChangedFiles(self):
        changes = self.p4.fetch_change()
        changedFiles = changes["Files"]
        fbxFiles = list()
        for cf in changedFiles:
            if cf.endswith("FBX") or cf.endswith("fbx"):
                fbxFiles.append(cf)
        return fbxFiles

    def getChangedFileInfo(self):
        fileState = dict()
        fbxFiles = self.getChangedFiles()
        for fbxfile in fbxFiles:
            fileState[fbxfile] = self.p4.run_fstat(fbxfile)[0]
        return fileState

            # for i in fileState:
            #     for j in i:
            #         print j, " ", i[j]

    # changelist = p4.run_changes('//Resource/BnS/BnS_WCS19/2_FinalData/Animation...@2019/07,@now')
    # for c in changelist:
    #       print c