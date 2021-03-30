from flask import Flask, render_template, abort
import os
import csv

app = Flask(__name__)
app.secret_key = 'QWEWRTEGFVserwgeefr34t5hrgdvfscefsdvdfrgtfgdrfsedxvdfrgtfvddefdgf'

subjects = {'math': ['Algerbra_1', 'AP_Calc_BC'], 'history': ['AP_World_History', 'American/Arizona_History']}
q_fields = ['qid','question','work','answer']
default_response = [{'qid': '', 'question': 'No problems have been added for this class', 'work': '', 'answer': ''}]

'''for subject in subjects.values():
    for c in subject:
        if not os.path.isfile('classes/' + c.lower() + '.csv'):
            with open('classes/' + c.lower() + '.csv', 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(q_fields)'''

def get_probs(selected):
    if os.path.isfile('classes/' + selected.lower() + '.csv'):
        qs = []
        with open('classes/' + selected.lower() + '.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                qs.append(row)
        if len(qs) > 0:
            return qs
        else:
            return default_response
    else:
        return default_response

@app.route('/')
def home():
    return render_template('subjects.html', subjects=subjects.keys(), redir='subjects')

@app.route('/newquestion', methods=['GET', 'POST'])
def new_q():
    return render_template('newquestion.html', classes=set().union(*subjects.values()))

@app.route('/subjects/<subject>')
def subject(subject):
    if subject in subjects.keys():
        return render_template('subjects.html', subjects=subjects[subject], redir='classes')
    else:
        abort(404)

@app.route('/classes/<selected>')
def class_page(selected):
    if any(selected in val for val in subjects.values()):
        return render_template('class.html', class_name=selected, problems=get_probs(selected))
    else:
        abort(404)

if __name__ == '__main__':
    app.run(port=80, debug=True)
