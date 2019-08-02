import os
import json
import getpass

HISTORY_FILE_PATH = "C:/Users/{USER}/Documents/visual_tech/log/UEAnimImporter.history"
HISTORY_FILE_PATH = HISTORY_FILE_PATH.format(USER=getpass.getuser())


LOG = {
    "Projects": {}
}

def writeJson(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
        f.close()


def readJson(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data


def getImportedTime(project, filename):
    if not os.path.exists(HISTORY_FILE_PATH):
        return None
    _log = readJson(HISTORY_FILE_PATH)
    if not _log["Projects"][project]["Imported_files"].has_key(filename):
        return None
    file_info = _log["Projects"][project]["Imported_files"][filename]
    imported_time = file_info["imported_time"]
    return imported_time


def writeHistory(project, filename, imported_time):
    if not os.path.exists(os.path.dirname(HISTORY_FILE_PATH)):
        os.makedirs(os.path.dirname(HISTORY_FILE_PATH))
    if os.path.exists(HISTORY_FILE_PATH):
        _log = readJson(HISTORY_FILE_PATH)
    else:
        _log = LOG
    if not _log["Projects"].has_key(project):
        _log["Projects"] = {project: {"Imported_files": dict()}}
    if not _log["Projects"][project]["Imported_files"].has_key(filename):
        _log["Projects"][project]["Imported_files"][filename] = dict()

    _log["Projects"][project]["Imported_files"][filename]["imported_time"] = imported_time
    writeJson(_log, HISTORY_FILE_PATH)