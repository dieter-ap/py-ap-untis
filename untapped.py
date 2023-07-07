import datetime
import json
import os
from pathlib import Path

try:
    import webview
except ImportError:
    exit('install the pywebview package')

import py_ap_untis

config = {}

def getConfig(key):
    global config
    if not config.get('configVersion'):
        loadConfig()
    return config.get(key)

def setConfig(key, value, save=True):
    global config
    changed = (getConfig(key) != value)
    config[key] = value
    if changed and save:
        saveConfig()

def _configPath(mkdir=False):
    configDir = os.path.join(Path.home(), '.untapped')
    configFile = os.path.join(configDir, 'config')
    if mkdir and not os.path.isdir(configDir):
        os.mkdir(configDir)
    return configFile

def loadConfig():
    global config
    configFile = _configPath()
    if os.path.isfile(configFile):
        with open(configFile, 'r') as inp:
            config.update(json.load(inp))
            config['configVersion'] = '1.0'

def saveConfig():
    global config
    configFile = _configPath(True)
    with open(configFile, 'w') as out:
        json.dump(config, out, indent=2)

untis_session = None

def untisLogin(username, passwd):
    global untis_session
    py_ap_untis._user = username
    py_ap_untis._password = passwd
    untis_session = py_ap_untis.get_session()
    if untis_session:
        untis_session.config['login_repeat'] = 1
        setConfig('untisUser', username)
    return bool(untis_session)

def _data4schoolyear(schoolyear):
    return {
        'id': schoolyear.id,
        'start': schoolyear.start.date().isoformat(),
        'end': schoolyear.end.date().isoformat(),
        'current': schoolyear.is_current,
        'name': schoolyear.name.replace('/', '-')
    }

def loadSchoolyears():
    global untis_session
    return {e.id: _data4schoolyear(e) for e in untis_session.schoolyears()}

def getTeacherTable(teacher, tbldate):
    '''
    Return the timetable for the given teacher (numeric id) and the tbldate
    which needs to be in isoformat.
    '''
    #s = py_ap_untis.get_session()
    global untis_session
    day1 = datetime.date.fromisoformat(tbldate)
    tt = untis_session.timetable(start=day1,
                                 end=(day1 + datetime.timedelta(days=4)),
                                 teacher=teacher)
    for e in tt:
        day = (e.start.date() - day1).days + 1
        e._data['day'] = day
    return [e._data for e in tt]


ui = webview.create_window('Untapped', url='./untapped.html')
ui.expose(getConfig, untisLogin, loadSchoolyears, getTeacherTable)
webview.start(debug=True)