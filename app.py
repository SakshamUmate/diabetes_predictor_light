import pickle
import os
from flask import Flask, render_template, request
import pymongo


uri = "mongodb+srv://saksham:qk70nd97a@cluster1.vucvhcs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"

app = Flask(__name__)
app.secret_key='saksham'
client = pymongo.MongoClient(uri)
db = client["diabetes"]
collection =db['login']

global Login
Login=False
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "GET":  
        return render_template('login.html')
    else:
        try:
            email=request.form.get("username")
            password=request.form.get("password")
            
            
            
            pas=collection.find_one({'username':email})
            if pas:
                passs=pas['password']
            if pas and passs==password:
                # session['username'] = email
                # flash('Login successful!', 'success')
                # Login = True
                return render_template('predict.html')
            else:
                return render_template('register.html')
            
        except Exception as e:
            return f'\U0001F613 \U0001F647 Error:{e}'   



@app.route('/register',methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        try:
            email=request.form.get("username")
            password=request.form.get("password")
            
            
            
            pas=collection.find_one({'username':email})
            if pas:
                passs=pas['password']
            if pas and passs==password:
                # Login=True
                return render_template('predict.html')
            else:
                collection.insert_one({'username':email,'password':password})   
                return render_template('predict.html')
            
        except Exception as e :
            return f'\U0001F613 \U0001F647 Error:{e}' 
    

@app.route('/predict',methods=['GET','POSt'])
def predict():
    if request.method == "GET":
        if Login:
            return render_template('predict.html')
        else:
            return render_template('login.html')
    else:
        try:
            preg=float(request.form.get("Pregnancies"))
            glucose=float(request.form.get("Glucose"))
            bp=float(request.form.get("BloodPressure"))
            skin=float(request.form.get("SkinThickness"))
            insulin=float(request.form.get("Insulin"))
            bmi=float(request.form.get("BMI"))
            dpf=float(request.form.get("DiabetesPedigreeFunction"))
            age=float(request.form.get("Age"))
            
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(current_dir, 'models', 'svc.pkl')
            scaler_path = os.path.join(current_dir, 'models', 'scaler.pkl')
            model = pickle.load(open(model_path, 'rb'))
            scaler = pickle.load(open(scaler_path, 'rb'))
            

            
            result=model.predict(scaler.transform([[preg, glucose, bp, skin, insulin, bmi, dpf, age]]))
            
            return render_template('predict.html',result=result)
        except Exception as e:
            return f'\U0001F613 \U0001F647 Error:{e}'
        




if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)