from flask import Flask, jsonify, request, render_template

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

@app.route('/design_basics')
def design_basics():
    return render_template('design_basics.html')

@app.route('/form1', methods=['GET', 'POST'])
def form1_handler():
    return render_template('form_1.html')

@app.route('/form2', methods=['GET', 'POST'])
def form2_handler():
    return render_template('form_2.html')

@app.route('/form3', methods=['GET', 'POST'])
def form3_handler():
    if request.method == "POST":
        d1 = request.form.get('data1')
        d2 = request.form.get('data2')
        d3 = request.form.get('data3')
        d4 = request.form.get('data4')
        with open('form3Data.txt', 'w') as f:
            f.write(d1+'\n')
            f.write(d2+'\n')
            f.write(d3+'\n')
            f.write(d4+'\n')
    return render_template('form_3.html')

# submits form asynchronously. Form is submitted to this function and page won't be reloaded.
@app.route('/form3_ajax',methods=['POST'])
def form3_ajax_handler():
    name = request.form.get('fullname')
    email = request.form.get('email')
    college = request.form.get('college')
    password = request.form.get('password')
    return jsonify({'status':'success'})

@app.route('/form4', methods=['GET', 'POST'])
def form4_handler():
    if request.method == "POST":
        print(request.form.keys())
        name = request.form.get('Data_Value')
        print("We got", name)
        # name = request.form.get('name')
    return render_template('form_4.html')

@app.route('/form4_ajax',methods=['POST'])
def form4_ajax_handler():
    specialName = request.form.get('name')
    return jsonify({'status':'success'})


#nm in the return statement above is a variable that can be used in html
if __name__ == '__main__':
    app.run(debug = True) # run this server in a testing mode
    

# Task: create 3 more pages (i.e. 3 more routes)
# Note: TemplateNotFound Error raised when clicking 'Recipes Page' and 'Music Page' button