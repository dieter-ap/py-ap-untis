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

def getsession(reset=False):
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
        print('To correct credentials, call getsession with reset=True')
        return
    return _session
