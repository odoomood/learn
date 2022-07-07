# -*- coding: utf-8 -*-
import erppeek

host = 'localhost'
port = 8569
db = 'o15-learn'
user = 'john_smith'
passw = '09546dcba10d222d917814416e324c49b4aa5a23'
# tech = 'xmlrpc'
tech = 'jsonrpc'
root = f'http://{host}:{port}/{tech}/'

o = erppeek.Client(root, db, user, passw)
print(f'Logged in as {user} (Server version: {o.server_version})')
sessions = o.OpenacademySession.browse(['id > 0'])
print('All sessions:')
for session in sessions:
    print(f'\t{session.name}, Course: {session.course_id.name}, Seats: {session.seats_taken} of {session.seats_total}')
if input('Do you wish to create new Session (y/n)? ').lower() == 'y':
    session_name = input('Enter name of the new Session: ')
    print('Available courses:')
    courses = o.OpenacademyCourse.browse(['id > 0'])
    for course in courses:
        print(f'\t{course.id}: {course.name}')
    course_id = int(input('Enter id of the available Course: '))
    o.OpenacademySession.create({
        'name': session_name,
        'course_id': o.OpenacademyCourse.get(course_id),
    })
    print('DONE!')
else:
    print('OK, goodby!')
