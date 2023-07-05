import datetime

try:
    import webview
except ImportError:
    exit('install the pywebview package')

import py_ap_untis

def getTTable():
    s = py_ap_untis.get_session()
    day1 = datetime.date(2023, 9, 18)
    tt = s.timetable(start=day1, end=(day1 + datetime.timedelta(days=4)), teacher=3817)
    for e in tt:
        day = (e.start.date() - day1).days + 1
        e._data['day'] = day
    return [e._data for e in tt]


ui = webview.create_window('Untapped', url='./untapped.html')
ui.expose(getTTable)
webview.start(debug=True)