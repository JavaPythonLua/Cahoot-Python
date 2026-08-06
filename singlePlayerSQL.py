#"singlePlayerSQL.py" A program to try to re-create the popular quiz game Kahoot! in python
#Copyright (C) 2026  Alex Inns


import time
import sys
import os
import sqlite3

NoQ = 1
Score = 0
print("Place place the question pack file in the following directory:")
print("\n")
print(os.getcwd())
print("\n")
input("Press enter once you are done")
try:
    PackName = str(input("Pack Name: "))
    con = sqlite3.connect(f"{PackName}.db")
    cur = con.cursor()
    res = cur.execute("SELECT COUNT(*) FROM packData")
    NoQuizzes = res.fetchone()[0]
    print(f"There are {NoQuizzes} quizzes in this pack.")
    for i in range(0,int(NoQuizzes)):
        res = cur.execute(f"SELECT QuizName FROM packData WHERE QuizNo = {i+1}")
        CurrentQuizName = res.fetchone()[0]
        print(f"{i+1}: {CurrentQuizName}")
    print("\nChoose a quiz number: ")
    ChosenNo = int(input())

except:
    print("Unable to open the Pack. Restart the project and check your spelling")
    print("If you call a support person give them this code:")
    print("ERR_METAFILE_NOT_FOUND")
    sys.exit(1)
try:
    res = cur.execute(f"SELECT QuizName FROM packData WHERE QuizNo = {ChosenNo}")
    QName = res.fetchone()[0]
    res = cur.execute(f"SELECT QuizType FROM packData WHERE QuizNo = {ChosenNo}")
    QType = res.fetchone()[0]
    res = cur.execute(f"SELECT NoQs FROM packData WHERE QuizNo = {ChosenNo}")
    NoQs = res.fetchone()[0]
except:
    print("Unable to load required information, try restarting the project.")
    print("If you call a support person give them this code:")
    print("ERR_METAFILE_DATA_INCORRECT")
    sys.exit(1)
try:
    print(f"The name of the quiz is: {QName}")
except:
    print("Unable to load questions, try restarting the project.")
    print("If you call a support person give them this code:")
    print("ERR_QUESTIONSFILE_NOT_FOUND")
    sys.exit(1)
for i in range(NoQs):
    Score = str(Score)
    try:
        res = cur.execute(f'SELECT QuesName FROM "{QName}" WHERE QuesNo = {NoQ}')
        question = res.fetchone()[0]
        res = cur.execute(f'SELECT Ans1 FROM "{QName}" WHERE QuesNo = {NoQ}')
        Q1 = res.fetchone()[0]
        res = cur.execute(f'SELECT Ans2 FROM "{QName}" WHERE QuesNo = {NoQ}')
        Q2 = res.fetchone()[0]
        res = cur.execute(f'SELECT Ans3 FROM "{QName}" WHERE QuesNo = {NoQ}')
        Q3 = res.fetchone()[0]
        res = cur.execute(f'SELECT CorrectAns FROM "{QName}" WHERE QuesNo = {NoQ}')
        Correct = res.fetchone()[0]
    except:
        print("Unable to load answers, try restarting the project.")
        print("If you call a support person give them this code:")
        print("ERR_QUESTIONSFILE_DATA_INCORRECT")
        sys.exit(1)
    print("\n\n")
    time.sleep(1)
    print(f"Q{NoQ}:")
    print(question)
    print(f"Answer A is {Q1}")
    print(f"Answer B is {Q2}")
    print(f"Answer C is {Q3}")
    try:
        ChosenAnswer = str(input("Enter the letter of the correct answer: "))
        ChosenAnswer = ChosenAnswer.lower()
        Score = int(Score)
    except:
        print("Unable to process user input, try restarting the project.")
        print("If you call a support person give them this code:")
        print("ERR_USER_INPUT_NOT_DATA")
        sys.exit(1)
    try:
        if ChosenAnswer == Correct:
            time.sleep(0.5)
            print("That is correct!")
            Score += 1
            time.sleep(0.5)
            print(f"Your score is {Score}")
        else:
            print("Incorrect!")
            time.sleep(0.5)
            print(f"The correct answer is {Correct}")
            time.sleep(0.5)
            print(f"Your score is {Score}")
    except:
        print("Unable to evaluate answer, try restarting the project.")
        print("If you call a support person give them this code:")
        print("ERR_EVALUATE_ANSWER_FAILED")
        sys.exit(1)
    NoQ += 1
    time.sleep(1)
print("That's the end of the quiz")
print(f"You got {Score}/{NoQs}")
con.close()