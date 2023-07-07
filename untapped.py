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

def getConfig(key, missingVal=None):
    global config
    if not config.get('configVersion'):
        loadConfig()
    return config.get(key, missingVal)

def setConfig(key, value, save=True):
    '''
    Change the value of key. The new value is immediately written to the
    configuration file if save is True.
    '''
    global config
    # Only write config if value is changed, or if we cannot easily see it.
    changed = (not value.__hash__ or getConfig(key) != value)
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

def untisLogout():
    global untis_session
    if untis_session:
        untis_session.logout(suppress_errors=True)

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

def loadTeachers():
    return getConfig('teachers', {})

def findTeacher(firstName, lastName, remember=True):
    res = py_ap_untis.search_teacher(lastName, firstName, False)
    if res:
        ret = {'id': res.id, 'name': res.full_name}
        if remember:
            teachers = getConfig('teachers', {})
            teachers[res.id] = ret
            setConfig('teachers', teachers)
        return ret

def getTeacherTable(teacher, tbldate):
    '''
    Return the timetable for the given teacher (numeric id) and the tbldate
    which needs to be in isoformat.
    '''
    global untis_session
    day1 = datetime.date.fromisoformat(tbldate)
    day1 -= datetime.timedelta(days=day1.weekday())
    tt = untis_session.timetable(start=day1,
                                 end=(day1 + datetime.timedelta(days=4)),
                                 teacher=teacher)
    return [{
        'day': e.start.isoweekday(),
        'id': e.id,
        'groups': [{'id': k.id, 'name': k.name, 'long_name': k.long_name} for k in e.klassen],
        'rooms': [{'id': r.id, 'name': r.name, 'long_name': r.long_name} for r in e.rooms],
        'subjects': [{'id': s.id, 'name': s.name, 'long_name': s.long_name} for s in e.subjects],
        'teachers': e._data['te'],
        'time': e.start.hour
    } for e in tt]


ui = webview.create_window('Untapped', url='./untapped.html')
ui.expose(getConfig, untisLogin, untisLogout, loadSchoolyears,
          loadTeachers, findTeacher, getTeacherTable)
webview.start(debug=True)