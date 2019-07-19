import unreal

def doIt(name=None, path=None):
    unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name=name,
                                                            package_path=path,
                                                            asset_class=unreal.LevelSequence,
                                                            factory=unreal.LevelSequenceFactoryNew())
