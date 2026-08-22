# pyrefly: ignore [missing-import]
from django.shortcuts import render, redirect
# pyrefly: ignore [missing-import]
from django.contrib import messages
from .models import *
import requests
from userapp.models import*
from adminapp.models import*
# pyrefly: ignore [missing-import]
from django.views.decorators.cache import cache_control

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def index(request):
    userid = request.session.get('userid')
    user = None

    if userid:
        user = UserInfo.objects.filter(email=userid).first()
        if user is None:
            request.session.flush()
            messages.error(request, 'Your session has expired. Please login again.')
            return redirect('login')

    context = {
        'userid': userid,
        'books': Book.objects.all()[:10],
        'user': user,
        'profile': user.profile if user else '',
        'name': user.name if user else '',
    }
    return render(request, 'index.html', context)



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def about(request):
    context={
        'userid' :request.session.get('userid'),
        
    }
    return render(request, 'about.html',context)



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def contact(request):
    context={
        'userid' :request.session.get('userid'),
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact_no = request.POST.get('contactno')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        enquiry = Enquiry(name=name, email=email, contact_no=contact_no, subject=subject, message=message)
        enquiry.save()
        

        url = "http://sms.bulkssms.com/submitsms.jsp"
        params = {
            "user": "BRIJESH",
            "key": "066c862acdXX",
            "mobile": f"{contact_no}",
            "message": "Thanks for enquiry we will contact you soon.\n\n-Bulk SMS",
            "senderid": "UPDSMS",
            "accusage": "1",
            "entityid": "1201159543060917386",
            "tempid": "1207169476099469445",
        }

        response = requests.get(url, params=params)
        print("Response:", response.text)

        messages.success(request, 'Your enquiry has been submitted successfully!')
        
        return redirect('contact')    
    return render(request, 'contact.html',context)





@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def register(request):
    context={
        'userid' :request.session.get('userid'),
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contactno = request.POST.get('contactno')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if password != cpassword:
            messages.error(request, "Password and Confirm Password must match.")
            return redirect('register')
        if LoginInfo.objects.filter(username=email).exists() or UserInfo.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered. Please use another email or login.")
            return redirect('register')
        if UserInfo.objects.filter(contactno=contactno).exists():
            messages.error(request, "Contact number is already registered. Please use a different contact number.")
            return redirect('register')
        try:
            log = LoginInfo(usertype="user", username=email, password=password)
            log.save()
            user = UserInfo(name=name, email=email, contactno=contactno, login=log)
            user.save()
            messages.success(request, "Registration is done successfully! Please log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Registration error: {str(e)}")
            return redirect('register')
    return render(request, 'register.html', context)



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = LoginInfo.objects.get(usertype="user",username=username,password=password)
            if user is not None:
                request.session['userid'] = username
                messages.success(request,"Welcome User")
                return redirect('index')
        except LoginInfo.DoesNotExist:
            messages.error(request,"Invalid username or password")
            return redirect('login')
    return render(request, 'login.html')




@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def category(request):
    cats = Category.objects.all()
    books = Book.objects.all()
    q = request.GET.get('q', '').strip()
    selected_cat = request.GET.get('cat', '').strip()

    if q:
        books = books.filter(title__icontains=q) | books.filter(author__icontains=q) | books.filter(description__icontains=q)
    if selected_cat:
        books = books.filter(category__id=selected_cat)

    context = {
        'userid': request.session.get('userid'),
        'categories': cats,
        'books': books,
        'selected_cat': selected_cat,
        'q': q,
    }
    return render(request, 'category.html', context)

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            ad = LoginInfo.objects.get(username=username, password=password)
            if ad is not None:
                request.session['adminid'] = ad.username
                messages.success(request, 'Welcome Admin!')
                return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request, 'Invalid credentials or user type.')
            return redirect('adminlogin')
    return render(request, 'adminlogin.html')



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def book_details(request,id):
    context={
        'userid' :request.session.get('userid'),
        'book':Book.objects.get(id=id)
    }
    return render(request, 'book_details.html',context )
