from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .models import Customer
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from datetime import datetime
from .models import Item,Category
from django.contrib.auth.password_validation import validate_password
from  django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.
@login_required(login_url='log_in')
def index(request):
    data=Item.objects.all()
    cate=Category.objects.all()
    cateid=request.GET.get('category')
    if cateid:
        data=Item.objects.filter(category=cateid)
    else:
        data=Item.objects.all()
   
  
    if request.method == 'POST': 
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Save customer data
        Customer.objects.create(name=name, email=email, phone=phone, message=message)

        # Prepare email
        subject = 'Thank you for contacting us'
        email_message = render_to_string('restaurantapp/msg.html', {'name': name ,'date':datetime.now})
        from_email = 'rojikc764@gmail.com'
        recipient_list = [email] 

        try:
            email_msg = EmailMessage(subject, email_message, from_email, to=recipient_list)
            email_msg.content_subtype = "html" 
            email_msg.send(fail_silently=True)

            messages.success(request, f"Hi {name}, your form has been successfully submitted. Please check your email for confirmation!")
            return redirect('index')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('index') 
    context= {
        'data':data,
        'cate':cate
        }

    return render(request, 'restaurantapp/index.html',context)
 

def about(request):
    return render(request,'restaurantapp/about.html')


def contact(request):
   if request.method == 'POST': 
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Save customer data
        Customer.objects.create(name=name, email=email, phone=phone, message=message)

        # Prepare email
        subject = 'Thank you for contacting us'
        email_message = render_to_string('restaurantapp/msg.html', {'name': name ,'date':datetime.now})
        from_email = 'rojikc764@gmail.com'
        recipient_list = [email] 

        try:
            email_msg = EmailMessage(subject, email_message, from_email, to=recipient_list)
            email_msg.content_subtype = "html" 
            email_msg.send(fail_silently=True)

            messages.success(request, f"Hi {name}, your form has been successfully submitted. Please check your email for confirmation!")
            return redirect('contact')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('contact')

   return render(request, 'restaurantapp/contact.html')

@login_required(login_url='log_in')

def menu(request):
    return render(request,'restaurantapp/menu.html')

def services(request):
    return render(request,'restaurantapp/services.html')


def privacy(request):
    return render(request,'restaurantapp/privacy.html')

def policy(request):
    return render(request,'restaurantapp/policy.html')

def terms(request):
    return render(request,'restaurantapp/terms.html')

def support(request):
    return render(request,'restaurantapp/support.html')







'''=====Authentication part starts here======'''
def register(request):
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        if password == password1:

           try: 
                validate_password(password)
                if User.objects.filter(username=username).exists():
                    messages.error(request,"Username already exists!")
                    return redirect('register')
                if User.objects.filter(email=email).exists():
                    messages.error(request,"Email already exists!")
                    return redirect('register')
                error=[]
                if not re.search(r'[A-Z]',password):
                    error.append("Password should be at least one uppercase")
                if not re.search(r'\d',password):
                    error.append("Password should contain at least one digit")
                if not re.search(r'[!@#$%^&*()]',password):
                    error.append("Password should contain at least one special character!")
                if error:
                    for i in error:
                        messages.error(request,i)
                    return redirect('register')
                else:
                    User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password) 
                    messages.success(request, "Registered Successfully!!")
                    return redirect('register')
           except ValidationError as e:
               for error in e.messages:
                   messages.error(request,error)
                   return redirect('register')
        else:
            messages.error(request, "Your password and confirm password don't match.")
            return redirect('register')

    return render(request, 'auth/register.html')



def log_in(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        remember_me=request.POST.get('remember_me')
        if not User.objects.filter(username=username).exists():
          messages.error(request,"Username is not registered!")
          return redirect('log_in')   
        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            if remember_me:
                request.session.set_expiry(120000)
            else:
                request.session.set_expiry(0)

                next=request.POST.get('next','')
                return redirect(next if next else 'index')
    next=request.GET.get('next','')


    return render(request,'auth/login.html',{'next':next})


def log_out(request):
    logout(request)
    return redirect('log_in')

@login_required(login_url='log_in')
def change_password(request):
    form=PasswordChangeForm(user=request.user)

    if request.method=='POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
         form.save()
         return redirect('log_in')
    return render(request,'auth/change_password.html',{'form':form})


