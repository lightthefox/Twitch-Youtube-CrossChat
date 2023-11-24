from flask import Flask as fls, request as req
import config as conf
import threading
import subprocess
import time
app = fls("twitch_youtube_chat")

def change_config(key, value):
	with open("config.py", "r") as cnf:
		c = cnf.read().split("\n")
		with open("config.py", "w") as cr:
			for line in c:
				li = line
				if li.startswith(key):
					li = key + ' = "' + value + '"'
				cr.write(li+"\n")

def load_template(template):
	with open("templates/"+template, "r") as f:
		return f.read()

def restart():
	subprocess.run(["python","chat.py"])
	
thr = threading.Thread(target=restart)

thr.start()
@app.route("/")
def root():
	
	return load_template("index.html")
@app.route("/getchat")
def getchat():
	with open("chat.log","r") as cl:
		f = cl.read().split("\n")
		f.reverse()
		f.pop(0)
		o = "\n".join(f)
		return o
	

@app.route("/config")
def config():
	ret = ""
	with open("templates/config_page.html","r") as f:
		ret = f.read()
		ret = ret.replace("%YOUTUBE_LIVESTREAM", conf.YOUTUBE_VIDEO)
		
		ret = ret.replace("%TWITCH_CHANNEL", conf.TWITCH_CHANNEL)
		
		ret = ret.replace("%TWITCH_NICK", conf.TWITCH_NICK)
		
		ret = ret.replace("%TWITCH_TOKEN", conf.TWITCH_TOKEN)
	return ret
	
@app.route("/submit")
def submit():
	global thr
	change_config("YOUTUBE_VIDEO", req.args.get("yt_live"))
	change_config("TWITCH_CHANNEL", req.args.get("tw_chn"))
	change_config("TWITCH_NICK", req.args.get("tw_nick"))
	change_config("TWITCH_TOKEN", req.args.get("tw_tkn"))
	
	print("youtube:", req.args.get("yt_live"))
	print("twitch:", req.args.get("tw_chn"))
	print("nick:", req.args.get("tw_nick"))
	print("tkn:", req.args.get("tw_tkn"))
	with open("KILL_PROC", "w") as kp:
		kp.close()
	thr._delete()
	
	thr = threading.Thread(target=restart)
	#thr._stop()
	time.sleep(0.8)
	thr.start()
	return "Submitted Changes."
app.run(debug=False, port=2545)