from django.shortcuts import render
import pyrebase


firebaseConfig = {
    'apiKey': "AIzaSyApZfa0yIaEgQarVcwjbZcXRGVU-0j-XV4",
    'authDomain': "webassignment-671ec.firebaseapp.com",
    'databaseURL': "https://webassignment-671ec-default-rtdb.asia-southeast1.firebasedatabase.app/",
    'projectId': "webassignment-671ec",
    'storageBucket': "webassignment-671ec.appspot.com",
    'messagingSenderId': "593673221556",
    'appId': "1:593673221556:web:e71d1673bdfaeb34022ee1",
    'measurementId': "G-HE3MPS1CPZ"
}

# Initialising database,auth and firebase for further use
firebase = pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()
db = firebase.database()


def signIn(request):
    return render(request, "Login.html")


def home(request):
    print(request)
    return render(request, "Home.html")


def postsignIn(request):
    email = request.POST.get('email')
    pasw = request.POST.get('pass')
    try:
        # if there is no error then signin the user with given email and password
        user = authe.sign_in_with_email_and_password(email, pasw)
    except:
        message = "Invalid Credentials!!Please ChecK your Data"
        return render(request, "Login.html", {"message": message})
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, "Home.html", {"email": email, "uid": user['idToken'],})


def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request, "Login.html")


def signUp(request):
    return render(request, "Registration.html")


def postsignUp(request):
    email = request.POST.get('email')
    passs = request.POST.get('pass')
    name = request.POST.get('name')

    try:
        # creating a user with the given email and password
        user = authe.create_user_with_email_and_password(email, passs)
        print(user)
        message = "Your signed up successfully!!"
        data = {
            'name': name,
            'email': email,
        }
        result = db.child("users").push(data,user['idToken'])
        return render(request, "Login.html", {"msg": message})
    except:
        return render(request, "Registration.html")



def reset(request):
    return render(request, "Reset.html")


def postReset(request):
    email = request.POST.get('email')
    try:
        authe.send_password_reset_email(email)
        message = "A email to reset password is successfully sent"
        return render(request, "Reset.html", {"msg": message})
    except:
        message = "Something went wrong, Please check the email you provided is registered or not"
        return render(request, "Reset.html", {"msg": message})
