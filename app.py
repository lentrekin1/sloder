from flask import Flask, render_template, abort, redirect, request, flash
from flask_wtf.csrf import CSRFProtect
import os
import csv
import random
import string
import re

app = Flask(__name__)
CSRFProtect(app)
app.config['SECRET_KEY'] = 'QWEWRTEGFVserwgeefr34t5hrgdvfscefsdvdfrgtfgdrfsedxvdfrgtfvddefdgf'

subjects = {'math': ['AP_Calc_AB', 'AP_Calc_BC', 'AP_Computer_Science_A', 'AP_Statistics', 'Algebra_I', 'Algebra_II', 'Honors_Algebra_II', 'Algebra_III_with_Trigonometry', 'Honors_Calculus_III', 'College_Mathematics', 'Financial_Math-Personal_&_Family', 'Foundations_of_Math', 'Geometry', 'Honors_Geometry_&_Trigonometry', 'Integrated_Algebra_II', 'Integrated_Math', 'Trigonometry_&_Pre-Calculus', 'Honors_Trigonometry_&_Pre-Calculus']}
q_fields = ['qid','question','work','answer']
class_dir = 'classes/'
nl_char = ' ⷣ'
default_response = [{'qid': '', 'question': 'No problems have been added for this class', 'work': '', 'answer': ''}]

'''for subject in subjects.values():
    for c in subject:
        if not os.path.isfile('classes/' + c.lower() + '.csv'):
            with open('classes/' + c.lower() + '.csv', 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(q_fields)'''

if not os.path.isdir(class_dir):
    os.mkdir(class_dir)

def get_probs(selected):
    if os.path.isfile(class_dir + selected.lower() + '.csv'):
        qs = []
        with open(class_dir + selected.lower() + '.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                print(row)
                #for r in row:
                #    row[r] = row[r].decode()
                row['work'] = row['work']#.replace(nl_char, '\n')
                qs.append(row)
        if len(qs) > 0:
            return qs
        else:
            return default_response
    else:
        return default_response

def get_classes():
    return set().union(*subjects.values())

def parse_ans(ans):
    return ''.join([str(int(c) + random.randint(1, 2)) if str.isdigit(c) else c for c in ans])

@app.route('/')
def home():
    #return render_template('subjects.html', subjects=subjects.keys(), redir='subjects')
    return redirect('/subjects/math')

@app.route('/newquestion', methods=['GET', 'POST'])
def new_q():
    if request.method == 'POST':
        form = request.form.to_dict()
        del form['csrf_token']
        for field in form:
            if form[field] == '':
                flash(f'Please enter a {field} for your question')
                return render_template('newquestion.html', classes=get_classes())
            if field == 'class':
                if not form[field] in get_classes():
                    flash('Please enter a valid class name')
                    return render_template('newquestion.html', classes=get_classes())
            if field == 'work':
                form[field] = form[field]#.replace('\n', nl_char)
            if field == 'answer':
                form[field] = parse_ans(form[field])
        if not os.path.isfile(class_dir + form['class'] + '.csv'):
            with open(class_dir + form['class'] + '.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(q_fields)
        form['qid'] = ''.join(random.choices(string.ascii_letters, k=7))
        with open(class_dir + form['class'] + '.csv', 'a', newline='', encoding='utf-8') as f:
            del form['class']
            writer = csv.DictWriter(f, q_fields)
            writer.writerow(form)
        flash('Question submitted successfully')
        return redirect('/newquestion')
    return render_template('newquestion.html', classes=get_classes())


@app.route('/subjects/<subject>')
def subject(subject):
    if subject.lower() in subjects.keys():
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
