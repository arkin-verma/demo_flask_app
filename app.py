from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/') # whenever the user opens this app, load the following function
def index():
    name = "Python Flask Famework"
    task = f"Create a web application using {name}"
    return render_template('index.html', nm = name,task=task) # checks if this file exists

@app.route('/news')
def news():
    return render_template('news.html')

#nm in the return statement above is a variable that can be used in html
if __name__ == '__main__':
    app.run(debug = True) # run this server in a testing mode
    

# Task: create 3 more pages (i.e. 3 more routes)