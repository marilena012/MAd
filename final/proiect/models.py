import socket
import sqlite3 as sql

import datetime


def createTable():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute('''DROP TABLE users''')
    cur.execute('''CREATE TABLE users (id integer PRIMARY KEY AUTOINCREMENT,
                                       username text,
                                       password text,
                                       country text,
                                       birthday date,
                                       gender text,
                                       sports boolean,
                                       food text,
                                       smoker boolean)''')
    cur.execute('''DROP TABLE listElement''')
    cur.execute('''CREATE TABLE listElement (id integer PRIMARY KEY AUTOINCREMENT,
                                             name text,
                                             elType text,
                                             count integer)''')
    cur.execute('''DROP TABLE list''')
    cur.execute('''CREATE TABLE list (userID integer,
                                      elementID integer)''')

    cur.execute('''DROP TABLE visited''')
    cur.execute('''CREATE TABLE visited (userID integer,
                                         elementID integer)''')

    cur.execute('''DROP TABLE scores''')
    cur.execute('''CREATE TABLE scores (userID integer,
                                         score integer,
                                         playDate date)''')


def insertUser(username, password, country, birthday, gender):
    con = sql.connect("database.db")
    cur = con.cursor()

    users = retrieveUsers()
    if len(users) == 0:
        cur.execute("INSERT INTO users (id, username, password, country, birthday, gender) VALUES (?,?,?,?,?,?)",
                    (1, username, password, country, birthday, gender))
    else:
        cur.execute("INSERT INTO users (username, password, country, birthday, gender) VALUES (?,?,?,?,?)",
                    (username, password, country, birthday, gender))
    con.commit()
    con.close()

def editUser(userID, username, password, country, birthday, gender, sports, food, smoker):
    con = sql.connect("database.db")
    cur = con.cursor()
    if username != '':
        cur.execute("UPDATE users SET username = ? WHERE id = ?",
                     (username, userID))
    if password != '':
        cur.execute("UPDATE users SET password = ? WHERE id = ?",
                     (password, userID))
    if country != '':
        cur.execute("UPDATE users SET country = ? WHERE id = ?",
                     (country, userID))
    if birthday != '':
        cur.execute("UPDATE users SET birthday = ? WHERE id = ?",
                     (birthday, userID))
    if gender != '':
        cur.execute("UPDATE users SET gender = ? WHERE id = ?",
                     (gender, userID))
    cur.execute("UPDATE users SET sports = ? WHERE id = ?",
                     (sports, userID))
    if food != '':
        cur.execute("UPDATE users SET food = ? WHERE id = ?",
                     (food, userID))
    
    cur.execute("UPDATE users SET smoker = ? WHERE id = ?",
                     (smoker, userID))
    con.commit()
    con.close()

def retrieveUsers():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    con.close()
    return users

def getNamePass():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT username, password FROM users")
    usern = cur.fetchall()
    con.close()
    return usern

def getUserInfo(userid):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (userid, ))
    info = cur.fetchall()
    con.close()
    return info

def getUserId(name):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", (name,))
    users = cur.fetchall()
    con.close()
    return users

def getElement(name, elType):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT id, name, elType, count FROM listElement WHERE name = ?", (name,))
    elements = cur.fetchall()
    con.close()
    return elements

def getElementByID(elID):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM listElement WHERE id = ?", (elID,))
    elements = cur.fetchall()
    con.close()
    return elements

def addElement(name, elType):
    elements = getElement(name, elType)

    con = sql.connect("database.db")
    cur = con.cursor()

    count = 1
    if len(elements) > 0:
        count = elements[0][3] + 1
        cur.execute("UPDATE listElement SET count = ? WHERE name = ?",
                    (count, name))
    else:
        elements = getAllElements()
        if len(elements) == 0:
            cur.execute("INSERT INTO listElement (id, name, elType, count) VALUES (?,?,?,?)",
                        (1, name, elType, count))
        else:
            cur.execute("INSERT INTO listElement (name, elType, count) VALUES (?,?,?)",
                        (name, elType, count))
    con.commit()
    con.close()

