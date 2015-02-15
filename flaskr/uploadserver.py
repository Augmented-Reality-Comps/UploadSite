# all the imports
import sqlite3
import os
import datetime
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from werkzeug import secure_filename
from datasource import DataSource
import config

app = Flask(__name__)
app.config.from_object(config.ProductionConfig)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route('/')
def index():
    return '<h1>Index</h1><h2>By Michael and Richard</h2><a href="/upload">Uploads</a><br/><a href="/uploadLabel">Upload Labels</a>'

@app.route('/uploadsuccess')
def uploadsuccess():
    return render_template('uploadsuccess.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET', 'POST'])
def upload_site():
    if request.method == 'POST':
        file = request.files['collada']
        latitude = float(request.form['latitude']) * 111000
        longitude = float(request.form['longitude']) * 79000
        if file and allowed_file(file.filename):
            #uploading the file
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #inserting into the database
            db = DataSource()
            database = 'demo'
            query = 'insert into '+database+'(lat, long, alt, file) values ('+str(latitude)+', '+str(longitude)+', 20, \''+filename+'\');'
            db.doData(query, True)

            return redirect(url_for('uploadsuccess'))
        return '<h1>Failure</h1>'
    else:
        return render_template('upload.html')

@app.route('/uploadLabel', methods=['GET', 'POST'])
def upload_label():
    if request.method == 'POST':
        
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        label = str(request.form['label'])

        #inserting into the database
        db = DataSource()
        database = 'labels'
        query = 'insert into '+database+'(lat, long, label) values ('+str(latitude)+', '+str(longitude)+', \''+str(label)+'\');';
        db.doData(query, True)

        return redirect(url_for('uploadsuccess'))
    else:
        return render_template('uploadLabel.html')

if __name__ == '__main__':
    app.run(debug=True)
