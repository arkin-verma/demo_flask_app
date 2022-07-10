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

# TASK: Create 3 more routes/pages
@app.route('/photos')
def photos():
    return render_template('photos.html')

@app.route('/recipes')
def recipes():
    return render_template('recipes.html')

@app.route('/music')
def music():
    return render_template('music.html')



#nm in the return statement above is a variable that can be used in html
if __name__ == '__main__':
    app.run(debug = True) # run this server in a testing mode
    

# Task: create 3 more pages (i.e. 3 more routes)
# Note: TemplateNotFound Error raised when clicking 'Recipes Page' and 'Music Page' button