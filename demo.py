from flask import Flask, render_template
from data import posts
app = Flask(__name__)



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts = posts)

@app.route("/about")
def about():
    return render_template('about.html', title='about')


import time
import json
@app.route("/time")
def timeCurent():
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    in_dictionary_form = {"time":time_string}
    json_response = json.dumps(in_dictionary_form)
    return render_template('time.html', current_time = time_string)


if __name__ == '__main__':
    app.run(debug = True)

{'friend_name':['sifat','siraj','talha','ali']}