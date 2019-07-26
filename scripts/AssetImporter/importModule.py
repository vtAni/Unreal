import re, os
import unreal
from PythonLibraries import AssetFunctions
reload(AssetFunctions)
from PythonLibraries import P4Functions
reload(P4Functions)


ANIM_SEQUENCE_PATH = "/Game/VisualTech/Animation"

class AssetImport():
    def __init__(self):
        self.VTP4 = P4Functions.VT_P4Class()

    def get_fileList(self):
        changeFileInfoDic = self.VTP4.getChangedFileInfo()
        return changeFileInfoDic

    def getCutNumber(self, fbxfile):
        filename = os.path.basename(fbxfile)
        p = re.compile("s\d+_c\d+")
        scene_cut = p.findall(filename)
        return scene_cut

    def getSkeleton(self, assetname):
        if unreal.EditorAssetLibrary.does_asset_exist(assetname):
            asset = unreal.load_asset(assetname)
            skeleton = asset.get_editor_property("skeleton").get_path_name()
        else:
            skeleton = None
        return skeleton

    def doImport(self, filesave):
        fileListDic = self.get_fileList()
        for fbxfile in fileListDic:
            clientFile = fileListDic[fbxfile]["clientFile"]
            animation_path = "/".join([ANIM_SEQUENCE_PATH, self.getCutNumber(clientFile)[0]])
            skeleton = self.getSkeleton("/".join([animation_path, os.path.splitext(os.path.basename(clientFile))[0]]))
            # skeleton = '/Game/VisualTech/Character/temp/JinF/mesh/JinF_Archer_Skeleton'
            animation_task = AssetFunctions.buildImportTask(clientFile, animation_path, filesave,
                                                            AssetFunctions.buildAnimationImportOptions(skeleton))

            AssetFunctions.executeImportTasks([animation_task])