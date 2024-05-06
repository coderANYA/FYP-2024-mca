from flask import Flask, render_template,redirect,request,flash,session
from database import User, add_to_db, File, open_db

#file upload
from werkzeug.utils import secure_filename   # This library is used for uploading files in Flask & also cleans your file name
from common.file_utils import *
from common.helper import *
import numpy as np

app = Flask(__name__)       # flask setting
app.secret_key = 'thisissupersecretkeyfornone'  # secret key is required for running sessions

class_names = ['fake', 'real']

# Routes = Addresses will be made so that the user can visit them 

# default first page (HOME/INDEX PAGE) which the user will visit
@app.route('/')
def index():
    return render_template('index.html')

# second page (LOGIN PAGE)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email:
            if password:
                print("Email =>", email)
                print("Password =>", password)
                try:
                    db = open_db()
                    user = db.query(User).filter_by(email=email,password=password).first()
                    print(user)
                    if user:
                        session['isauth'] = True
                        session['email'] = user.email
                        session['id'] = user.id
                        del db
                        flash('Login Successful','success')
                        return redirect('/')
                    else:
                        flash('email or password is wrong','danger')
                except Exception as e:
                    flash(e,'danger')
                    print(e)
            else:
                print("error")
        else:
            print('email error')
    return render_template('login.html')

# third page (REGISTER PAGE)
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        print(username,email,password,cpassword)

        if len(username) == 0 or len(email) == 0 or len(password) == 0 or len(cpassword) == 0:
            flash("All fields are required", 'danger')
            return redirect('/register') # reload the page
        user = User(username = username, email = email, password = password)
        try:add_to_db(user)
        except Exception as e:
            flash("error: contact admin",'danger')
    return render_template('register.html')

# fourth page (FILE UPLOADING PAGE)
@app.route('/file/upload', methods = ['GET','POST'])
def file_upload():
    if request.method == 'POST':
        file = request.files['file']
        name = secure_filename(file.filename)
        path = upload_file(file, name)
        file = File(path = path, user_id = 1)
        add_to_db(file)
        flash("File uploaded successfully", 'success')
    return render_template('upload.html')

# fifth page (DISPLAY_LIST PAGE)
@app.route('/file/list', methods= ['GET','POST'])
def file_list():
    db = open_db()
    files = db.query(File).all()
    return render_template('display_list.html', files = files)

# sixth page (VIEW_FILE PAGE)
# 127.0.0.1:8000/file/4/view
@app.route('/file/<int:id>/view/')      # <int:id> means dynamic path
def file_view(id):
    db = open_db()
    file = db.query(File).get(id)
    return render_template('view_file.html', file=file)

# deleting an item from the display list
@app.route('/delete/<int:id>')
def delete_item(id):
    try:
        db = open_db()
        file = db.query(File).get(id)
        try:os.remove(os.path.join(os.getcwd(),file.path))
        except:print('file not exist')
        finally: 
            db.delete(file)
        db.commit()
        db.close()
    except Exception as e:
        print('error finding object', e)
    return redirect('/file/list')

# seventh page (ABOUT)
@app.route('/about')
def about():
    #code
    return render_template('about.html')

# LogOut
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# load model
# detect
@app.route('/detect/<int:id>')
def detect_forgery(id):
    db =  open_db()
    img = db.query(File).get(id)
    path = img.path
    if os.path.exists(path):
        image = prepare_image(path)
        image = image.reshape(-1, 128, 128, 3)
        model = load_my_model('models\model_casia_run1.h5')
        print('model loaded')
        y_pred = model.predict(image)
        y_pred_class = np.argmax(y_pred, axis=1)[0]
        cls = class_names[y_pred_class]
        conf  = np.amax(y_pred)*100
        if y_pred_class == 0:
            try:
                os.makedirs('static/ela', exist_ok=True)
                ela_path = f'static/ela/{img.id}.png'
                convert_to_ela_image(path, 91).save(ela_path)
                # coords = find_manipulated_region(ela_path)
                # modify_boundary = make_pixels_white(ela_path, coords)
                # os.makedirs('static/modified', exist_ok=True)
                # modified_path = f'static/modified/{img.id}.png'
                # modify_boundary.save(modified_path)
                return render_template('result.html', img = img, cls = cls, conf = conf, ela_path = ela_path)
            except Exception as e:
                print(e)
        return render_template('result.html', img = img, cls = cls, conf = conf)
    else:
        flash('file not found','danger')
    return redirect('/file/list')

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 