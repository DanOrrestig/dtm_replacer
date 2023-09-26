import os
import sys
import PySimpleGUI as sg
from datetime import date, timedelta

sg.theme('DarkTeal11')   # Add a touch of color
# All the stuff inside your window.
t = sg.Multiline(size=(120,50))
t.DefaultText = ""

today = date.today()

fin = [] # array with texts to find
rep = [] # array with texts to replace with

def today_fix(input):
    if input.startswith('TODAY'):
        input = str(today + timedelta(days=int(input[5:])))
    if input.startswith('EMPTY'):
        input = ''
    return input.rstrip()

app_path = os.path.dirname(__file__) + '\\' # "/home/airflow/gcs/dags/gdpr/"
sys.path.insert(1, app_path)
#dags_path = app_path[:app_path.rfind("/")] #"/home/airflow/gcs/dags"
#script_path = '{}/sa-sponsor-selection/doc/truncate/truncate_sa_sponsor_selection.sql'.format(dags_path)
with open(app_path + 'settings.txt','r') as file:

    for line in file:
        if line == '\n' or line.startswith('#'):
            continue

        both = line.split('||')
        
        left = both[0].split('|')
        for i in range(len(left)):
            left[i] = today_fix(left[i])
        fin.append(sg.Combo(left,size=20,default_value=left[0]))

        right = both[1].split('|')
        for i in range(len(right)):
            right[i] = today_fix(right[i])
        rep.append(sg.Combo(right,size=20,default_value=right[0]))

layout = [
    [sg.Text('Find')], fin,
    [sg.Text('Replace with')], rep,
    [sg.Text('Text to fix')],
    [t],
    [sg.Button('Ok (and copy)',size=(38,40), font=("", 15)), sg.Button('Cancel',size=(38,40), font=("", 15))],
]

# Create the Window
window = sg.Window('dtm_replacer', layout, size=(900,1000), finalize=True)
t.set_cursor(cursor="arrow")
t.set_focus()

for i in range(len(fin)):
    fin[i].set_cursor(cursor="arrow")
    rep[i].set_cursor(cursor="arrow")

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break

    if len(t.Get()) > 0:
        s = t.Get()
    
        for i in range(len(fin)):
            if len(fin[i].Get()) > 0:
                print('find ', fin[i].Get(), ' replace with ', rep[i].Get())
                s = s.replace(fin[i].Get(),rep[i].Get(),-1)

        print('\n')
        t.update(s)
        
        sg.clipboard_set(s)

window.close()