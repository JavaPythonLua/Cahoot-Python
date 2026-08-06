#"clientSQL.py" A program to try to re-create the popular quiz game Kahoot! in python
#Copyright (C) 2026  Alex Inns

#You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.


import socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("Created socket")
HOST = input("Host: ")
PORT = int(input("Port: "))
s.connect((HOST,PORT))
print("Connected to server")
print("Enter your nickname:")
nick = input()
s.send(nick.encode('utf-8'))

while True:
    q = s.recv(1024).decode('utf-8')
    if q == "Q":
        print("Answer A or B or C:")
        ans = input().lower()
        s.send(ans.encode('utf-8'))
        right = s.recv(1024).decode('utf-8')
        if right == "correct":
            print("You were correct!")
        else:
            print("You were incorrect!")
    elif q == "e":
        break
place = s.recv(1024).decode('utf-8')
print("That's the end of the quiz")
print(f"You came in {place}th place")