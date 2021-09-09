#!/usr/bin/python3

from getpass import getpass
import sys

try:
    import webuntis
except ModuleNotFoundError:
    sys.exit('You need to install the untis package (pip install webuntis)')

_server = 'arche.webuntis.com'
_school = 'ap-hogeschool-antwerpen'
_useragent = 'py-ap-untis'
_user = None
_password = None
_session = None

_departments = None
_subjects = None
_rooms = None
_schoolyears = None
_teachers = None

def get_session(reset=False):
    global _session
    
    for v in ('server', 'school', 'user', 'password'):
        val = globals()['_' + v]
        if reset or not val:
            if v == 'password':
                new_v = getpass(prompt='password: ')
            else:
                new_v = input('%s [%s]: ' % (v, val))
            if new_v:
                globals()['_' + v] = new_v
            elif not val:
                print('A value for %s is required' % v, file=sys.stderr)
                return

    _session = webuntis.Session(server=_server, school=_school,
                                useragent=_useragent,
                                username=_user, password=_password)
    try:
        _session.login()
    except webuntis.errors.BadCredentialsError as err:
        print(str(err), file=sys.stderr)
        print('To correct credentials, call get_session with reset=True')
        return
    return _session

def _assert_session():
    assert _session, 'You need to get_session first'

def get_departments(reset=False):
    global _departments
    if not reset and _departments is not None:
        return _departments
    _assert_session()
    _departments = {s.id: s for s in _session.departments()}
    return _departments

def get_department(name):
    global _departments
    if _departments is None:
        get_departments()
    return next(d for d in _departments.values() if d.name == name)

def get_subjects(reset=False):
    global _subjects
    if not reset and _subjects is not None:
        return _subjects
    _assert_session()
    _subjects = {s.id: s for s in _session.subjects()}
    return _subjects

def get_rooms(reset=False):
    global _rooms
    if not reset and _rooms is not None:
        return _rooms
    _assert_session()
    _rooms = {r.id: r for r in _session.rooms()}
    return _rooms

def get_schoolyears(reset=False):
    global _schoolyears
    if not reset and _schoolyears is not None:
        return _schoolyears
    _assert_session()
    _schoolyears = {s.id: s for s in _session.schoolyears()}
    return _schoolyears

def get_teachers(reset=False):
    global _teachers
    if not reset and _teachers is not None:
        return _teachers
    _assert_session()
    try:
        _teachers = _session.teachers()
    except webuntis.errors.RemoteError as err:
        _teachers = {}
        print(err, file=sys.stderr)
        print('You can cache teachers manually using search_teacher',
              file=sys.stderr)
    return _teachers

def search_teacher(surname, forename, try_reversed=True):
    global _teachers
    if _teachers is None:
        _teachers = {}
    _assert_session()
    try:
        t = _session.get_teacher(surname=surname, fore_name=forename)
    except KeyError:
        if try_reversed:
            try:
                t = search_teacher(surname=forename, forename=surname,
                                   try_reversed=False)
            except KeyError:
                t = None
    if t:
        _teachers[t.id] = t
        return t
