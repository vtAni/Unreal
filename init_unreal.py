import shutil
import unreal
import site
server_paths = [
    "C:/Users\kayamayan.NC-KOREA/Documents/visual_tech/vtTools/Unreal/scripts",
    "//vt_server1/ANIMATION/global/Lib/site-packages"
]
for path in server_paths:
    site.addsitedir(path)

#root_path = unreal.SystemLibrary.get_project_content_directory()
#content_path = "VisualTech/Blueprint/_AnimationImporter"
#unique_path = root_path + content_path#"/".join([root_path, content_path])

#if not unreal.EditorAssetLibrary.does_asset_exist(asset_path="/Game/" + content_path + "/_AnimationImporter"):
#    shutil.copytree("//vt_server1/ANIMATION/Unreal/blueprints/AnimationImporter", unique_path)


#import AnimImporterWin.MainWindow
#reload(AnimImporterWin.MainWindow)