def getAllElements():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM listElement ORDER BY count DESC")
    elements = cur.fetchall()
    con.close()
    return elements

def getElements(elType):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM listElement WHERE elType = ?",(elType,))
    elements = cur.fetchall()
    con.close()
    return elements

def addElementInList(userID, name, elType):
    con = sql.connect("database.db")
    cur = con.cursor()
    
    if len(getElement(name, elType)) == 0:
        addElement(name, elType)
    
    elementID = getElement(name, elType)[0][0]

    cur.execute("SELECT * FROM list WHERE userID = ? AND elementID = ?",(userID, elementID,))
    elements = cur.fetchall()
    if len(elements) == 0:
        cur.execute("INSERT INTO list (userID, elementID) VALUES (?,?)",
                    (userID, elementID))
    con.commit()
    con.close()

def addVisitedDisease(userID, name, elType):
    con = sql.connect("database.db")
    cur = con.cursor()
    
    if len(getElement(name, elType)) == 0:
        addElement(name, elType)
    
    elementID = getElement(name, elType)[0][0]

    cur.execute("SELECT * FROM visited WHERE userID = ? AND elementID = ?",(userID, elementID,))
    elements = cur.fetchall()
    if len(elements) == 0:
        cur.execute("INSERT INTO visited (userID, elementID) VALUES (?,?)",
                    (userID, elementID))
    con.commit()
    con.close()

def getUserList(userID):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM list WHERE userID = ?",(userID,))
    elements = cur.fetchall()
    con.close()
    return elements

def getUserVisitedList(userID):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM visited WHERE userID = ?",(userID,))
    elements = cur.fetchall()
    con.close()
    return elements

def deleteElement(name, elType):
    elID = getElement(name, elType)[0][0]
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM visited WHERE elementID = ?",(elID,))
    cur.execute("DELETE FROM list WHERE elementID = ?",(elID,))
    cur.execute("DELETE FROM listElement WHERE id = ?",(elID,))
    con.commit()
    con.close()

def addScore(userID, score):
    con = sql.connect("database.db")
    cur = con.cursor()
    
    today = datetime.date.today()
    cur.execute("INSERT INTO scores (userID, score, playDate) VALUES (?,?,?)",
                    (userID, score, today))
    con.commit()
    con.close()

def getUserScores(userID):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM scores WHERE userID = ?",(userID,))
    scores = cur.fetchall()
    con.close()
    return scores

def deleteScore(userID, score):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM scores WHERE score = ? and userID = ?",(score, userID))
    con.commit()
    con.close()

#createTable()
"""
insertUser("marilena", "1234", "c", "d", "g")
insertUser("silvia", "1234", "SUA", "", "female")

addElement("influenza", "disease")
addElement("flu", "disease")
addElement("meningitis", "disease")
addElement("croup", "disease")
addElement("lung cancer", "disease")
"""
"""
addElementInList(1, "influenza", "disease")
addElementInList(1, "flu", "disease")
addElementInList(1, "meningitis", "disease")
addElementInList(1, "croup", "disease")
addElementInList(1, "lung cancer", "disease")
"""

#print(getUserId("marilena"))

#editUser(1, "", "", "SUA", "1993-10-21", "", False, "fast food", True)
#editUser(2, "", "", "", "", "female", False, "fast food", False)
print(getElements("disease"))

#deleteScore(1, 10)

#deleteElement("nut allergy", "disease")

#print(getUserList(1))
print(getUserVisitedList(1))
#print(getUserInfo(1))

"""(id integer PRIMARY KEY AUTOINCREMENT,
   username text,
   password text,
   country text,
   birthday date,
   gender text,
   sports boolean,
   food text,
   smoker boolean)''')"""