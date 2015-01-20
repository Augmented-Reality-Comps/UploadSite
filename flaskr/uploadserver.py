# all the imports
import sqlite3
import os
import datetime
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from werkzeug import secure_filename
import config
from datasource import DataSource

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route('/')
def index():
    return '<h1>Index</h1><h2>By Michael and Richard</h2><a href="/upload">Uploads</a>'

@app.route('/uploadsuccess')
def uploadsuccess():
    return render_template('uploadsuccess.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_site():
    if request.method == 'POST':
        #do_the_upload()
        file = request.files['collada']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        if file and allowed_file(file.filename):
            filename = latitude + "_" + longitude + '_' + datetime.datetime.now().strftime("%M_%S_%B_%d_%Y") + '_' + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploadsuccess'))
        return '<h1>Failure</h1>'
    else:
        return render_template('upload.html')

@app.route('/db')
def testDBConnection():
    query = 'select * from test4'
    db = DataSource()
    file = db.doData(query, False)
    return '<h1>Index</h1><h2>'+str(file)+'</h2><a href="/upload">Uploads</a>'

@app.route('/db2')
def addFileToDatabase():#file, lat, long):
    lat = 35
    long = 15
    query = 'insert into test4 (lat, long, alt, file) values ('+str(lat)+', '+str(long)+', 19, \'test.txt\');'
    print query
    #query = 'select * from test4'
    db = DataSource()
    output = db.doData(query, True)
    return '<h1>Index</h1><h2>'+str(output)+'</h2><a href="/upload">Uploads</a>'

if __name__ == '__main__':
    app.run(debug=True)
