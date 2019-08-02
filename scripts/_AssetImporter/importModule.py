"""
TODO
get file modified time.

save file imported time.
get file imported time.

"""

import re, os
import time
import unreal
from PythonLibraries import AssetFunctions

reload(AssetFunctions)
import P4Functions, history

reload(P4Functions)

ANIM_SEQUENCE_PATH = "/Game/VisualTech/Animation"


class AssetImport():
    def __init__(self):
        self.VTP4 = P4Functions.VT_P4Class()

    def get_fileInfoList(self):
        changeFileInfoDic = self.VTP4.getChangedFileInfo()
        return changeFileInfoDic

    def getCutNumber(self, fbxfile):
        filename = os.path.basename(fbxfile)
        p = re.compile("s\d+_c\d+")
        scene_cut = p.findall(filename)
        return scene_cut

    def getCharacterName(self, fbxfile):
        filename = os.path.basename(fbxfile)
        filename_split = filename.split("_")
        return filename_split[2]

    def getSkeleton(self, assetname):
        if unreal.EditorAssetLibrary.does_asset_exist(assetname):
            asset = unreal.load_asset(assetname)
            skeleton = asset.get_editor_property("skeleton").get_path_name()
        else:
            skeleton = None
        return skeleton

    def getProjectFilepath(self, fullpath=True):
        if fullpath:
            return unreal.Paths.get_project_file_path()
        else:
            return os.path.basename(unreal.Paths.get_project_file_path())

    def doImport(self, filesave, getLatestFile):
        fileListDic = self.get_fileInfoList()
        latestfilename = None
        latestfileinfo = None
        project = self.getProjectFilepath(fullpath=False)

        if not fileListDic:
            return
        if getLatestFile:
            fileListDic = {}
            tempFileInfo = self.get_fileInfoList()
            latestfilename = self.VTP4.getLatestFile(project, tempFileInfo)
            for latestfile in latestfilename:
                latestfileinfo = tempFileInfo[latestfile]
                fileListDic[latestfile] = latestfileinfo

        for fbxfile in fileListDic:
            clientFile = fileListDic[fbxfile]["clientFile"]
            # animation_path = "/".join([ANIM_SEQUENCE_PATH, self.getCutNumber(clientFile)[0]])
            animation_path = "/".join([ANIM_SEQUENCE_PATH, self.getCharacterName(clientFile)])
            skeleton = self.getSkeleton("/".join([animation_path, os.path.splitext(os.path.basename(clientFile))[0]]))
            if not skeleton:
                continue
            # skeleton = '/Game/VisualTech/Character/temp/JinF/mesh/JinF_Archer_Skeleton'
            animation_task = AssetFunctions.buildImportTask(clientFile, animation_path, filesave,
                                                            AssetFunctions.buildAnimationImportOptions(skeleton))

            AssetFunctions.executeImportTasks([animation_task])
            imported_time = time.time()
            history.writeHistory(project, fbxfile, imported_time)

        if getLatestFile:
            print latestfilename, " ", latestfileinfo
