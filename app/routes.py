import files_sdk
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from app import app, db
from werkzeug.urls import url_parse
from waitress import serve

import os
from datetime import date, datetime
from app.forms import LoginForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
import re
import psutil
p = psutil.Process()
p.memory_info()


today = str(date.today())
api_key = os.environ.get("API_KEY")
#login to Files.com
files_sdk.set_api_key(api_key)
list_obj = files_sdk.list_for('/')


def getFileNumbers(list_obj):

    dir_dict = {}
    directories = []
    
    #get directories

    for f in list_obj.auto_paging_iter():
        if "LOA" in f.path.upper():
            directories.append(f.path)
          
 
    #get file numbers in directories
    for dir in directories:
       
   
        dir_obj = files_sdk.list_for(dir)
        count = 0
        today_count = 0
        no_files = []
       
        
        for file in files_sdk.folder.list_for(dir,{"per_page": 1000}).auto_paging_iter():    
            count += 1

            #get files uploaded today
            today_file = file.mtime[0:10]
                    
            if today_file == today:
                today_count += 1


        print(count)
        no_files.append(count)
        no_files.append(today_count)
        dir_dict[dir] = no_files
        

    
    return dir_dict



@app.route('/')
@app.route('/index')
@login_required
def index():    
    
    p = psutil.Process()
    print(p.memory_info())


    return render_template('index.html', dir_dict = getFileNumbers(list_obj))


@app.route('/login', methods=['GET', 'POST'])
def login():
    errors=[]
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            
            errors.append('Invalid username or password')
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form, errors=errors)


def main():
    pass


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))




if __name__ == "__main__":
    peint('starts here')
    serve(app, host='0.0.0.0', port=8000)
    
