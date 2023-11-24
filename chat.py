import socket
import pytchat
from os import path, system
from threading import Thread
from datetime import datetime
import config

sock = socket.socket()

chatlog = "chat.log"

with open(chatlog, "r") as cl:
	with open(chatlog+"_bak", "w") as bak:
		bak.write(cl.read())
with open(chatlog, "w"):
	pass


chat = pytchat.create(video_id=config.YOUTUBE_VIDEO)


srv = "irc.chat.twitch.tv"
port = 6667
nickname=config.TWITCH_NICK
channel="#"+config.TWITCH_CHANNEL
token = config.TWITCH_TOKEN

sock.connect((srv, port))

sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))


def getYT(cht):
	while cht.is_alive() and not path.exists("KILL_PROC"):
		for c in cht.get().sync_items():
			print(f"{c.datetime} [{c.author.name}]- {c.message}")
			with open(chatlog, "a") as f:
				f.write(f"YT: {c.datetime},{c.author.name},{c.message}\n")

thr = Thread(target=getYT, args=(chat, ))
thr.start()
while True:
	print("running...")
	if path.exists("KILL_PROC"):
		thr._stop()
		system("rm KILL_PROC")
		system("del KILL_PROC")
		system("cls")
		exit()
	
	resp = sock.recv(2048).decode('utf-8')
	print("got: "+resp)
	if ":tmi.twitch.tv" in resp:
		print("SKIPPED: "+resp)
	elif len(resp.split(":")) == 6 and "JOIN" in resp:
		print("SKIPPED: "+resp)
	else:	
		name = resp.split(":")[1].split("!")[0]
		msg=""
		for i in range(len(resp.split(":"))-2):
			msg = msg + ":" + resp.split(":")[i+2]	
		msgtime = datetime.now().strftime("%Y-%m-%D %H:%m:%S")
		print(msgtime, name, ":", msg.lstrip(":"))
		with open(chatlog, "a") as f:
			f.write(f"TW: {msgtime},{name},{msg}\n")
sock.close()
