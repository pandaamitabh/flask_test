from flask import Flask

app = Flask(__name__)



@app.route("/cgi-bin/")
def script1():
    pass
   #./some_script.py    # e.g. I want to make flask run some_script.py, which is in the same directory as my flask.py file on a server

def script2():
    pass
   #./some_other_script.py    # e.g. same thing