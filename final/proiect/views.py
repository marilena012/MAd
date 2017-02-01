import collections
import json
import subprocess
import datetime

from web_init import web_app
from local_db_stuff import DBStuff
from sqlalchemy import exc
from flask import request, render_template, flash, Flask, request, url_for, redirect, session
from wtforms import Form, BooleanField, RadioField, TextField, PasswordField, DateField, validators

from passlib.hash import sha256_crypt

import models as dbHandler

from sparql import Sparql
from content_management import Content

TOPIC_DICT = Content()

@web_app.route('/', methods=["POST", "GET"])
def index():
    logged_in = session.get('logged_in')
    if logged_in:
        return redirect(url_for('home'))
    return render_template("index.html")

@web_app.route('/home/', methods=['GET', 'POST'])
def home():
    logged_in = session.get('logged_in')
    if logged_in:
        info = {}
        diseaseInfo = ""
        diseaseName = ""
        diseaseTreatment = ""

        name = []
        symptoms = []
        treatment = []
        hasCauses = []
        causeOf = []
        image =""

        info["symptoms"] = symptoms
        info["treatment"] = treatment
        info["hasCauses"] = hasCauses
        info["causeOf"] = causeOf
        info["info"] = diseaseInfo
        info["name"] = name
        info["image"] = image

        diseaseInfo = False

        userList = []
        userListDb = dbHandler.getUserList(session.get("userid"))
        for l in userListDb:
            el = dbHandler.getElementByID(l[1])
            userList.append(el[0][1])

        b = True
        i = 0
        mostVisited = []
        visited = dbHandler.getElements("disease")
        while b == True:
            if i < 5 and len(visited) > i:
                mostVisited.append(visited[i][1])
                i = i + 1
            else:
                b = False

        suggestions = {}
        s = Sparql()
        suggestions = s.getSuggestions(session.get("userid"))

        if request.method == "GET":
            diseaseName = request.args.get("diseaseName")
            diseaseSymptoms = request.args.get("symptoms")
            diseaseTreatment = request.args.get("treatment")
            diseaseCauses = request.args.get("causes")
            diseaseType = request.args.get("type")
            diseaseCountry = request.args.get("country")
            diseaseClimate = request.args.get("climate")
            diseaseFood = request.args.get("food")
            first = True

            if(type(diseaseName) == str and len(diseaseName) != 0):
                s = Sparql()
                info = s.search_name(diseaseName)
                dbHandler.addElement(diseaseName, "disease")
                session["diseaseName"] = diseaseName
                diseaseInfo = True
                dbHandler.addVisitedDisease(session.get("userid"), diseaseName, "disease")

            if(type(diseaseSymptoms) == str and len(diseaseSymptoms) != 0):
                s = Sparql()
                if first == True:
                    info = s.search_symptoms(diseaseSymptoms)
                    first = False
                else:
                    infoTemp = s.search_symptoms(diseaseSymptoms)
                    info["name"] = list(set(info["name"]).intersection(infoTemp["name"]))
                symptoms = diseaseSymptoms.split(", ")
                for s in symptoms:
                    dbHandler.addElement(s, "symptom")

            if(type(diseaseTreatment) == str and len(diseaseTreatment) != 0):
                s = Sparql()
                
                if first == True:
                    info = s.search_treatment(diseaseTreatment)
                    first = False
                else:
                    infoTemp = s.search_treatment(diseaseTreatment)
                    info["name"] = list(set(info["name"]).intersection(infoTemp["name"]))

                treatments = diseaseTreatment.split(", ")
                for t in treatments:
                    dbHandler.addElement(t, "treatment")

            if(type(diseaseCauses) == str and len(diseaseCauses) != 0):
                s = Sparql()

                if first == True:
                    info = s.search_bycauses(diseaseCauses)
                    first = False
                else:
                    infoTemp = s.search_bycauses(diseaseCauses)
                    info["name"] = list(set(info["name"]).intersection(infoTemp["name"]))

                causes = diseaseCauses.split(", ")
                for c in causes:
                    dbHandler.addElement(c, "causes")

            if(type(diseaseType) == str and len(diseaseType) != 0):
                s = Sparql()
                if first == True:
                    info = s.search_bytype(diseaseType)
                    first = False
                else:
                    infoTemp = s.search_bytype(diseaseType)
                    info["name"] = list(set(info["name"]).intersection(infoTemp["name"]))
                types = diseaseType.split(", ")
                for t in types:
                    dbHandler.addElement(t, "types")

            if(type(diseaseCountry) == str and len(diseaseCountry) != 0):
                s = Sparql()
                if first == True:
                    info["name"] = s.search_diseaseByCountry(diseaseCountry)
                    first = False
                else:
                    infoTemp = s.search_diseaseByCountry(diseaseCountry)
                    info["name"] = list(set(info["name"]).intersection(infoTemp))

                dbHandler.addElement(diseaseCountry, "country")

            if(type(diseaseClimate) == str and len(diseaseClimate) != 0):
                s = Sparql()

                if first == True:
                    info["name"] = s.search_diseaseByClimate(diseaseClimate)
                    first = False
                else:
                    infoTemp = s.search_diseaseByClimate(diseaseClimate)
                    info["name"] = list(set(info["name"]).intersection(infoTemp))

                dbHandler.addElement(diseaseClimate, "climate")

            if(type(diseaseFood) == str and len(diseaseFood) != 0):
                s = Sparql()

                if first == True:
                    info["name"] = s.search_diseaseByFood(diseaseFood)
                    first = False
                else:
                    infoTemp = s.search_diseaseByFood(diseaseFood)
                    info["name"] = list(set(info["name"]).intersection(infoTemp))

                dbHandler.addElement(diseaseFood, "food")

            return render_template("home.html",
                                   username=session.get("username"),
                                   disease=info["name"],
                                   symptoms=info["symptoms"],
                                   treatment=info["treatment"],
                                   hasCauses=info["hasCauses"],
                                   causeOf=info["causeOf"],
                                   info=info["info"],
                                   image=info["image"],
                                   userList=userList,
                                   visited=mostVisited, 
                                   suggestions=suggestions,
                                   diseaseInfo=diseaseInfo)

        if request.method == "POST":
            dbHandler.addElementInList(session.get("userid"),
                                       session.get("diseaseName"), 
                                       "disease")
            userList.append(session.get("diseaseName"))
            return render_template("home.html",
                                   userList=userList,
                                   visited=mostVisited, 
                                   suggestions=suggestions)
    else:
        return redirect(url_for('index'))


