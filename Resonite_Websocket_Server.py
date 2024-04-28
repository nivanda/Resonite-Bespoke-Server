import socket, threading, random
import module

HEADER = 64
PORT = 5050
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

TASK = ""
TASK_DONE = True
CONFIRMATION_SENT = True

modules = {"sg": [], "env": [], "noteseq": []}

def main():
   global TASK, TASK_DONE, modules
   gain = module.get("gain")
   while True:
      if not TASK_DONE:
         if "create sg" in TASK:
            sgName = TASK.split()[2]
            exec(sgName + " = module.create('signalgenerator', random.randint(1, 10000), random.randint(1, 10000))")
            modules["sg"].append(sgName)
            TASK_DONE = True
         if "create env" in TASK:
            envName = TASK.split()[2]
            exec(envName + " = module.create('envelope', random.randint(1, 10000), random.randint(1, 10000))")
            modules["env"].append(envName)
            TASK_DONE = True
         if "create noteseq" in TASK:
            noteseqName = TASK.split()[2]
            exec(noteseqName + " = module.create('notesequencer', random.randint(1, 10000), random.randint(1, 10000))")
            modules["noteseq"].append(noteseqName)
            TASK_DONE = True
         if "connect main" in TASK:
            source = TASK.split()[2]
            destination = TASK.split()[3]



def handle_client(conn, addr):
   global TASK, TASK_DONE, CONFIRMATION_SENT
   connected = True
   while connected:
      if TASK_DONE and CONFIRMATION_SENT:
         msg_length = conn.recv(HEADER).decode(FORMAT)
         if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
               connected = False
            else:
               TASK = msg
               TASK_DONE = False
               CONFIRMATION_SENT = False
      elif TASK_DONE and not CONFIRMATION_SENT:
         conn.send("done".encode(FORMAT))
         CONFIRMATION_SENT = True

   conn.close()

def start():
   server.listen()
   while True:
      conn, addr = server.accept()
      thread = threading.Thread(target=handle_client, args=(conn, addr))
      thread.start()

mainThread = threading.Thread(target=main)
mainThread.start()
serverThread = threading.Thread(target=start)
serverThread.start()