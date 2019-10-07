import os
import time
import datetime
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

def cleanupHistory(days=30.0):
    _log = getHistory()
    _log_tmp = getHistory()
    _projects = _log["Projects"]
    if not _projects:
        return
    for prj in _projects:
        if _projects[prj].has_key("Last_edited"):
            last_edit_time = _projects[prj]["Last_edited"]
            ctime = time.gmtime(time.time())
            dtime = datetime.datetime(ctime.tm_year, ctime.tm_mon, ctime.tm_mday, ctime.tm_hour, ctime.tm_min)

            last_edit_gmtime = time.gmtime(last_edit_time)
            last_edit_dtime = datetime.datetime(
                last_edit_gmtime.tm_year,
                last_edit_gmtime.tm_mon,
                last_edit_gmtime.tm_mday,
                last_edit_gmtime.tm_hour,
                last_edit_gmtime.tm_min
            )

            time_diff = dtime - last_edit_dtime
            if time_diff.days >= days:
                _log_tmp["Projects"].pop(prj)
    if getHistory() != _log_tmp:
        writeJson(_log_tmp, HISTORY_FILE_PATH)


def getHistory():
    history = readJson(HISTORY_FILE_PATH)
    return history


def getImportedTime(project, filename):
    if not os.path.exists(HISTORY_FILE_PATH):
        return None
    _log = getHistory()
    if not _log["Projects"].has_key(project):
        return None
    if not _log["Projects"][project]["Imported_files"].has_key(filename):
        return None
    file_info = _log["Projects"][project]["Imported_files"][filename]
    imported_time = file_info["imported_time"]
    return imported_time


def writeHistory(project, filename, imported_time):
    if not os.path.exists(os.path.dirname(HISTORY_FILE_PATH)):
        os.makedirs(os.path.dirname(HISTORY_FILE_PATH))
    if os.path.exists(HISTORY_FILE_PATH):
        _log = getHistory()
    else:
        _log = LOG
    if not _log["Projects"].has_key(project):
        _log["Projects"] = {project: {"Imported_files": dict(), "Last_edited": float()}}

    if not _log["Projects"][project].has_key("Last_edited"):
        _log["Projects"][project]["Last_edited"] = float()

    if not _log["Projects"][project]["Imported_files"].has_key(filename):
        _log["Projects"][project]["Imported_files"][filename] = dict()

    _log["Projects"][project]["Imported_files"][filename]["imported_time"] = imported_time
    _log["Projects"][project]["Last_edited"] = imported_time
    writeJson(_log, HISTORY_FILE_PATH)
