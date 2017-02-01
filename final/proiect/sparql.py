from SPARQLWrapper import SPARQLWrapper, JSON
import requests
from random import randint
import random
import re 

import models as dbHandler
import rdflib
import rdfextras


class Sparql:
    def __init__(self):
        pass

    def search_name(self, name):
        print(name)
        print("search_name")
        info = {}
        symptoms = []
        treatment = []
        hasCauses = []
        causeOf = []
        diseases = []
        image = ""

        # getting symptoms
        hpCharURL = '''https://query.wikidata.org/sparql?query=
                      SELECT ?Slabel
        WHERE{
            ?disease wdt:P31 wd:Q12136.
            ?disease rdfs:label "''' + name + '''"@en .
            ?disease wdt:P780 ?symptoms .
            ?symptoms rdfs:label ?Slabel
            FILTER (langMatches( lang(?Slabel), "en" ) )  .
        }
        &format = JSON'''

        headers = {"Accept": "application/json"}
        r2 = requests.get(hpCharURL, headers=headers)
        r = r2.json()

        for d in r["results"]["bindings"]:
            if d['Slabel']['value'] not in symptoms:
                symptoms.append(d['Slabel']['value'])
        info["symptoms"] = symptoms

        # getting treatment
        hpCharURL = '''https://query.wikidata.org/sparql?query=
                      SELECT ?Tlabel
        WHERE{
            ?disease wdt:P31 wd:Q12136.
            ?disease rdfs:label "''' + name + '''"@en .
            ?disease wdt:P2176 ?treatment .
            ?treatment rdfs:label ?Tlabel
            FILTER (langMatches( lang(?Tlabel), "en" ) )  .
        }
        &format = JSON'''

        headers = {"Accept": "application/json"}
        r2 = requests.get(hpCharURL, headers=headers)
        r = r2.json()

        for d in r["results"]["bindings"]:
            if d['Tlabel']['value'] not in treatment:
                treatment.append(d['Tlabel']['value'])
        info["treatment"] = treatment

        # getting causes
        hpCharURL = '''https://query.wikidata.org/sparql?query=
                      SELECT ?Clabel
        WHERE{
            ?disease wdt:P31 wd:Q12136.
            ?disease rdfs:label "''' + name + '''"@en .
            ?disease wdt:P828 ?cause .
            ?cause rdfs:label ?Clabel
            FILTER (langMatches( lang(?Clabel), "en" ) )  .
        }
        &format = JSON'''

        headers = {"Accept": "application/json"}
        r2 = requests.get(hpCharURL, headers=headers)
        r = r2.json()

        for d in r["results"]["bindings"]:
            if d['Clabel']['value'] not in hasCauses:
                hasCauses.append(d['Clabel']['value'])
        info["hasCauses"] = hasCauses

        # getting causes
        hpCharURL = '''https://query.wikidata.org/sparql?query=
                      SELECT ?Clabel
        WHERE{
            ?disease wdt:P31 wd:Q12136.
            ?disease rdfs:label "''' + name + '''"@en .
            ?disease wdt:P1542 ?cause .
            ?cause rdfs:label ?Clabel
            FILTER (langMatches( lang(?Clabel), "en" ) )  .
        }
        &format = JSON'''

        headers = {"Accept": "application/json"}
        r2 = requests.get(hpCharURL, headers=headers)
        r = r2.json()

        for d in r["results"]["bindings"]:
            if d['Clabel']['value'] not in causeOf:
                causeOf.append(d['Clabel']['value'])
        info["causeOf"] = causeOf

        # getting image
        hpCharURL = '''https://query.wikidata.org/sparql?query=
                      SELECT ?disease ?image
                  WHERE {
                  ?disease wdt:P31 wd:Q12136.
                  ?disease rdfs:label "''' + name + '''"@en.
                  ?disease wdt:P18 ?image .
                }
        &format = JSON'''

        headers = {"Accept": "application/json"}
        r2 = requests.get(hpCharURL, headers=headers)
        r = r2.json()

        for d in r["results"]["bindings"]:
            if d['image']['value'] not in causeOf:
                image = d['image']['value']
        info["image"] = image

        # getting info
        hpCharURL = '''https://dbpedia.org/sparql?query=
          select distinct ?disease ?about
                where {
                    ?disease rdf:type <http://dbpedia.org/ontology/Disease>.
                    ?disease dbo:abstract ?about .
                    ?disease rdfs:label ?Ilabel .
                    FILTER (langMatches(lang(?about),"en")).
                    FILTER (lcase(str(?Ilabel)) = "''' + name.lower() + '''")
                }
        &format = JSON'''

        headers = {"Accept": "application/json"}
        r2 = requests.get(hpCharURL, headers=headers)
        r = r2.json()

        if len(r["results"]["bindings"]) > 0:
            info["info"] = r["results"]["bindings"][0]["about"]["value"]
        else:
            info['info'] = ""

        diseases.append(name)
        info["name"] = diseases

        return info

    def search_symptoms(self, symptomslist):
        print("search_symptoms")
        info = {}
        symptoms = []
        treatment = []
        hasCauses = []
        causeOf = []
        diseases = []
        image = ""

        symptoms = symptomslist.split(", ")

        firstS = True
        for s in symptoms:
            # getting diseases
            hpCharURL = '''https://query.wikidata.org/sparql?query=
              SELECT ?Dlabel
                WHERE {
                  ?disease wdt:P31 wd:Q12136.
                  ?disease rdfs:label ?Dlabel.
                  ?disease wdt:P780 ?symptoms.
                  ?symptoms rdfs:label ?Slabel.
                  FILTER(LANGMATCHES(LANG(?Dlabel), "en"))
                  FILTER(lcase(str(?Slabel)) = "''' + s.lower() + '''")
                }
            &format = JSON'''

            headers = {"Accept": "application/json"}
            r2 = requests.get(hpCharURL, headers=headers)
            r = r2.json()


            if firstS == True:
                for d in r["results"]["bindings"]:
                    if d['Dlabel']['value'] not in diseases:
                        diseases.append(d['Dlabel']['value'])
                firstS = False

            else:
                secondDiseases = []
                for d in r["results"]["bindings"]:
                    if d['Dlabel']['value'] not in secondDiseases:
                        secondDiseases.append(d['Dlabel']['value'])
                diseases = list(set(diseases).intersection(secondDiseases))
            
        info["symptoms"] = symptoms
        info["treatment"] = treatment
        info["hasCauses"] = hasCauses
        info["causeOf"] = causeOf
        info["info"] = ""
        info["name"] = diseases
        info["image"] = image

        return info

    def search_treatment(self, treatmentList):
        print("search_treatment")
        info = {}
        symptoms = []
        treatment = []
        hasCauses = []
        causeOf = []
        diseases = []
        image = ""

        treatment = treatmentList.split(" ")

        for t in treatment:
            # getting diseases
            hpCharURL = '''https://query.wikidata.org/sparql?query=
              SELECT ?Dlabel
                WHERE {
                  ?disease wdt:P31 wd:Q12136.
                  ?disease rdfs:label ?Dlabel.
                  ?disease wdt:P2176 ?treatment.
                  ?treatment rdfs:label ?Tlabel.
                  FILTER(LANGMATCHES(LANG(?Dlabel), "en"))
                }
            &format = JSON'''

            headers = {"Accept": "application/json"}
            r2 = requests.get(hpCharURL, headers=headers)
            r = r2.json()

            for d in r["results"]["bindings"]:
                if d['Dlabel']['value'] not in diseases:
                    diseases.append(d['Dlabel']['value'])

        info["symptoms"] = symptoms
        info["treatment"] = treatment
        info["hasCauses"] = hasCauses
        info["causeOf"] = causeOf
        info["info"] = ""
        info["name"] = diseases
        info["image"] = image

        return info

    def search_bycauses(Self, causesList):
        print("search_bycauses")
        info = {}
        symptoms = []
        treatment = []
        hasCauses = []
        causeOf = []
        diseases = []
        image = ""

        hasCauses = causesList.split(", ")

        firstS = True
        for c in hasCauses:
            # getting diseases
            hpCharURL = '''https://query.wikidata.org/sparql?query=
              SELECT ?Dlabel
                WHERE {
                  ?disease wdt:P31 wd:Q12136 .
                  ?disease rdfs:label ?Dlabel.
                  ?disease wdt:P828 ?cause .
                  ?cause rdfs:label ?Clabel .
                  FILTER(LANGMATCHES(LANG(?Dlabel), "en"))
                  FILTER(lcase(str(?Clabel)) = "''' + c.lower() + '''")
                }
            &format = JSON'''

            headers = {"Accept": "application/json"}
            r2 = requests.get(hpCharURL, headers=headers)
            r = r2.json()

            if firstS == True:
                for d in r["results"]["bindings"]:
                    if d['Dlabel']['value'] not in diseases:
                        diseases.append(d['Dlabel']['value'])
                firstS = False

            else:
                secondDiseases = []
                for d in r["results"]["bindings"]:
                    if d['Dlabel']['value'] not in secondDiseases:
                        secondDiseases.append(d['Dlabel']['value'])
                diseases = list(set(diseases).intersection(secondDiseases))

        info["symptoms"] = symptoms
        info["treatment"] = treatment
        info["hasCauses"] = hasCauses
        info["causeOf"] = causeOf
        info["info"] = ""
        info["name"] = diseases
        info["image"] = image

        return info

    def search_bytype(self, typesList):
        print("search_bytype")
        info = {}
        symptoms = []
        treatment = []
        hasCauses = []
        causeOf = []
        diseases = []
        image = ""

        types = typesList.split(", ")

        firstS = True
        for t in types:
            # getting diseases
            hpCharURL = '''https://query.wikidata.org/sparql?query=
              SELECT ?Dlabel
                WHERE {
                  ?disease wdt:P31 wd:Q12136.
                  ?disease rdfs:label ?Dlabel.
                  ?disease wdt:P279 ?type.
                  ?type rdfs:label ?Tlabel.
                  FILTER(LANGMATCHES(LANG(?Dlabel), "en"))
                  FILTER(lcase(str(?Tlabel)) = "''' + t.lower() + '''")
                }
            &format = JSON'''

            headers = {"Accept": "application/json"}
            r2 = requests.get(hpCharURL, headers=headers)
            r = r2.json()


            if firstS == True:
                for d in r["results"]["bindings"]:
                    if d['Dlabel']['value'] not in diseases:
                        diseases.append(d['Dlabel']['value'])
                firstS = False

            else:
                secondDiseases = []
                for d in r["results"]["bindings"]:
                    if d['Dlabel']['value'] not in secondDiseases:
                        secondDiseases.append(d['Dlabel']['value'])
                diseases = list(set(diseases).intersection(secondDiseases))
            
        info["symptoms"] = symptoms
        info["treatment"] = treatment
        info["hasCauses"] = hasCauses
        info["causeOf"] = causeOf
        info["info"] = ""
        info["name"] = diseases
        info["image"] = image

        return info

    def search_diseaseClass(self, diseaseName):
        print("search_diseaseClass")
        hpCharURL = '''https://query.wikidata.org/sparql?query=
                      SELECT ?class ?Dlabel ?Clabel
                WHERE {
                  ?disease wdt:P31 wd:Q12136 .
                  ?disease rdfs:label "''' + diseaseName + '''"@en.
                  ?disease wdt:P279 ?class.
                  ?class rdfs:label ?Clabel.
                  FILTER(LANGMATCHES(LANG(?Clabel), "en"))
                }
        &format = JSON'''

        headers = {"Accept": "application/json"}
        r2 = requests.get(hpCharURL, headers=headers)
        r = r2.json()

        classes = []
        for d in r["results"]["bindings"]:
            classes.append(d['Clabel']['value'])
        return classes

    def search_diseasesByClass(self, diseaseName):
        print(diseaseName)
        print("search_diseasesByClass")
        classes = self.search_diseaseClass(diseaseName)
        diseases = []
        for cl in classes:
            hpCharURL = '''https://query.wikidata.org/sparql?query=
                          SELECT ?class ?Dlabel ?disease
                    WHERE {
                      ?disease wdt:P31 wd:Q12136 .
                      ?disease rdfs:label ?Dlabel .
                      ?disease wdt:P279 ?class .
                      ?class rdfs:label "''' + cl + '''"@en.
                      FILTER(LANGMATCHES(LANG(?Dlabel), "en")) .
                    }
            &format = JSON'''

            headers = {"Accept": "application/json"}
            r2 = requests.get(hpCharURL, headers=headers)
            r = r2.json()

            i = 0
            b = True
            while b == True:
                if(i < len(r["results"]["bindings"]) and
                    r["results"]["bindings"][i]["Dlabel"]["value"] != diseaseName):
                    diseases.append(r["results"]["bindings"][i]["Dlabel"]["value"])
                    b = False
                i = i + 1

        return diseases

    def getSuggestions(self, userid):
        print("getSuggestions")
        userList = dbHandler.getUserList(userid)
        suggestionList = {}
        elList = []
        for el in userList:
            elList.append(dbHandler.getElementByID(el[1])[0])

        diseasesClass = []
        for el in elList:
            diseasesClass.extend(self.search_diseasesByClass(el[1]))

        userInfo = dbHandler.getUserInfo(userid)[0]
        country = userInfo[3]

        diseasesCountry = []

        if country:
            diseasesCountry = self.search_diseaseByCountry(country)

        suggestionList["class"] = diseasesClass
        suggestionList["country"] = diseasesCountry
        suggestionList["risks"] = self.search_predispositions(userInfo[6], userInfo[8], userInfo[5], userInfo[7])

        return suggestionList


    def search_diseaseByActivityAndFood(self, activity, food):
        print("search_diseaseByActivityAndFood")
        filename = "country.rdf"
        rdfextras.registerplugins()

        diseases = []
        diseaseNames = []

        g = rdflib.Graph()
        try:
            g.parse(filename)
        except:
            filename = "proiect\country.rdf"
            g.parse(filename)

        results = g.query('''
            PREFIX schemaorg:<http://schema.org/>
            PREFIX wikidata:<https://www.wikidata.org/wiki/>

            SELECT ?n  WHERE {?s wikidata:Q2095 "''' + food + '''"@en.
                              ?s schemaorg:Action "''' + activity + '''"@en .
                              ?s schemaorg:Thing ?n}''')

        for row in results:
            diseases.append(row.__getattr__("n").__reduce__()[1][0])

        return diseases


    def search_diseasebyRisk(self, name):
        print("search_diseasebyRisk")
        filename = "country.rdf"
        rdfextras.registerplugins()

        diseases = []
        diseaseNames = []

        g = rdflib.Graph()
        try:
            g.parse(filename)
        except:
            filename = "proiect\country.rdf"
            g.parse(filename)

        results = g.query('''
            PREFIX wikidataQ:<https://www.wikidata.org/wiki/>
            PREFIX property:<http://meta.schema.org/Property>
            PREFIX person:<http://schema.org/Person>
            PREFIX riskfactor:<https://health-lifesci.schema.org/MedicalRiskFactor>

            SELECT ?diseaseName WHERE {?disease property:category ?diseaseCat ;
                                                property:name ?diseaseName ;
                                                riskfactor:name ?risk .
                                       FILTER(str(?risk) = "''' + name + '''") .
                                       FILTER(str(?diseaseCat) = "disease") .
                                }''')
        for row in results:
            diseases.append(row.__getattr__("diseaseName").__reduce__()[1][0])

        return diseases

    def search_diseasebyGender(self, name):
        print("search_diseasebyGender")
        filename = "country.rdf"
        rdfextras.registerplugins()

        diseases = []
        diseaseNames = []

        g = rdflib.Graph()
        try:
            g.parse(filename)
        except:
            filename = "proiect\country.rdf"
            g.parse(filename)

        results = g.query('''
            PREFIX wikidataQ:<https://www.wikidata.org/wiki/>
            PREFIX property:<http://meta.schema.org/Property>
            PREFIX person:<http://schema.org/Person>
            PREFIX riskfactor:<https://health-lifesci.schema.org/MedicalRiskFactor>

            SELECT ?diseaseName WHERE {?disease property:category ?diseaseCat ;
                                                property:name ?diseaseName ;
                                                person:gender ?gender .
                                       FILTER(str(?gender) = "''' + name + '''") .
                                       FILTER(str(?diseaseCat) = "disease") .
                                }''')
        for row in results:
            diseases.append(row.__getattr__("diseaseName").__reduce__()[1][0])

        return diseases

    def search_predispositions(self, sedentarism, smoking, gender, food):
        print("search_predispositions")

        possibleDiseases = {}
        if gender:
            possibleDiseases["gender"] = self.search_diseasebyGender(gender)
        if food:
            possibleDiseases["food"] = self.search_diseaseByFood(food)
        if sedentarism == False:
            possibleDiseases["sedentarism"] = self.search_diseasebyRisk("sedentarism")
        if smoking == True:
            possibleDiseases["smoking"] = self.search_diseasebyRisk("smoking")

        diseases = {}
        for p in possibleDiseases:
            for d in possibleDiseases[p]:
                if d in diseases:
                    diseases[d]["n"] = diseases[d]["n"] + 1
                    diseases[d]["factors"].append(p)
                else:
                    diseases[d] = {}
                    diseases[d]['n'] = 1
                    diseases[d]["factors"] = []
                    diseases[d]["factors"].append(p)

        riskyDiseases = {}
        for d in diseases:
            if diseases[d]["n"] > 1:
                riskyDiseases[d] = {}
                riskyDiseases[d]["cause"] = ""
                for c in self.search_diseasebyRisk(d):
                    riskyDiseases[d]["cause"] = riskyDiseases[d]["cause"] + ", " + c
                riskyDiseases[d]["cause"] = riskyDiseases[d]["cause"][2:]
                riskyDiseases[d]["factors"] = ""
                riskyDiseases[d]["rec"] = ""
                for f in diseases[d]["factors"]:
                    if f == "smoking":
                        riskyDiseases[d]["factors"] = riskyDiseases[d]["factors"] + ", you smoke"
                        riskyDiseases[d]["rec"] = riskyDiseases[d]["rec"] + ", you should quit smoking"
                    if f == "sedentarism":
                        riskyDiseases[d]["factors"] = riskyDiseases[d]["factors"] + ", you don't practice any sport"
                        riskyDiseases[d]["rec"] = riskyDiseases[d]["rec"] + ", you should be more active"
                    if f == "food":
                        riskyDiseases[d]["factors"] = riskyDiseases[d]["factors"] + ", you eat " + food
                        riskyDiseases[d]["rec"] = riskyDiseases[d]["rec"] + ", you should eat more healthy"
                riskyDiseases[d]["factors"] = riskyDiseases[d]["factors"][2:]
                riskyDiseases[d]["rec"] = riskyDiseases[d]["rec"][2:]

        return riskyDiseases



    def search_diseaseByCountry(self, name):
        print("search_diseaseByCountry")
        filename = "country.rdf"
        rdfextras.registerplugins()

        diseases = []
        diseaseNames = []

        g = rdflib.Graph()
        try:
            g.parse(filename)
        except:
            filename = "proiect\country.rdf"
            g.parse(filename)

        results = g.query('''
            PREFIX wikidataQ:<https://www.wikidata.org/wiki/>
            PREFIX property:<http://meta.schema.org/Property>
            PREFIX person:<http://schema.org/Person>

            SELECT ?diseaseName WHERE {?country property:name ?countryName ;
                                                person:nationality ?nationality ;
                                                property:category ?countryCat .
                                       ?disease property:category ?diseaseCat ;
                                                property:name ?diseaseName ;
                                                person:nationality ?nationality .
                                       FILTER(str(?countryName) = "''' + name + '''") .
                                       FILTER(str(?countryCat) = "country") .
                                       FILTER(str(?diseaseCat) = "disease") .
                                }''')
        for row in results:
            if row.__getattr__("diseaseName").__reduce__()[1][0] not in diseases:
                diseases.append(row.__getattr__("diseaseName").__reduce__()[1][0])

        return diseases

    def search_diseaseByClimate(self, name):
        print("search_diseaseByClimate")

        filename = "country.rdf"
        rdfextras.registerplugins()

        diseases = []
        diseaseNames = []

        g = rdflib.Graph()
        try:
            g.parse(filename)
        except:
            filename = "country.rdf"
            g.parse(filename)

        results = g.query('''
            PREFIX wikidataQ:<https://www.wikidata.org/wiki/>
            PREFIX property:<http://meta.schema.org/Property>
            PREFIX person:<http://schema.org/Person>

            SELECT ?diseaseName WHERE {?country wikidataQ:Q7937 ?climat ;
                                                person:nationality ?nationality ;
                                                property:category ?countryCat .
                                       ?disease property:category ?diseaseCat ;
                                                property:name ?diseaseName ;
                                                person:nationality ?nationality .
                                       FILTER(str(?climat) = "''' + name + '''") .
                                       FILTER(str(?countryCat) = "country") .
                                       FILTER(str(?diseaseCat) = "disease") .
                                }''')

        for row in results:
            if row.__getattr__("diseaseName").__reduce__()[1][0] not in diseases:
                diseases.append(row.__getattr__("diseaseName").__reduce__()[1][0])

        return diseases

    def search_diseaseByFood(self, name):
        print("search_diseaseByFood")
        filename = "country.rdf"
        rdfextras.registerplugins()

        diseases = []
        diseaseNames = []

        g = rdflib.Graph()
        try:
            g.parse(filename)
        except:
            filename = "proiect\country.rdf"
            g.parse(filename)

        results = g.query('''
            PREFIX wikidataQ:<https://www.wikidata.org/wiki/>
            PREFIX property:<http://meta.schema.org/Property>
            PREFIX person:<http://schema.org/Person>

            SELECT ?diseaseName WHERE {?disease property:category ?diseaseCat ;
                                                property:name ?diseaseName ;
                                                food:name ?food .
                                       FILTER(str(?food) = "''' + name + '''") .
                                       FILTER(str(?diseaseCat) = "disease") .
                                }''')

        for row in results:
            if row.__getattr__("diseaseName").__reduce__()[1][0] not in diseases:
                diseases.append(row.__getattr__("diseaseName").__reduce__()[1][0])

        return diseases


    def generate_question(self, userID):
        question = {}
        question["question"] = ""
        question["correctAnswer"] = ""
        question["answers"] = []
        userList = dbHandler.getUserList(userID)
        userList.extend(dbHandler.getUserVisitedList(userID))

        if len(userList) > 0:
            ok = False
            while ok == False:
                n = randint(0, len(userList) - 1)
                dID = userList[n][1]
                dName = dbHandler.getElementByID(dID)[0][1]
                disease = self.search_name(dName)
                elements = dbHandler.getElements("disease")

                n = randint(0, len(elements) - 1)
                while elements[n][1] == dName:
                    n = randint(0, len(elements) - 1)
                d1 = elements[n][1]
                n = randint(0, len(elements) - 1)
                while elements[n][1] == dName and elements[n][1] != d1:
                    n = randint(0, len(elements) - 1)
                d2 = elements[n][1]


                question["correctAnswer"] = dName
                question["answers"] = [d1, d2, dName]

            
                n = randint(1, 4)
                if n == 1 and len(disease["symptoms"]) > 0:                
                    for s in disease["symptoms"]:
                        question["question"] = question["question"] + ", " + s
                    question["question"] = "Which disease has the following symptoms: " + question["question"][2:] + "?"
                    ok = True
                    return question

                if n == 2 and len(disease["info"]) > 0:

                    sentences = disease["info"].split(". ")
                    n = randint(0, len(sentences) - 1)
                    while dName.lower() in sentences[n]:
                        n = randint(0, len(sentences) - 1)
                    m = n
                    while m == n:
                        m = randint(0, len(sentences) - 1)
                    question["question"] = sentences[m] + ". " + sentences[n] + "."
                    ok = True
                    return question

                if n == 3 and len(disease["treatment"]) > 0:
                    for t in disease["treatment"]:
                        question["question"] = question["question"] + ", " + t
                    question["question"] = "Which disease has the following treatment: " + question["question"][2:] + "?"
                    ok = True
                    return question

                if n == 4 and len(disease["hasCauses"]) > 0:
                    for c in disease["hasCauses"]:
                        question["question"] = question["question"] + ", " + c
                    question["question"] = "Which disease has the following causes: " + question["question"][2:] + "?"
                    ok = True
                    return question

    def search(self, symptom, treatment, cause, type, country, climate, food):
        hpCharURL = '''https://query.wikidata.org/sparql?query=
                      SELECT ?Slabel
        WHERE{
            ?disease wdt:P31 wd:Q12136.
            ?disease rdfs:label ?Dlabel .
            ?disease wdt:P780 ?symptoms .
            ?symptoms rdfs:label ?Slabel
            FILTER (langMatches( lang(?Slabel), "en" ) )  .
        }
        &format = JSON'''



        headers = {"Accept": "application/json"}
        r2 = requests.get(hpCharURL, headers=headers)
        r = r2.json()

        for d in r["results"]["bindings"]:
            if d['Slabel']['value'] not in symptoms:
                symptoms.append(d['Slabel']['value'])
        info["symptoms"] = symptoms


#s = Sparql()
#search_country("romania")
#print(s.search_diseaseByClimate("humid"))
#print(s.search_diseaseByCountry("romania"))
#print(s.search_diseaseByFood("fats"))
#print(s.search_diseasebyRisk("sedentarism"))
#print(s.search_diseasebyGender("female"))
#s.search_predispositions(True, False, "female", "sugar")
#s.getSuggestions(1)
#s.search_diseaseByCountry("romania")
#s.search_diseaseByActivityAndFood("sedentarism", "fast food")
#s.search_diseaseBySmokingAndActivity("smoking", "sedentarism")
#print(s.getSuggestions(1))
