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

def get_subjects(reset=False):
    global _subjects
    if not reset and _subjects is not None:
        return _subjects
    _assert_session()
    _subjects = _session.subjects()
    return _subjects

def get_rooms(reset=False):
    global _rooms
    if not reset and _rooms is not None:
        return _rooms
    _assert_session()
    _rooms = _session.rooms()
    return _rooms

def get_schoolyears(reset=False):
    global _schoolyears
    if not reset and _schoolyears is not None:
        return _schoolyears
    _assert_session()
    _schoolyears = _session.schoolyears()
    return _schoolyears
