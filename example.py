#!/usr/bin/python3

import datetime
import sys

from py_ap_untis import *

get_session()

# No rights to fetch all teachers, only to query by name.
search_teacher('Willemen', 'Vaya (Vanessa)')
search_teacher('Wim', 'Livens')
search_teacher('Serge', 'Horsmans')
search_teacher('Peetermans', 'Wouter')
search_teacher('Patrick', 'De Meersman')

# Some subjects have multiple (unused) variations. Check len(tt) to see
# which one is actively used.
subjects = find_subjects('datacom & netwerken')

# see `help(_session.timetable)`
tt = get_session().timetable(start=datetime.date(2021, 9, 20),
                        end=datetime.date(2021, 12, 21),
                        subject=subjects[0])

write_timetable_csv(sys.stdout, tt)

with open('timetable.csv', 'w') as outfile:
    write_timetable_csv(outfile, tt)
