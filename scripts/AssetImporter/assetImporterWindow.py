import site
site.addsitedir("C:/Python27/Lib/site-packages")
from PySide import QtGui, QtUiTools
import AssetFunctions

WINDOW_NAME = "VT Asset Importer"
UI_FILE_FULLNAME = "C:/Users/kayamayan/Documents/visual_tech/Unreal/scripts/AssetImporter/ui/mainWindow.ui"

character_asset = 'D:/perforce/Resource/BnS/BnS_Archer/2_FinalData/Character/JinF_Archer/FBX/JinF_Archer_test.FBX'
animation_asset = 'D:/perforce/Resource/BnS/BnS_Archer/2_FinalData/Animation/Archer/s05_c007_X_Archer_Battle_C.fbx'

class AssetImporterWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(AssetImporterWindow, self).__init__(parent)
        self.aboutToClose = None
        self.widget = QtUiTools.QUiLoader().load(UI_FILE_FULLNAME)
        self.widget.setParent(self)
        self.setWindowTitle(WINDOW_NAME)
        self.setGeometry(100, 50, self.widget.width(), self.widget.height())
        self.initialiseWidget()

    def closeEvent(self, event):
        if self.aboutToClose:
            self.aboutToClose(self)
        event.accept()


    def initialiseWidget(self):
        self.widget.animAssetPath_lineEdit.setText(animation_asset)
        self.widget.characterAssetPath_lineEdit.setText(character_asset)
        self.widget.skeletalPath_lineEdit.setText('/Game/VisualTech/Character/JinF_Archer_Skeleton')
        self.widget.importCharacter_pushButton.clicked.connect(self.importCharacter)
        self.widget.importAnim_pushButton.clicked.connect(self.importAnim)


    def importCharacter(self):
        characterAsset = str(self.widget.characterAssetPath_lineEdit.text())
        options = AssetFunctions.buildSkeletalMeshImportOptions()
        task = AssetFunctions.buildImportTask(filename=characterAsset, destination_path='/Game/VisualTech/Character', options=options)
        AssetFunctions.executeImportTasks([task])

    def importAnim(self):
        animAsset = str(self.widget.animAssetPath_lineEdit.text())
        skeletalPath = str(self.widget.skeletalPath_lineEdit.text())
        options = AssetFunctions.buildAnimationImportOptions(skeleton_path=skeletalPath)
        task = AssetFunctions.buildImportTask(filename=animAsset,
                                              destination_path='/Game/VisualTech/Animation',
                                              options=options)
        AssetFunctions.executeImportTasks([task])