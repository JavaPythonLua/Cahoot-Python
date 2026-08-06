import sqlite3
full_dict = {}
print("welcome to the Kohoot! question pack creator")
print("Please enter the name that you would like your question pack file to be named:")
PackName = input('')
con = sqlite3.connect(f"{PackName}.db")
cur = con.cursor()
cur.execute("CREATE TABLE packData (QuizNo int PRIMARY KEY, QuizName varchar(255), NoQs int NOT NULL, QuizType varchar(10))")
print("Please enter the number of quizzes you would like to create in this pack:")
NoQuizzes = int(input())
for i in range(0,NoQuizzes):
    print(f"Please enter the name of quiz {i+1}:")
    QuizName = input('')
    cur.execute(f'CREATE TABLE "{QuizName}" (QuesNo int NOT NULL, QuesName varchar(255), Ans1 varchar(255), Ans2 varchar(255), Ans3 varchar(255), CorrectAns varchar(1) NOT NULL)')
    print(f"Please enter the number of questions in quiz {i+1}: ")
    NoQs = input('')
    cur.execute("INSERT INTO packData (QuizNo, QuizName, NoQs, QuizType) VALUES (?, ?, ?, ?)",(i+1,QuizName,int(NoQs),"quiz"))
    con.commit()
    rounds = 0
    for i in range(0,int(NoQs)):
        rounds +=1
        print("What is the question?")
        Q = input('')
        print("What is answer A?")
        Ans1 = input('')
        print("What is answer B?")
        Ans2 = input('')
        print("What is answer C?")
        Ans3 = input('')
        print("What is the correct answer? (a, b or c)")
        CorrectAns = input('')
        cur.execute(f'INSERT INTO "{QuizName}" (QuesNo, QuesName, Ans1, Ans2, Ans3, CorrectAns) VALUES (?, ?, ?, ?, ?, ?)',(rounds, Q, Ans1, Ans2, Ans3, CorrectAns))
        con.commit()
con.close()