#Importing Modules
import socket
import queue
import threading
import logging
import sqlite3
logging.basicConfig(level=logging.WARN)

#Defining Queues
ans_queue = queue.Queue()
addr_queue = queue.Queue()
conn_queue = queue.Queue()
nickname_queue = queue.Queue()
score_queue  = queue.Queue()

#Defining Lists
addr_list = []
conn_list = []


#Defining Functions
def accept_conn(s,addr_queue,conn_queue,nickname_queue):
    while conns == True:
        conn,addr = s.accept()
        print(f"got connection from {str(addr)}")
        conn_queue.put(conn)
        addr_queue.put(addr)
        nickname = conn.recv(1024).decode('utf-8')
        nickname_queue.put(nickname)
        print(f'"{nickname}" joined the game')
def wait_for_start():
    global conns
    input("Press enter to start...")
    conns = False
def handle_qs(s,conn,ans_queue):
    logging.debug("handle_qs")
    conn.send("Q".encode('utf-8'))
    logging.debug("Message sent")
    message = conn.recv(1024).decode('utf-8')
    ans = (conn,message)
    ans_queue.put(ans)
def end_quiz(s,conn,place):
    logging.debug("ending")
    conn.send("e".encode('utf-8'))
    logging.debug("ending sent")
    conn.send(str(place).encode('utf-8'))
    logging.debug('sent place')
def recv_score(s,conn,score_queue):
    score = conn.recv(1024).decode('utf-8')
    score_queue.put(score)

score_dict = {}

#Unpacking The quiz pack file
kpack = input("What is the pack name?")

con = sqlite3.connect(f"{kpack}.db")
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
res = cur.execute(f"SELECT QuizName FROM packData WHERE QuizNo = {ChosenNo}")
QName = res.fetchone()[0]
res = cur.execute(f"SELECT QuizType FROM packData WHERE QuizNo = {ChosenNo}")
QType = res.fetchone()[0]
res = cur.execute(f"SELECT NoQs FROM packData WHERE QuizNo = {ChosenNo}")
noQs = res.fetchone()[0]
print(f"The name of the quiz is {QName}")

#Getting conn data and handling conns
connstup = tuple()
no_conns = int(input('Enter the number of players: '))
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
HOST = socket.gethostbyname(socket.gethostname())
OPORT = 0
s.bind((HOST,OPORT))
PORT = str(s.getsockname()[1])
print(f"The host is: {HOST}")
print(f"The port is: {PORT}")
s.listen()
global conns
conns = True
for j in range(0 ,no_conns):
    conns_queue = threading.Thread(target=accept_conn,args=(s,addr_queue,conn_queue,nickname_queue))
    conns_queue.start()
rounds = 0
wait_start_thread = threading.Thread(target=wait_for_start)
wait_start_thread.start()
while len(connstup) < no_conns:
    conn = conn_queue.get()
    nickname  = nickname_queue.get()
    score_dict[conn] = {"nickname":nickname,"score":0}
    connstup = connstup + (conn,)
logging.debug(len(connstup))
wait_start_thread.join()




#Handling questions and recieving answers
for f in range(0,noQs):
    index = "Q"+str(f+1)

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
    print(index+":")
    print(question)
    print("A: " + Q1)
    print("B: " + Q2)
    print("C: " + Q3)
    logging.debug(len(connstup))
    for i in range(0,len(connstup)):
        logging.debug("Loop1")
        handle_thread = threading.Thread(target=handle_qs,args=(s,connstup[i],ans_queue,)).start()
        logging.debug("Thread")
        rounds = 0
    while len(connstup) > rounds:
        ans = ans_queue.get()
        if ans == None:
            pass
        elif ans[1] == Correct:
            ans[0].send("correct".encode('utf-8'))
            rounds += 1
            score_dict[ans[0]]["score"] += 1
        elif rounds != Correct:
            ans[0].send("wrong".encode('utf-8'))
            rounds += 1
print(score_dict)
top_score = 0
for i in range(0,len(connstup)):
    score = score_dict[connstup[i]]["score"]
    if score >= top_score:
        top_score = score
        top_nick = score_dict[connstup[i]]["nickname"]
print(f"The winner was {top_nick} with {top_score} points")

con.close()
