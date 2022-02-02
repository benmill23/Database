import mysql.connector
from mysql.connector import errorcode
import datetime

# Ben Milligan
# Program 1 database

try:
    mydb = mysql.connector.connect(user='HW3335', password='PW3335',
                                   host='localhost')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    mycursor = mydb.cursor()
    mycursor.execute("DROP DATABASE IF EXISTS Relationship")
    mycursor.execute("CREATE DATABASE IF NOT EXISTS Relationship")
    mycursor.execute("USE Relationship")
    # create table adn set primary key
    mycursor.execute("CREATE TABLE IF NOT EXISTS Person (LastName VARCHAR(25), FirstName VARCHAR(25), DateOfBirth DATE, Gender CHAR, CityOfBirth VARCHAR(25), StateOfBirth VARCHAR(25), CityLive VARCHAR(25), StateLive VARCHAR(25), PRIMARY KEY (LastName, FirstName))")
    # create basicrelationship table
    mycursor.execute("CREATE TABLE IF NOT EXISTS BasicRelationship (LastName1 VARCHAR(25), FirstName1 VARCHAR(25), LastName2 VARCHAR(25), FirstName2 VARCHAR(25), BasicRelationship CHAR, PRIMARY KEY (LastName1, FirstName1, LastName2, FirstName2))")
    # create Relationship table
    mycursor.execute("CREATE TABLE IF NOT EXISTS Relationship (RelationshipName VARCHAR(25), RelationCount INT, AgeDiff CHAR, PRIMARY KEY (RelationshipName))")
    # create RSteps table
    mycursor.execute("CREATE TABLE IF NOT EXISTS RSteps (RelationshipName VARCHAR(25), Step INT, BasicRelationship CHAR, PRIMARY KEY (RelationshipName, Step))")
    # commit to the database
    mycursor.execute(mydb.commit())


    def relateSibling(p1Last, p1First, p2Last, p2First):
        if p1Last == p2Last and p1First == p2First:
            print("Error duplicate info")
        else:
            try:
                mycursor.execute(
                    "SELECT Gender FROM Person WHERE LastName = '{0}' AND FirstName='{1}'".format(
                        p1Last, p1First))
                genderPersonOne = mycursor.fetchone()
                try:
                    mycursor.execute(
                        "SELECT Gender FROM Person WHERE LastName = '{0}' AND FirstName = '{1}'".format(
                            p2Last, p2First))
                    genderPersonTwo = mycursor.fetchone()

                    if genderPersonOne[0] == 'M' and genderPersonTwo[0] == 'M':
                        mycursor.execute(
                            "INSERT INTO BasicRelationship (LastName1, FirstName1, LastName2, FirstName2, BasicRelationship) "
                            "VALUES (%s, %s, %s, %s, %s)",
                            (p2Last, p2First, p1Last, p1First, 'B'))
                        mydb.commit()
                    elif genderPersonOne[0] == 'M' and genderPersonTwo[0] == 'F':
                        mycursor.execute(
                            "INSERT INTO BasicRelationship (LastName1, FirstName1, LastName2, FirstName2, BasicRelationship) "
                            "VALUES (%s, %s, %s, %s, %s)",
                            (p2Last, p2First, p1Last, p1First, 'S'))
                        mydb.commit()
                    elif genderPersonOne[0] == 'F' and genderPersonTwo[0] == 'M':
                        mycursor.execute(
                            "INSERT INTO BasicRelationship (LastName1, FirstName1, LastName2, FirstName2, BasicRelationship) "
                            "VALUES (%s, %s, %s, %s, %s)",
                            (p2Last, p2First, p1Last, p1First, 'B'))
                        mydb.commit()
                    elif genderPersonOne[0] == 'F' and genderPersonTwo[0] == 'F':
                        mycursor.execute(
                            "INSERT INTO BasicRelationship (LastName1, FirstName1, LastName2, FirstName2, BasicRelationship) "
                            "VALUES (%s, %s, %s, %s, %s)",
                            (p2Last, p2First, p1Last, p1First, 'S'))
                        mydb.commit()
                    else:
                        print("Error")
                except mysql.connector.Error:
                    print("did not work")
            except mysql.connector.Error:
                print("doesnt work bro")



    # ask user for input

    # enter in the steps and then you loop into that and
    while True:
        # DONE
        print("What would you like to do?")
        # DONE minus char checking
        print("1. Enter one person")
        # DONE minus char checking
        print("2. Enter relationship about two people in the database")
        # DONE
        print("3. Define a relationship")
        #DONE
        print("4. Enter a person and find all people with a basic relationship to them")
        #
        print("5. Enter a person and a relationship and it will return all people with that relationship")
        #
        print("6. Given a person, list all people that have relationship with him/her, and for each person, the steps between them (you do not need to list relationships)")
        #
        print("7. Given two person, check if they are related within a link of 3 basic relationships. If so, list the relationship (if defined)")
        print("8. Done entering info")
        i = int(input())
        if i == 8:
            break

        # -----------------------------
        # -----------------------------
        # -----------------------------
        # -----------------------------
        elif i == 1:
            lastName = input("last name: ")
            firstName = input("first name: ")
            try:
                print("Enter birthdate: ")
                year = int(input('Enter a year'))
                month = int(input('Enter a month'))
                day = int(input('Enter a day'))
                dateOfBirth = datetime.date(year, month, day)
                # check if just a character
                gender = input("gender: ")
                cityOfBirth = input("city of birth: ")
                stateOfBirth = input("state of birth: ")
                cityLive = input("city you live in: ")
                stateLive = input("state you live in: ")
                try:
                    mycursor.execute(
                        "INSERT INTO Person (LastName, FirstName, DateOfBirth, Gender, CityOfBirth, StateOfBirth, CityLive, StateLive)"
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (lastName, firstName, dateOfBirth, gender, cityOfBirth, stateOfBirth, cityLive, stateLive))
                except mysql.connector.Error:
                    print("you entered bad info")
            except:
                print("error wrong input")

        # -----------------------------
        # -----------------------------
        # -----------------------------
        # -----------------------------
        elif i == 2:
            # enter in person 1 info
            print("Enter person 1: ")
            lastName1 = input("last name: ")
            firstName1 = input("first name: ")
            # query if this person exists
            try:
                mycursor.execute("SELECT * FROM Person WHERE LastName = '{0}' AND FirstName = '{1}'".format(lastName1, firstName1))
                mycursor.fetchall()
                if mycursor.rowcount > 0:
                    print("Person exists...")
                    # enter in person 2 info
                    print("Enter person 2: ")
                    lastName2 = input("last name: ")
                    firstName2 = input("first name: ")
                    try:
                        mycursor.execute("SELECT * FROM Person WHERE LastName = '{0}' AND FirstName = '{1}'".format(lastName2, firstName2))
                        # result = mycursor.fetchall()
                        mycursor.fetchall()
                        if mycursor.rowcount > 0:
                            print("Person exists...")
                            #  now youre going to ask to enter in all the stuff for these two people
                            print("Enter these peoples basic relationship: ")
                            # check character only
                            # go back and check if order of all the querys is correct and everything works given this format
                            basicRelationship = input("basic relationship (first person you entered is second persons (F, M, B, S, H)): ")
                            try:
                                # insert the basic relationship into the table
                                mycursor.execute("INSERT INTO BasicRelationship (LastName1, FirstName1, LastName2, FirstName2, BasicRelationship)"
                                                "VALUES (%s, %s, %s, %s, %s)",(lastName1, firstName1, lastName2, firstName2, basicRelationship))
                                mydb.commit()
                            except mysql.connector.Error:
                                print("you entered bad info")

                            # -------------- FATHER --------------
                            # -------------- FATHER --------------
                            # -------------- FATHER --------------
                            # -------------- FATHER --------------
                            if basicRelationship == 'F':
                                # find all of person 2 siblings
                                mycursor.execute("SELECT LastName2, FirstName2 FROM BasicRelationship WHERE LastName1 = '{0}' AND FirstName1 = '{1}' AND (BasicRelationship = '{2}' OR BasicRelationship = '{3}')".format(lastName2, firstName2, 'S', 'B'))
                                result = mycursor.fetchall()
                                for temp in result:
                                    mycursor.execute("INSERT INTO BasicRelationship (LastName1, FirstName1, LastName2, FirstName2, BasicRelationship)"
                                                    "VALUES (%s, %s, %s, %s, %s)", (lastName1, firstName1, temp[0], temp[1], basicRelationship))
                                mydb.commit()

                                # check if any have mother
                                try:
                                    mycursor.execute("SELECT LastName1, FirstName1 FROM BasicRelationship WHERE LastName2 = '{0}' AND FirstName2 = '{1}' AND BasicRelationship = '{2}'".format(lastName2, firstName2, 'M'))
                                    momName = mycursor.fetchall()
                                    for x in momName:
                                        try:
                                            mycursor.execute(
                                                "INSERT INTO BasicRelationship (LastName1, FirstName1, LastName2, FirstName2, BasicRelationship)"
                                                "VALUES (%s, %s, %s, %s, %s)",
                                                (lastName1, firstName1, x[0], x[1], 'H'))
                                            mydb.commit()
                                        except mysql.connector.Error:
                                            print("Error inserting into database")

                                except mysql.connector.Error:
                                    print("No mother")

                            # -------------- MOTHER --------------
                            # -------------- MOTHER --------------
                            # -------------- MOTHER --------------
                            # -------------- MOTHER --------------
                            elif basicRelationship == 'M':
                                # find all of person 1 children
                                mycursor.execute("SELECT LastName2, FirstName2 FROM BasicRelationship WHERE LastName1 = '{0}' AND FirstName1 = '{1}' AND (BasicRelationship = '{2}' OR BasicRelationship = '{3}')".format(lastName2, firstName2, 'S', 'B'))
                                result = mycursor.fetchall()
                                for temp in result:
                                    mycursor.execute("INSERT INTO BasicRelationship (LastName1, FirstName1, LastName2, FirstName2, BasicRelationship)"
                                                    "VALUES (%s, %s, %s, %s, %s)",(lastName1, firstName1, temp[0], temp[1], basicRelationship))
                                mydb.commit()

                                # check if any have father
                                try:
                                    mycursor.execute("SELECT LastName1, FirstName1 FROM BasicRelationship WHERE LastName2 = '{0}' AND FirstName2 = '{1}' AND BasicRelationship = '{2}'".format(lastName2, firstName2, 'F'))
                                    dadName = mycursor.fetchall()
                                    for x in dadName:
                                        try:
                                            mycursor.execute("INSERT INTO BasicRelationship (LastName1, FirstName1, LastName2, FirstName2, BasicRelationship)"
                                                            "VALUES (%s, %s, %s, %s, %s)", (x[0], x[1], lastName1, firstName1,'H'))
                                            mydb.commit()
                                        except mysql.connector.Error:
                                            print("Error inserting into database")
                                except mysql.connector.Error:
                                    print("No father")

                            # -------------- BROTHER --------------
                            # -------------- BROTHER --------------
                            # -------------- BROTHER --------------
                            # -------------- BROTHER --------------
                            elif basicRelationship == 'B':
                                relateSibling(lastName1, firstName1, lastName2, firstName2)

                                hasMother = 1
                                hasFather = 1

                                mycursor.execute(
                                    "SELECT LastName2, FirstName2 FROM BasicRelationship WHERE LastName1 = '{0}' AND FirstName1 = '{1}' AND (BasicRelationship = '{2}' OR BasicRelationship = '{3}')".format(
                                        lastName2, firstName2, 'S', 'B'))
                                result = mycursor.fetchall()
                                addList1 = [lastName2, firstName2]
                                result.append(addList1)

                                mycursor.execute(
                                    "SELECT LastName2, FirstName2 FROM BasicRelationship WHERE LastName1 = '{0}' AND FirstName1 = '{1}' AND (BasicRelationship = '{2}' OR BasicRelationship = '{3}')".format(
                                        lastName1, firstName1, 'S', 'B'))
                                result2 = mycursor.fetchall()
                                addList2 = [lastName1, firstName1]
                                result2.append(addList2)

                                for temp in result:
                                    for temp2 in result2:
                                        relateSibling(temp[0], temp[1], temp2[0], temp2[1])
                                        relateSibling(temp2[0], temp2[1], temp[0], temp[1])

                                # get all siblings
                                mydb.commit()
                                mycursor.execute("SELECT LastName2, FirstName2 FROM BasicRelationship WHERE LastName1 = '{0}' AND FirstName1 = '{1}' AND (BasicRelationship = '{2}' OR BasicRelationship = '{3}')".format(lastName1, firstName1, 'S', 'B'))
                                addList3 = [lastName1, firstName1]
                                result3 = mycursor.fetchall()
                                result3.append(addList3)
                                # loop through siblings
                                for temp3 in result3:
                                    try:
                                        mycursor.execute("SELECT LastName1, FirstName1 FROM BasicRelationship WHERE LastName2 = '{0}' AND FirstName2 = '{1}' AND BasicRelationship = '{2}'".format(temp3[0], temp3[1], 'F'))
                                        hasFather = 0
                                        father = mycursor.fetchall()
                                        for x in result3:
                                            for y in father:
                                                try:
                                                    mycursor.execute("INSERT INTO BasicRelationship (LastName1, FirstName1, LastName2, FirstName2, BasicRelationship)"
                                                                    "VALUES (%s, %s, %s, %s, %s)",(y[0], y[1], x[0], x[1], 'F'))
                                                except mysql.connector.Error:
                                                    print("Already has father...")

                                    except mysql.connector.Error:
                                        print("no father")


                                mydb.commit()
                                mycursor.execute(
                                    "SELECT LastName2, FirstName2 FROM BasicRelationship WHERE LastName1 = '{0}' AND FirstName1 = '{1}' AND (BasicRelationship = '{2}' OR BasicRelationship = '{3}')".format(
                                        lastName1, firstName1, 'S', 'B'))
                                addList3 = [lastName1, firstName1]
                                result3 = mycursor.fetchall()
                                result3.append(addList3)
                                # loop through siblings
                                for temp3 in result3:
                                    try:
                                        mycursor.execute(
                                            "SELECT LastName1, FirstName1 FROM BasicRelationship WHERE LastName2 = '{0}' AND FirstName2 = '{1}' AND BasicRelationship = '{2}'".format(
                                                temp3[0], temp3[1], 'M'))
                                        hasMother = 0
                                        mother = mycursor.fetchall()

                                        for x in result3:
                                            for y in mother:
                                                try:
                                                    mycursor.execute(
                                                        "INSERT INTO BasicRelationship (LastName1, FirstName1, LastName2, FirstName2, BasicRelationship)"
                                                        "VALUES (%s, %s, %s, %s, %s)",
                                                        (y[0], y[1], x[0], x[1], 'M'))
                                                except mysql.connector.Error:
                                                    print("Already has mother...")

                                    except mysql.connector.Error:
                                        print("no mother")
                                if hasMother == 0 and hasFather == 0:
                                    # query to get the fathers name
                                    mycursor.execute(
                                        "SELECT LastName1, FirstName1 FROM BasicRelationship WHERE LastName2 = '{0}' AND FirstName2 = '{1}' AND BasicRelationship = '{2}'".format(
                                            lastName1, firstName1, 'F'))
                                    nameFather = mycursor.fetchall()

                                    # query to get mothers name
                                    mycursor.execute(
                                        "SELECT LastName1, FirstName1 FROM BasicRelationship WHERE LastName2 = '{0}' AND FirstName2 = '{1}' AND BasicRelationship = '{2}'".format(
                                            lastName1, firstName1, 'M'))
                                    nameMother = mycursor.fetchall()
                                    for x in nameFather:
                                        for y in nameMother:
                                            try:
                                                mycursor.execute(
                                                    "INSERT INTO BasicRelationship (LastName1, FirstName1, LastName2, FirstName2, BasicRelationship)"
                                                    "VALUES (%s, %s, %s, %s, %s)", (x[0], x[1], y[0], y[1], 'H'))
                                            except mysql.connector.Error:
                                                print("Error, trying to insert duplicate values")
                                    mydb.commit()

                            # -------------- SISTER --------------
                            # -------------- SISTER --------------
                            # -------------- SISTER --------------
                            # -------------- SISTER --------------
                            elif basicRelationship == 'S':
                                relateSibling(lastName1, firstName1, lastName2, firstName2)

                                hasMother = 1
                                hasFather = 1

                                mycursor.execute(
                                    "SELECT LastName2, FirstName2 FROM BasicRelationship WHERE LastName1 = '{0}' AND FirstName1 = '{1}' AND (BasicRelationship = '{2}' OR BasicRelationship = '{3}')".format(lastName2, firstName2, 'S', 'B'))
                                result = mycursor.fetchall()
                                addList1 = [lastName2, firstName2]
                                result.append(addList1)

                                mycursor.execute(
                                    "SELECT LastName2, FirstName2 FROM BasicRelationship WHERE LastName1 = '{0}' AND FirstName1 = '{1}' AND (BasicRelationship = '{2}' OR BasicRelationship = '{3}')".format(
                                        lastName1, firstName1, 'S', 'B'))
                                result2 = mycursor.fetchall()
                                addList2 = [lastName1, firstName1]
                                result2.append(addList2)

                                for temp in result:
                                    for temp2 in result2:
                                        relateSibling(temp[0], temp[1], temp2[0], temp2[1])
                                        relateSibling(temp2[0], temp2[1], temp[0], temp[1])

                                # get all siblings
                                mydb.commit()
                                mycursor.execute(
                                    "SELECT LastName2, FirstName2 FROM BasicRelationship WHERE LastName1 = '{0}' AND FirstName1 = '{1}' AND (BasicRelationship = '{2}' OR BasicRelationship = '{3}')".format(
                                        lastName1, firstName1, 'S', 'B'))
                                addList3 = [lastName1, firstName1]
                                result3 = mycursor.fetchall()
                                result3.append(addList3)
                                # loop through siblings
                                for temp3 in result3:
                                    try:
                                        mycursor.execute(
                                            "SELECT LastName1, FirstName1 FROM BasicRelationship WHERE LastName2 = '{0}' AND FirstName2 = '{1}' AND BasicRelationship = '{2}'".format(
                                                temp3[0], temp3[1], 'F'))
                                        hasFather = 0
                                        father = mycursor.fetchall()
                                        for x in result3:
                                            for y in father:
                                                try:
                                                    mycursor.execute(
                                                        "INSERT INTO BasicRelationship (LastName1, FirstName1, LastName2, FirstName2, BasicRelationship)"
                                                        "VALUES (%s, %s, %s, %s, %s)",
                                                        (y[0], y[1], x[0], x[1], 'F'))
                                                except mysql.connector.Error:
                                                    print("Already has father...")

                                    except mysql.connector.Error:
                                        print("no father")

                                mydb.commit()
                                mycursor.execute(
                                    "SELECT LastName2, FirstName2 FROM BasicRelationship WHERE LastName1 = '{0}' AND FirstName1 = '{1}' AND (BasicRelationship = '{2}' OR BasicRelationship = '{3}')".format(
                                        lastName1, firstName1, 'S', 'B'))
                                addList3 = [lastName1, firstName1]
                                result3 = mycursor.fetchall()
                                result3.append(addList3)
                                # loop through siblings
                                for temp3 in result3:
                                    try:
                                        mycursor.execute(
                                            "SELECT LastName1, FirstName1 FROM BasicRelationship WHERE LastName2 = '{0}' AND FirstName2 = '{1}' AND BasicRelationship = '{2}'".format(
                                                temp3[0], temp3[1], 'M'))
                                        hasMother = 0
                                        mother = mycursor.fetchall()

                                        for x in result3:
                                            for y in mother:
                                                try:
                                                    mycursor.execute(
                                                        "INSERT INTO BasicRelationship (LastName1, FirstName1, LastName2, FirstName2, BasicRelationship)"
                                                        "VALUES (%s, %s, %s, %s, %s)",
                                                        (y[0], y[1], x[0], x[1], 'M'))
                                                except mysql.connector.Error:
                                                    print("Already has mother...")

                                    except mysql.connector.Error:
                                        print("no mother")
                                mydb.commit()
                                if hasMother == 0 and hasFather == 0:
                                    # query to get the fathers name
                                    mycursor.execute("SELECT LastName1, FirstName1 FROM BasicRelationship WHERE LastName2 = '{0}' AND FirstName2 = '{1}' AND BasicRelationship = '{2}'".format(lastName1, firstName1, 'F'))
                                    nameFather = mycursor.fetchall()

                                    # query to get mothers name
                                    mycursor.execute("SELECT LastName1, FirstName1 FROM BasicRelationship WHERE LastName2 = '{0}' AND FirstName2 = '{1}' AND BasicRelationship = '{2}'".format(lastName1, firstName1, 'M'))
                                    nameMother = mycursor.fetchall()
                                    for x in nameFather:
                                        for y in nameMother:
                                            try:
                                                mycursor.execute("INSERT INTO BasicRelationship (LastName1, FirstName1, LastName2, FirstName2, BasicRelationship)"
                                                                "VALUES (%s, %s, %s, %s, %s)", (x[0], x[1], y[0], y[1], 'H'))
                                            except mysql.connector.Error:
                                                print("Error, trying to insert duplicate values")
                                    mydb.commit()

                            else:
                                print("lame")
                        else:
                            print("Person doesnt exist, sorry...")
                    except mysql.connector.Error:
                        print("Person doesnt exist...")
                else:
                    print("Sorry, person does not exist...")
            except mysql.connector.Error:
                print("error, person doesnt exist")

        # -----------------------------
        # -----------------------------
        # -----------------------------
        # -----------------------------
        elif i == 3:
            # DEFINING A RELATIONSHIP
            print("What is the name of this relationship?")
            rName = input()
            try:
                rCount = int(input("What is the relation count?"))
                ageDiff = input("Does this relationship depend on age? ('N' for no, 'O' if 1st person is older or same age, 'Y' if the 1st person is strictly younger)")
                if ageDiff == 'N' or ageDiff == 'O' or ageDiff == 'Y':
                    # insert into table
                    try:
                        mycursor.execute("INSERT INTO Relationship (RelationshipName, RelationCount, AgeDiff)"
                                         "VALUES (%s, %s, %s)", (rName, rCount, ageDiff))
                        mydb.commit()
                        num = 1
                        while num <= rCount:
                            print("Enter the character of the basic relationship at this step (person 1 is person 2's):")
                            basicRelationship = str(input("(N = son, R = daughter, W = wife, e = elder bro, y = younger bro, s = elser sis, i = younger sis)"))
                            if len(basicRelationship) < 2:
                                # input into the queries
                                try:
                                    mycursor.execute("INSERT INTO RSteps (RelationshipName, Step, BasicRelationship)"
                                                    "VALUES (%s, %s, %s)", (rName, num, basicRelationship))
                                except mysql.connector.Error:
                                    print("Error, insert into table failed...")
                            else:
                                print("Invalid input")
                            num += 1
                        mydb.commit()
                    except mysql.connector.Error:
                        print("Error, insert failed")
                else:
                    print("Sorry, not a valid option, please try again")
            except ValueError:
                print("sorry, not a valid count")

        # -----------------------------
        # -----------------------------
        # -----------------------------
        # -----------------------------
        elif i == 4:
            # list all people with basic relation to the person they enter
            firstName = input("Please enter first name of person: ")
            lastName = input("Please enter last name of person: ")

            try:
                mycursor.execute("SELECT * FROM Person WHERE LastName = '{0}' AND FirstName = '{1}'".format(lastName, firstName))
                try:
                    mycursor.execute(
                        "SELECT LastName2, FirstName2, BasicRelationship FROM BasicRelationship WHERE LastName1 = '{0}' AND FirstName1 = '{1}' AND (BasicRelationship = '{2}' OR BasicRelationship = '{3}')".format(
                            lastName, firstName, 'B', 'S'))
                    result = mycursor.fetchall()
                    for temp in result:
                        if temp[2] == 'B':
                            print(firstName, " ", lastName, " is the brother of ", temp[1], " ", temp[0])
                        elif temp[2] == 'S':
                            print(firstName, " ", lastName, " is the sister of ", temp[1], " ", temp[0])
                except mysql.connector.Error:
                    print("This person has no siblings...")

                try:
                    mycursor.execute(
                        "SELECT LastName1, FirstName1, BasicRelationship FROM BasicRelationship WHERE LastName2 = '{0}' AND FirstName2 = '{1}' AND (BasicRelationship = '{2}' OR BasicRelationship = '{3}')".format(
                            lastName, firstName, 'F', 'M'))
                    result2 = mycursor.fetchall()
                    for temp in result2:
                        if temp[2] == 'F':
                            print(temp[1], " ", temp[0], " is the Father of ", firstName, " ", lastName)
                        elif temp[2] == 'M':
                            print(temp[1], " ", temp[0], " is the Mother of ", firstName, " ", lastName)
                except mysql.connector.Error:
                    print("This person does not have a father or mother")

                try:
                    mycursor.execute(
                        "SELECT gender FROM Person WHERE LastName = '{0}' AND FirstName = '{1}'".format(lastName,
                                                                                                        firstName))
                    result3 = mycursor.fetchall()
                    if result3[0] == 'M':
                        # then they can have a wife
                        try:
                            mycursor.execute(
                                "SELECT LastName2, FirstName2 FROM BasicRelationship WHERE LastName1 = '{0}' AND FirstName1 = '{1}' AND BasicRelationship = '{2}'".format(
                                    lastName, firstName, 'H'))
                            result4 = mycursor.fetchall()
                            for temp in result4:
                                print(firstName, " ", lastName, " is the Husband of ", temp[1], " ", temp[0])
                        except mysql.connector.Error:
                            print()
                    elif result3[0] == 'F':
                        # then they can have a husband
                        try:
                            mycursor.execute(
                                "SELECT LastName1, FirstName1 FROM BasicRelationship WHERE LastName2 = '{0}' AND FirstName2 = '{1}' AND BasicRelationship = '{2}'".format(
                                    lastName, firstName, 'H'))
                            result5 = mycursor.fetchall()
                            for temp in result5:
                                print(firstName, " ", lastName, " is the Wife of ", temp[1], " ", temp[0])
                        except mysql.connector.Error:
                            print()
                except mysql.connector.Error:
                    print("Error, invalid person")
            except mysql.connector.Error:
                print("This person does not exist...")

        # -----------------------------
        # -----------------------------
        # -----------------------------
        # -----------------------------
        elif i == 5:
            # Given a person, and a relationship, return all people with that relationship
            firstName = input("Please enter first name of person: ")
            lastName = input("Please enter last name of person: ")

            try:
                mycursor.execute("SELECT * FROM Person WHERE LastName = '{0}' AND FirstName = '{1}'".format(lastName, firstName))
                mycursor.fetchall()
                relationship = str(input("Enter the name of the relationship: "))
                try:
                    mycursor.execute(
                        "SELECT RelationshipName, RelationCount FROM Relationship WHERE RelationshipName = '{0}'".format(
                            relationship))
                    result = mycursor.fetchall()
                    num = result[0][1]
                    name = result[0][0]

                    while num >= 1:
                        # query the rsteps table
                        try:
                            # have the highest instance of the step
                            mycursor.execute("SELECT BasicRelationship FROM RSteps WHERE Step = '{0}' AND RelationshipName = '{1}'".format(num, name))
                            result2 = mycursor.fetchall()
                            # holds relationship name
                            relation = result2[0][0]
                            # use this to find that persons blank
                            if relation == 'B':
                                mycursor.execute("SELECT LastName1, FirstName1 FROM BasicRelationship WHERE Lastname2 = '{0}' AND FirstName2 = '{1}' AND BasicRelationship = '{2}'".format(lastName, firstName, 'B'))
                                result3 = mycursor.fetchall()

                            elif relation == 'S':
                                mycursor.execute()

                            elif relation == 'F':
                                mycursor.execute()

                            elif relation == 'M':
                                mycursor.execute()

                            elif relation == 'H':
                                mycursor.execute()

                            elif relation == 'N':
                                mycursor.execute()

                            elif relation == 'R':
                                mycursor.execute()

                            elif relation == 'W':
                                mycursor.execute()

                            elif relation == 'e':
                                mycursor.execute()

                            elif relation == 'y':
                                mycursor.execute()

                            elif relation == 's':
                                mycursor.execute()

                            elif relation == 'i':
                                mycursor.execute()

                            else:
                                print("Invalid input")
                        except mysql.connector.Error:
                            print("query failed")

                        num -= 1



                    # query relationship table to get step count and then query each step or all
                        # use info from relationship table to loop and query the rsteps table
                            # for each step in the rsteps table
                                # use the5
                except mysql.connector.Error as e:
                    print(e)

                    print("worked")
                except mysql.connector.Error:
                    print("didnt work")
            except mysql.connector.Error:
                print("Error, person you entered does not exist")

        # -----------------------------
        # -----------------------------
        # -----------------------------
        # -----------------------------
        elif i == 6:
            print("algorithm 3")

        # -----------------------------
        # -----------------------------
        # -----------------------------
        # -----------------------------
        elif i == 7:
            # Given two person, check if they are related within a link of 3 basic relationships. If so, list the
            # relationship (if defined)
            firstName1 = input("enter first name of person 1:")
            lastName1 = input("enter last name of person 1:")

            try:
                mycursor.execute("SELECT * FROM Person WHERE LastName = '{0}' AND FirstName = '{1}'".format(lastName1, firstName1))
                mycursor.fetchall()
                firstName2 = input("enter first name of person 2:")
                lastName2 = input("enter last name of person 2:")
                try:
                    mycursor.execute("SELECT * FROM Person WHERE LastName = '{0}' AND FirstName = '{1}'".format(lastName2, firstName2))
                    mycursor.fetchall()
                    count = 0
                    try:
                        mycursor.execute("SELECT LastName2, FirstName2 FROM BasicRelationship WHERE LastName1 = '{0}' AND FirstName1 = '{1}'".format(lastName1, firstName1))
                        result = mycursor.fetchall()


                    except mysql.connector.Error:
                        print("query error")

                except mysql.connector.Error:
                    print("Error person doenst exist")
            except mysql.connector.Error:
                print("Person doesnt exist")
        else:
            print("not valid input")
    # commmit to the database
    mydb.commit()
    # add stuff to my tables
    mycursor.close()
    mydb.close()
