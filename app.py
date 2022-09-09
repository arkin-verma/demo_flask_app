from flask import Flask, jsonify, request, render_template, session, flash, redirect, url_for
from sqlalchemy.orm import sessionmaker
from database import Base, User, ReviewData, create_engine, DATABASE_PATH
import spider


app = Flask(__name__)
app.secret_key = '1s2i3104u83faujsud'

def connect_db():
    engine = create_engine(DATABASE_PATH)
    DBSession = sessionmaker(bind=engine)
    return DBSession()

@app.route('/') # whenever the user opens this app, load the following function
def index():
    name = "Python Flask Famework"
    task = f"Create a web application using {name}"
    return render_template('index.html', nm=name,task=task) # checks if this file exists

@app.route('/login')
def login_form():
    next = request.args.get('next', '/')
    return render_template('login.html', nextaddr=next)

@app.route('/login_api', methods=['POST']) 
def login_api():
    email = request.form.get('email')
    password = request.form.get('password')
    if len(email) == 0 or len(password) == 0:
        return jsonify({"message": "Please enter email and password", 'status':'error'})
    elif len(email)<10 or '@' not in email:
        return jsonify({"message": "Please enter a valid email", 'status':'error'})
    else:
        db = connect_db()
        user = db.query(User).filter_by(email=email).first()
        if user is None:
            db.close()
            return jsonify({"message": "User not found", 'status':'error'})
        elif user.password != password:
            db.close()
            return jsonify({"message": "Incorrect password", 'status':'error'})
        else:
            session['user_id'] = user.id
            session['user_email'] = user.email
            session['is_logged_in'] = True
            db.close()
            return jsonify({'status':"success", "message":"Login successful"})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/register_api',methods=['POST'])
def register_ajax_handler():
    name = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    cpassword = request.form.get('cpassword')
    if len(name)<3:
        return jsonify({"status":"error","message":"Username must be atleast 3 characters"})
    elif len(email)<    10 or '@' not in email:
        return jsonify({"status":"error","message":"Invalid email"})
    elif len(password)<6:
        return jsonify({"status":"error","message":"Password must be atleast 6 characters"})
    elif password != cpassword:
        return jsonify({"status":"error","message":"Passwords do not match"})
    else:
        db = connect_db()
        user = User(name=name,email=email,password=password)
        db.add(user)
        db.commit()
        db.close()
        return jsonify({"status":"success","message":"User created successfully"})

# @app.route('/news')
# def news():
#     return render_template('news.html')

# # TASK: Create 3 more routes/pages
# @app.route('/photos')
# def photos():
#     return render_template('photos.html')

# @app.route('/recipes')
# def recipes():
#     return render_template('recipes.html')

# @app.route('/music')
# def music():
#     return render_template('music.html')

# @app.route('/design_basics')
# def design_basics():
#     return render_template('design_basics.html')

@app.route('/register', methods=['GET', 'POST'])
def register_handler():
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
# Ajax is used for front-end and sending data from the front end.
# Asynchronously.
@app.route('/form3_ajax',methods=['POST'])
def form3_ajax_handler():
    name = request.form.get('data1')
    email = request.form.get('data2')
    college = request.form.get('data3')
    password = request.form.get('data4')

    if len(name) < 3:
        return jsonify({"status":"error", "message": "Username must be at least 3 characters"})
    
    elif len(email) < 10:
        pass # COME BACK TO THIS

    else:
        db = connect_db()
        user = User(name=name, email=email, password=password)
        db.add(user)
        db.commit()
        db.close()
        return jsonify({'status':'success', "message":"User created successfully"})

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

@app.route('/startmining',methods=['GET','POST'])
def start_mining():
    if 'is_logged_in' not in session:
        flash('Please login to start mining')
        return redirect('/login?next=startmining')
    return render_template('start_mining.html')

@app.route('/scrapper_api',methods=['POST'])
def scrapper_api():
    if 'is_logged_in' not in session:
        return jsonify({"status":"error","message":"Please login to start mining"})
    else:
        url = request.form.get('product_url')
        name = request.form.get('product_title')
        userLimit = int(request.form.get('page_limit'))

        # print('LOOK:', url, name, userLimit)

        if 'amazon' not in url: # url validation should be fixed,not the best
            return jsonify({"status":"error","message":"Please enter a valid url"})
        else:
            # call scrapper function
            # save the result in database
            reviewLink = spider.get_review_link(url)

            allReviews = spider.collect_reviews(reviewLink, limit = userLimit)
            if allReviews == None:
                return jsonify({"status":'error', "message": f'No reviews were collected from {reviewLink}'})
            if len(allReviews) == 0:
                return jsonify({"status":'error', "message": 'No reviews were collected'})
            print(len(allReviews))
            fileAddress = spider.save_reviews(allReviews, filename = name+'.json')

            db = connect_db()
            reviewData = ReviewData(user_id=session['user_id'], product_url=reviewLink, filepath=fileAddress) 
            db.add(reviewData)
            db.commit()
            db.close()

            return jsonify({"status":"success","message":"Product mined successfully"})

            #DEBUGGING HELP: committing changes to SQLite, finding user_id to add to reviewData
            # - Success window is not popping up after data is mined

            # First box: # of reviews limit
            # Second box: File name


#nm in the return statement above is a variable that can be used in html
if __name__ == '__main__':
    app.run(debug = True) # run this server in a testing mode
    
# Tasks
# Clean up UI
# Fill out login information - remove old things that I tested, or make a simple page
# and not remove everything

# Notes
# jsonify: asynchronous (sending chunks of information without reloading the page) sending to form. Handled by JavaScript
# sending tiny bit of data back to server from the client
# Fix the UI on the pages (specifically the front page)