@web_app.route('/dashboard/')
def dashboard():
    flash("flash test!!!!")
    flash("fladfasdfsaassh test!!!!")
    flash("asdfas asfsafs!!!!")
    return render_template("dashboard.html", TOPIC_DICT=TOPIC_DICT)


@web_app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@web_app.route('/login/', methods=['GET', 'POST'])
def login_page():
    if request.method == "POST":
        username = request.form['inputName']
        password = request.form['inputPassword']

        userId = dbHandler.getUserId(username)
        if len(userId) == 1:
            session['logged_in'] = True
            session['username'] = username
            session['userid'] = userId[0][0]
            return redirect(url_for('home'))

        else:
            flash("Invalid credentials. Please try again!")
            return render_template("login.html")
    if request.method == "GET":
        return render_template("login.html")


@web_app.route('/register/', methods=["GET", "POST"])
def register_page():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == 'POST':
        username = request.form['inputName']
        country = request.form['inputCountry']
        birthday = request.form['inputDateOfBirth']
        gender = request.form['genders']
        password = request.form['inputPassword']
        confirmPassword = request.form['inputConfirmPassword']
        if password == confirmPassword:
            userId = dbHandler.getUserId(username)
            if len(userId) == 1:
                flash("Username already exists")
                return render_template('register.html')
            else:
                dbHandler.insertUser(username, password, country, birthday, gender)
                userId = dbHandler.getUserId(username)
                session['logged_in'] = True
                session['username'] = username
                session['userid'] = userId[0][0]
                return redirect(url_for('home'))
        else:
            flash("Password must match")
            return render_template('register.html')


