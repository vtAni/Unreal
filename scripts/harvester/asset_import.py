
import os
import unreal


class AssetImport():
    def __init__(self, asset_data) -> None:
        self.asset_data = asset_data
        self.import_task = unreal.AssetImportTask()

    def abc_import_option(self):
        options = unreal.AbcImportSettings()
        options.import_type = unreal.AlembicImportType.GEOMETRY_CACHE
        options.sampling_settings.skip_empty = True
        options.conversion_settings.rotation = {"x": 90.0, "y": 0.0, "z": 0.0}
        return options

    def fbx_import_option(self):
        options = unreal.FbxImportUI()
        options.auto_compute_lod_distances = False
        options.lod_number = 0
        options.import_as_skeletal = bool(self.asset_data.get("skeletal_mesh"))
        options.import_animations = bool(self.asset_data.get("animation"))
        options.import_materials = bool(self.asset_data.get("import_materials"))
        options.import_textures = bool(self.asset_data.get("import_textures"))
        options.import_mesh = bool(self.asset_data.get("import_mesh"))
        options.static_mesh_import_data.generate_lightmap_u_vs = False
        options.lod_distance0 = 1.0

        # if this is a skeletal mesh import
        if bool(self.asset_data.get("skeletal_mesh")):
            options.skeletal_mesh_import_data.normal_import_method = unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS
            options.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH
            options.skeletal_mesh_import_data.import_mesh_lo_ds = bool(self.asset_data.get("lods"))

            assetname = self.asset_data.get("skeletal_mesh_game_path")
            if assetname.find("/") != -1:
                unreal.log(unreal.EditorAssetLibrary.does_asset_exist(assetname))
                if unreal.EditorAssetLibrary.does_asset_exist(assetname):
                    asset = unreal.load_asset(assetname)
                    skeleton_asset_name = os.path.splitext(asset.get_editor_property("skeleton").get_path_name())[0]
                    skeleton_asset = unreal.load_asset(skeleton_asset_name)
                    unreal.log(skeleton_asset)

                    if skeleton_asset:
                        options.set_editor_property("skeleton", skeleton_asset)

        # if this is an static mesh import
        if not bool(self.asset_data.get("skeletal_mesh")):
            options.static_mesh_import_data.normal_import_method = unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS_AND_TANGENTS
            options.mesh_type_to_import = unreal.FBXImportType.FBXIT_STATIC_MESH
            options.static_mesh_import_data.import_mesh_lo_ds = bool(self.asset_data.get("lods"))

        # if this is an animation import
        if bool(self.asset_data.get("animation")):
            assetname = self.asset_data.get("skeletal_mesh_game_path")
            if unreal.EditorAssetLibrary.does_asset_exist(assetname):
                asset = unreal.load_asset(assetname)
                skeleton_asset_name = os.path.splitext(asset.get_editor_property("skeleton").get_path_name())[0]
                skeleton_asset = unreal.load_asset(skeleton_asset_name)
                unreal.log(skeleton_asset)
                # '    skeleton_asset = unreal.load_asset(r"{0}")'.format(asset_data.get("skeleton_game_path")),

                # if a skeleton can be loaded from the provided path
                if skeleton_asset:
                    options.set_editor_property("skeleton", skeleton_asset)
                    options.set_editor_property("original_import_type", unreal.FBXImportType.FBXIT_ANIMATION)
                    options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_ANIMATION)
                else:
                    raise RuntimeError("Unreal could not find a skeleton here: {0}".format(self.asset_data.get("skeletal_mesh_game_path")))
        return options

    def do_import(self):
        import_task = unreal.AssetImportTask()
        import_task.filename = self.asset_data.get("fbx_file_path")
        import_task.destination_path = self.asset_data.get("game_path")
        import_task.automated = not bool(self.asset_data.get("advanced_ui_import"))
        import_task.replace_existing = True
        import_task.save = self.asset_data.get("file_save")
        
        # abc import options
        if self.asset_data.get("abc_import"):
            options = self.abc_import_option()
        else:
            options = self.fbx_import_option()

        # assign the options object to the import task and import the asset
        import_task.options = options
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([import_task])
        skeleton_asset_name = os.path.splitext(options.get_editor_property("skeleton").get_path_name())[0]
        skeleton_asset = unreal.load_asset(skeleton_asset_name)

        if skeleton_asset:
            unreal.log('SAVE SKELETON ASSET!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            unreal.log(skeleton_asset)
            unreal.EditorAssetLibrary.save_asset(skeleton_asset)