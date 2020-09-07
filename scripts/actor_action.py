import unreal

editor_level_lib = unreal.EditorLevelLibrary()
editor_util = unreal.EditorUtilityLibrary()
layer_sys = unreal.LayersSubsystem()
system_lib = unreal.SystemLibrary()

editor_filter_lib = unreal.EditorFilterLibrary()

selected_assets = editor_util.get_selected_assets()

actors = editor_level_lib.get_selected_level_actors()

cameras = editor_filter_lib.by_class(actors, unreal.CineCameraActor)

parents = dict()
for i in cameras:
    attach_parent = i.get_attach_parent_actor()
    parents = {i: attach_parent}
    while True:
        parent = attach_parent.get_attach_parent_actor()
        if parent:
            parents[attach_parent] = parent
            attach_parent = parent
        else:
            break

sequence_asset = unreal.LevelSequence.cast(unreal.load_asset("/Game/VisualTech/Seq/NewLevelSequence"))

for i in parents:
    track_exsists = sequence_asset.find_binding_by_name(system_lib.get_display_name(parents[i]))
    if track_exsists.sequence: continue
    child_possessable = sequence_asset.add_possessable(object_to_possess=i)
    possessable = sequence_asset.add_possessable(object_to_possess=parents[i])
    attach_track = child_possessable.add_track(track_type=unreal.MovieScene3DAttachTrack)
    attach_section = attach_track.add_section()

    attach_binding_id = unreal.MovieSceneObjectBindingID()
    attach_binding_id.set_editor_property("Guid", possessable.get_id())
    attach_section.set_editor_property('constraint_binding_id', attach_binding_id)
    attach_section.set_range_seconds(sequence_asset.get_playback_start_seconds(), sequence_asset.get_playback_end_seconds())