@web_app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index'))


@web_app.route('/result/')
def result():
    pass

@web_app.route('/quiz/', methods=['GET', "POST"])
def game():
    logged_in = session.get('logged_in')
    if logged_in:

        visited = dbHandler.getUserVisitedList(session.get("userid"))
        if len(visited) < 5:
            flash("You have to learn first!")
            return redirect(url_for('home'))

        question = {}
        question["question"] = "start"
        question["correctAnswer"] = ""
        question["answers"] = []

        scores = dbHandler.getUserScores(session.get("userid"))

        if request.method == "POST":
            answer = request.form['ans']
            if answer == session["currentQuestion"]["correctAnswer"]:
                session["correctAnswers"] = session["correctAnswers"] + 1
            session["numberOfQuestions"] = session["numberOfQuestions"] + 1
            if session["numberOfQuestions"] < 10:
                s = Sparql()
                question = s.generate_question(session.get("userid"))
                session["currentQuestion"] = question
                return render_template("quiz.html", username=session.get("username"), 
                                                question=question, scores = scores)
            else:
                flash("Your score is " + str(session["correctAnswers"]) + " correct answers out of 10!")
                dbHandler.addScore(session.get("userid"), session["correctAnswers"])
                s = Sparql()
                question = s.generate_question(session.get("userid"))
                session["currentQuestion"] = question
                session["numberOfQuestions"] = 0
                session["correctAnswers"] = 0
                return render_template("quiz.html", username=session.get("username"),
                                                question=question, scores = scores)

        if request.method == "GET":
            session["currentQuestion"] = question
            session["numberOfQuestions"] = 0
            session["correctAnswers"] = 0
            s = Sparql()
            question = s.generate_question(session.get("userid"))
            session["currentQuestion"] = question
            return render_template("quiz.html", username=session.get("username"),
                                                question=question, scores = scores)
    else:
        return render_template("index.html")


@web_app.route('/account/', methods=["GET", "POST"])
def settings():
    logged_in = session.get('logged_in')
    if logged_in:
        if request.method == 'POST':
            newSports = ""
            newSmoker = ""

            userID = session.get("userid")
            newUsername = request.form['inputUsername']
            newPassword = request.form['inputPassword']
            newconfirmPassword = request.form['inputConfirmPassword']
            newCountry = request.form['inputCountry']
            newBirthday = request.form['inputBirthday']
            newFood = request.form['favoriteFood']
            newGender = request.form['genders']
            try:
                newSports = request.form['lifestyle']
                newSmoker = request.form['smoker']
            except:
                pass

            if newPassword == newconfirmPassword:      
                dbHandler.editUser(userID, newUsername, newPassword, newCountry, newBirthday, newGender, newSports, newFood, newSmoker)
                userID = session.get("userid")
                user = dbHandler.getUserInfo(userID)
                return redirect(url_for('home'))
                #return render_template('account.html',username = user[0][1], password = user[0][2] , country = user[0][3], birthday=user[0][4], gender=user[0][5], 
                #   sports = user[0][6], food = user[0][7], smoker=user[0][8]) 
            else:
                flash("Invalid credentials. Please try again!")
                userID = session.get("userid")
                user = dbHandler.getUserInfo(userID)
                return render_template('account.html',username = user[0][1], password = user[0][2] , country = user[0][3], birthday=user[0][4], gender=user[0][5], 
                   sports = user[0][6], food = user[0][7], smoker=user[0][8]) 
            #newUsername = newUsername, newCountry = newCountry, newBirthday = newBirthday, newGender = newGender, newPassword = newPassword,
            #   newconfirmPassword = newconfirmPassword,newSports= newSports, newFood = newFood, newSmoker = newSmoker )
        if request.method == "GET":
            userID = session.get("userid")
            user = dbHandler.getUserInfo(userID)
            return render_template('account.html',username = user[0][1], password = user[0][2] , country = user[0][3], birthday=user[0][4], gender=user[0][5], 
                sports = user[0][6], food = user[0][7], smoker=user[0][8]) 
    else:
        render_template("index.html") 

