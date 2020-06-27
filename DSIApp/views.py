from django.shortcuts import render , redirect
from DSIApp.models import Student
from DSIApp.forms import StudentForm, LogForm
from django.contrib import messages
from pymongo import MongoClient
from ecdsa import SigningKey, NIST521p, VerifyingKey, BadSignatureError
from django.core.files.storage import FileSystemStorage
# Create your views here.

n = ''

def log_view(request):
    
    if request.method == 'POST':
        log_form = LogForm(request.POST)
        myclient = MongoClient("mongodb+srv://dsiuser:drdo@cluster0-7hfqh.mongodb.net/DSIDATA?retryWrites=true&w=majority")
        username1 = request.POST['Username']
        password1 = request.POST['Password']
        mydb = myclient["DSIDATA"]
        mycol = mydb["DSIApp_student"]
        myquery = { "Name": username1,"Pass":password1 }
        mydoc = mycol.find(myquery) 
        
        for x in mydoc:
            global n
            n = x['Name']
            return redirect("/upload")          
    else:
        log_form = LogForm()
    return render(request,'users/loginbase.html',{'log_form': log_form})   
    
def form_view(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            password1 = request.POST['Pass']
            password2 = request.POST['Re_Pass']
            if password1 != password2:
                return redirect('/')
            else:
                form.save()        
        return redirect('login')
    else:
        form = StudentForm()    
    return render(request,'users/home.html',{'form':form})        

def upload_view(request):
    context = {'a':n}
    if request.method == "POST" and 'sbutton' in request.POST:
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)

    if request.method == "POST" and 'ebutton' in request.POST:
        uploaded_file = request.FILES['document']
        sk = SigningKey.generate(curve=NIST521p)
        vk = sk.verifying_key
        with open("EncryptCode/private.pem", "wb") as f:
            f.write(sk.to_pem())
        with open("EncryptCode/public.pem", "wb") as f:
            f.write(vk.to_pem())

        with open("EncryptCode/private.pem") as f:
            sk = SigningKey.from_pem(f.read())
            message = uploaded_file.read()
        sig = sk.sign(message)
        with open("EncryptCode/signature", "wb") as f:
            f.write(sig)   

    if request.method == "POST" and 'vbutton' in request.POST:
        uploaded_file = request.FILES['document']
        message = uploaded_file.read()
        vk = VerifyingKey.from_pem(open("EncryptCode/public.pem").read())
        with open("EncryptCode/signature", "rb") as f:
            sig = f.read()
        try:
            vk.verify(sig, message)
            print ("good signature")
            messages.success(request, "Good Signature")
        except BadSignatureError:
            print ("BAD SIGNATURE")
            messages.success(request, "Bad Signature")

    if request.method == "POST" and 'lbutton' in request.POST:
        return redirect("login")        
    return render(request,'work/upload.html', context)    
  