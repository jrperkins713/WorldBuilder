from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from werkzeug.utils import secure_filename
from model import Person
from mysql.connector import connect, Error
import os
import json
import shutil

UPLOAD_FOLDER = 'static/media/'
ALLOWED_EXTENSIONS = set(['jpg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/<name>/")
def display_person(name):
    person = queryPerson(name)
    return render_template('template_person.html', pwd=os.getcwd(), person = person.__dict__)

@app.route("/")
def homepage():
    allPeople = queryAllPeople()
    print(allPeople)

    return render_template('template_homepage.html', personList = allPeople)

@app.route("/create-person/")
def servePersonForm():
    return render_template('form_create_person.html', person = False, createNew = True)

@app.route("/edit-person/<name>/", methods=['POST'])
def serveEditPersonForm(name):
    print("hit edit person")
    return render_template('form_create_person.html', person = queryPerson(name).__dict__, createNew = False)

@app.route("/handleDeletePerson/<name>/", methods=['POST'])
def handleDeletePerson(name):
    dropPerson(name)
    return redirect(url_for('homepage'))

@app.route("/handleCreatePerson/<createNew>", methods=['POST'])
def handleCreatePerson(createNew):
    print("createNew = " + createNew)
    newPerson = Person.Person()
    newPerson.copyDict(request.form)
    image = request.files.get('photo', '')
    if image.filename == '':
        print("no filename")
    if image:
        filename = secure_filename(newPerson.name + ".jpg")
        print("saving file: " + filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    storePerson(newPerson, createNew)
    return redirect(url_for('display_person', name = newPerson.name))

def makePerson(name):
    return Person.Person(name, "Topsfield", "Barkeep")

def storePerson(person, createNew):
    createNew = createNew == "True"
    try:
        f = open("creds.json")
        creds = json.load(f)
        with connect(
            host="localhost",
            user=creds["username"],
            password=creds["password"],
        ) as connection:
            query = "INSERT INTO my_schema.characters" + \
                        "(`name`, `location`, `occupation`,"+ \
                        "`str`, `dex`, `con`, `int`, `wis`, `chr`,"+ \
                        "`bio`, `race`, `alignment`, `sex`, `age`) "+ \
                    "VALUES ('"+\
                        person.name + "','" + \
                        person.city + "','" + \
                        person.occupation + "','" + \
                        person.stats['str'] + "','" + \
                        person.stats['dex'] + "','" + \
                        person.stats['con'] + "','" + \
                        person.stats['int'] + "','" + \
                        person.stats['wis'] + "','" + \
                        person.stats['chr'] + "','" + \
                        person.bio + "','" + \
                        person.race + "','" + \
                        person.alignment + "','" + \
                        person.sex + "','" + \
                        person.age + "');"
            print(createNew)
            print(type(createNew))
            if(not createNew):
                query = query.replace("INSERT", "REPLACE")
            with connection.cursor() as cursor:
                print(query)
                cursor.execute(query)
                connection.commit()
    except Error as e:
        print(e)
    return True

def queryAllPeople():
    
    try:
        f = open("creds.json")
        creds = json.load(f)
        with connect(
            host="localhost",
            user=creds["username"],
            password=creds["password"],
        ) as connection:
            query = 'SELECT * FROM my_schema.characters;'
            with connection.cursor() as cursor:
                cursor.execute(query)
                personList = []
                for j, db in enumerate(cursor):
                    person = Person.Person()
                    person.name = db[0]
                    person.city = db[1]
                    person.occupation = db[2]
                    for i, key in enumerate(person.stats):
                        person.stats[key] = db[i+3]
                    person.bio = db[9]
                    person.race = db[10]
                    person.alignment = db[11]
                    person.sex = db[12]
                    person.age = db[13]
                    personList.append(person)
    except Error as e:
        print(e)    
    return personList

def queryPerson(name):
    try:
        f = open("creds.json")
        creds = json.load(f)
        with connect(
            host="localhost",
            user=creds["username"],
            password=creds["password"],
        ) as connection:
            query = 'SELECT * FROM my_schema.characters WHERE name="'+ name+'";'
            with connection.cursor() as cursor:
                cursor.execute(query)
                for db in cursor:
                    person = Person.Person()
                    person.name = db[0]
                    person.city = db[1]
                    person.occupation = db[2]
                    for i, key in enumerate(person.stats):
                        person.stats[key] = db[i+3]
                    person.bio = db[9]
                    person.race = db[10]
                    person.alignment = db[11]
                    person.sex = db[12]
                    person.age = db[13]
    except Error as e:
        print(e)
    return person


def dropPerson(name):
    try:
        f = open("creds.json")
        creds = json.load(f)
        with connect(
            host="localhost",
            user=creds["username"],
            password=creds["password"],
        ) as connection:
            query = 'DELETE FROM `my_schema`.`characters` WHERE (`name` = "' + name + '");'
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
    except Error as e:
        print(e)