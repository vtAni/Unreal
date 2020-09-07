import unreal

editor_level_lib = unreal.EditorLevelLibrary()
editor_util = unreal.EditorUtilityLibrary()
layer_sys = unreal.LayersSubsystem()
system_lib = unreal.SystemLibrary()
editor_filter_lib = unreal.EditorFilterLibrary()


def bake_keyframes(camera):
    scene_component = camera.get_editor_property('root_component')
    sequence_start = sequence_asset.get_playback_start_seconds()
    sequence_end = sequence_asset.get_playback_end_seconds()

    possessable = sequence_asset.add_possessable(object_to_possess=i)
    for track in possessable.get_tracks():
        if not isinstance(track, unreal.MovieScene3DTransformTrack):
            continue
        for section in track.get_sections():
            if isinstance(section, unreal.MovieScene3DTransformSection):
                # print("\tSection: " + section.get_name())
                cam_location = scene_component.get_editor_property('relative_location')
                cam_rotation = scene_component.get_editor_property('relative_rotation')

                print cam_location, cam_rotation
                for channel in section.get_channels():
                    if channel.get_name() == "Rotation.X":
                        key = cam_rotation.roll
                    elif channel.get_name() == "Rotation.Y":
                        key = cam_rotation.pitch
                    elif channel.get_name() == "Rotation.Z":
                        key = cam_rotation.yaw
                    else:
                        continue
                    for t in range(int(sequence_start) * 30, int(sequence_end) * 30 + 1):
                        print(channel.get_name(), key)
                        new_key = channel.add_key(unreal.FrameNumber(t), key)


actors = editor_level_lib.get_selected_level_actors()
cameras = editor_filter_lib.by_class(actors, unreal.CineCameraActor)

sequence_asset_path = "/Game/VisualTech/Seq/NewLevelSequence"
sequence = unreal.load_asset(sequence_asset_path)
sequence_asset = unreal.LevelSequence.cast(sequence)

actors = editor_level_lib.get_selected_level_actors()
cameras = editor_filter_lib.by_class(actors, unreal.CineCameraActor)

for camera in cameras:
    bake_keyframes(camera)