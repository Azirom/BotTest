from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_session import Session               ## pip install Flask-Session
import google.oauth2.credentials                ## Used by Google OAuth
import google_auth_oauthlib.flow                ## Used by Google OAuth
from googleapiclient.discovery import build     ## Used by Google OAuth
app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get['GOOGLE_PROVIDER_AUTHENTICATION_SECRET']
app.config['SESSION_TYPE'] = "filesystem"
app.config['SESSION_FILE_DIR'] = os.path.join(app.root_path, "sessions")
app.config['SESSION_FILE_THRESHOLD'] = 1000
Session(app)

@app.route('/')
def main():
    if "credentials" not in session:    ## If not logged in
        return redirect("authorize")    ## Start the login process
    elif "user" in session:             ## If we are logged in return a customised index page
        return render_template("index.html", person=session['user']['name'])
    else:                               ## Else
        return send_file("index.html")  ## This should never be reached?
 
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

if __name__ == '__main__':
   app.run()