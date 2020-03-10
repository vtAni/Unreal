import unreal
import site
import sys

site.addsitedir("C:/Python27/Lib/site-packages")
from PySide import QtCore, QtGui, QtUiTools


class VolumeSlider(QtGui.QDialog):

    def __init__(self, parent=None):
        super(VolumeSlider, self).__init__(parent)
        self.setWindowTitle("Visual Tech - Animation Importer")
        self.setGeometry(100, 50, self.width(), self.height())
        self.importBtn = QtGui.QPushButton("Import Animation")
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.importBtn)
        self.setLayout(layout)


APP = None
if not QtGui.QApplication.instance():
    APP = QtGui.QApplication(sys.argv)

main_window = VolumeSlider()
main_window.show()
unreal.parent_external_window_to_slate(main_window.winId())