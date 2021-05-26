from flask import Flask, render_template, session, url_for, request, redirect, current_app, send_from_directory, flash
from flask_pymongo import PyMongo
import bcrypt
import subprocess
import os
from werkzeug.utils import secure_filename

import audio_converter 
#from user import routes

app = Flask(__name__)

#app.config['MONGO_DBNAME'] = "pym-user"
app.config['MONGO_URI'] = 'mongodb+srv://dbUser:bfh-project@cluster0.vzr4j.mongodb.net/pym-user?retryWrites=true&w=majority'

uploads_dir = os.path.join(app.instance_path, 'uploads')
uploads_directory = str(r"C:\1. Work and Academics\work\flask_projects\Post-your-Music\uploads")
downloads_directory = str(r"C:\1. Work and Academics\work\flask_projects\Post-your-Music\output")
app.config['UPLOAD_FOLDER'] = uploads_directory
app.config['DOWNLOAD_FOLDER'] = downloads_directory

#client = pymongo.MongoClient("mongodb+srv://dbUser:bfh-project@cluster0.vzr4j.mongodb.net/pym-user?retryWrites=true&w=majority")
#db = client.test

#connector
mongo = PyMongo(app)


@app.route('/')
def index():

    if 'email' in session:
        #return('You are logged in as ' + session['email'])
        return render_template('index.html')
    return render_template('login.html')
    #return redirect(url_for('login'))



@app.route('/login', methods=['POST'])
def login():

    users = mongo.db.user
    #print(users)
    login_user =users.find_one({'mail': request.form['email']})

    if login_user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['passwd'].encode('utf-8')) == login_user['passwd'].encode('utf-8'):
            session['email'] = request.form['email']
            session['loggedin'] = True
            return redirect(url_for('index'))

    return 'Invalid username/mail or password combination'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        users = mongo.db.user
        existing_user = users.find_one({'email': request.form['email']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'mail': request.form['email'], 'passwd': hashpass})
            session['email'] = request.form['email']
            session['loggedin'] = True
            return redirect(url_for('index'))
        return 'User already exist!'
    return render_template('login.html')



@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'Choose file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['Choose file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            #mongo.save_file(filename, file)
            mongo.db.user.insert({'audio': filename, 'audio_file': file})
            print("successfully stored in db")
            #file.save(os.path.join(uploads_dir, filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("successfully stored in upload")
            #session['audio'] = file
            session['filename'] = filename
            #app.add_url_rule("/uploads/<name>", endpoint="download_file", build_only=True)

            # now that the file has been saved I need to process it
            #remove_silence(file.filename)
    #return render_template('index.html')
    return redirect(url_for('convert_and_download'))


'''from werkzeug.middleware.shared_data import SharedDataMiddleware
app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})
'''


@app.route('/download', methods=['POST', 'GET'])
def convert_and_download():
    #filename = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    #filename = request.form['Choose file']
    filename = str(session['filename'])
    #file_path = uploads_directory + str('\\') + filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(file_path)
    video = audio_converter.Generate_video.generate_video(file_path, filename)
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename=video, as_attachment=True)



@app.route('/logout')
def logout():
    session.pop('loggedin', False)
    session.pop('email', None)
    session.pop('password', None)
    return redirect(url_for('login'))
    
    
if __name__ == '__main__':
    app.secret_key = 'secretivekeyagain'
    app.run(debug=True)