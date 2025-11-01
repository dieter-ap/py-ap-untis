import json

import untapped

teachers_c = untapped.getConfig('teachers')

with open('teachers.json') as tfh:
    teachers_all = json.load(tfh)
teachers_all = teachers_all['teachers']

for t in teachers_c:
    print(f'Processing {t["name"]}', end='… ')
    select = [x for x in teachers_all if x['teacher']['longName'] == t['surname']]
    if len(select) == 0:
        print('Teacher not found')
    elif len(select) == 1:
        newdata = select[0]["teacher"]
        print(f'Found {newdata["displayName"]}')
    else:
        print('multiple options',
              ", ".join([x["teacher"]["displayName"] for x in select]))
        select = [x for x in select if t['forename'] in x['teacher']['displayName']]
        if len(select) == 0:
            print('\tTeacher not found')
        elif len(select) == 1:
            newdata = select[0]['teacher']
            print(f'\tFound {newdata["displayName"]}')
        else:
            print('\tstill multiple options',
                  ", ".join([x["teacher"]["displayName"] for x in select]))
    if newdata and t['id'] != newdata['id']:
        print(f'\tTeacher id changed: {t["id"]} → {newdata["id"]}')
        t["id"] = newdata["id"]

untapped.setConfig('teachers', teachers_c)