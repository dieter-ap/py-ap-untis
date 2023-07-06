import datetime

try:
    import webview
except ImportError:
    exit('install the pywebview package')

import py_ap_untis

untis_session = None

def untisLogin(username, passwd):
    global untis_session
    py_ap_untis._user = username
    py_ap_untis._password = passwd
    untis_session = py_ap_untis.get_session()
    return bool(untis_session)

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
ui.expose(untisLogin, getTeacherTable)
webview.start(debug=True)