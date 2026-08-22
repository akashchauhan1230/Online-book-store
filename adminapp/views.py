
# pyrefly: ignore [missing-import]
from django.contrib import messages
# pyrefly: ignore [missing-import]
from django.shortcuts import render, redirect
from mainapp.models import *
from .models import *
from userapp.models import *

from decimal import Decimal

# pyrefly: ignore [missing-import]
from django.views.decorators.cache import cache_control

# pyrefly: ignore [missing-import]
from django.db.models import Sum

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def admindash(request):
    if 'adminid' not in request.session:
        messages.error(request, 'You are not logged in.')
        return redirect('adminlogin')
    adminid = request.session.get('adminid')

    user_count = UserInfo.objects.all().count()
    book_count = Book.objects.all().count()
    order_count = Order.objects.all().count()
    category_count = Category.objects.all().count()
    enquiry_count = Enquiry.objects.all().count()
    
    rev_agg = Order.objects.aggregate(total=Sum('total_amount'))
    total_revenue = rev_agg['total'] or 0

    recent_orders = Order.objects.all().order_by('-ordered_at')[:6]

    context = {
        'adminid': adminid,
        'user_count': user_count,
        'book_count': book_count,
        'order_count': order_count,
        'category_count': category_count,
        'enquiry_count': enquiry_count,
        'total_revenue': total_revenue,
        'orders': recent_orders,
    }
        
    return render(request, 'admindash.html', context)


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def adminlogout(request):
    if 'adminid' in request.session:
        del request.session['adminid']
        messages.success(request, 'You have been logged out successfully.')
        return redirect('adminlogin')
    else:
        messages.error(request, 'You are not logged in.')
        return redirect('index')


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewenq(request):
    if 'adminid' not in request.session:
        messages.error(request, 'You are not logged in.')
        return redirect('adminlogin')
    enqs = Enquiry.objects.all()
    return render(request, 'viewenq.html', {'enqs': enqs})



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def delenq(request, id):
    if 'adminid' not in request.session:
        messages.error(request, 'You are not logged in.')
        return redirect('adminlogin')
    enq = Enquiry.objects.filter(id=id)
    if enq.exists():
        enq.delete()
        messages.success(request, 'Enquiry deleted successfully.')
    else:
        messages.error(request, 'Enquiry not found.')
    return redirect('viewenq')



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def delcat(request, id):
    if 'adminid' not in request.session:
        messages.error(request, 'You are not logged in.')
        return redirect('adminlogin')
    cat = Category.objects.filter(id=id)
    if cat.exists():
        cat.delete()
        messages.success(request, 'Category deleted successfully.')
    else:
        messages.error(request, 'Category not found.')
    return redirect('viewcat')



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def adminchangepwd(request):
    if 'adminid' not in request.session:
        messages.error(request, 'You are not logged in.')
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    if request.method == 'POST':
        oldpwd = request.POST.get('oldpwd')
        newpwd = request.POST.get('newpwd')
        confirmpwd = request.POST.get('confirmpwd')
        try:
            admin = LoginInfo.objects.get(username = adminid)
            if admin.password != oldpwd:
                messages.error(request,"Old password is Incorrect")
                return redirect('adminchangepwd')
            elif newpwd !=confirmpwd:
                messages.error(request,"New Password and confirm password do not match")
                return redirect('adminchangepwd')
            elif admin.password==newpwd:
                messages.error(request,"New password is same as old password ")
                return redirect('adminchangepwd')
            else:
                admin.password = newpwd
                admin.save()
                messages.success(request,"Your Password has been change")
            return redirect('adminchangepwd')
        except LoginInfo.DoesNotExist:
            messages.error(request,"something went worng")
            return redirect('adminlogin')
    return render(request,'password.html',{'adminid':adminid})



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def addcat(request):
    if 'adminid' not in request.session:
        messages.error(request, 'You are not logged in.')
        return redirect('adminlogin')
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        cat=Category(name=name, description=description)
        cat.save()
        messages.success(request, 'Category added successfully!')
        return redirect('addcat')
    return render(request, 'addcat.html')




@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewcat(request):
    if 'adminid' not in request.session:
        messages.error(request, 'You are not logged in.')
        return redirect('adminlogin')
    cats = Category.objects.all()
    # attach book count
    for c in cats:
        c.book_count = Book.objects.filter(category=c).count()
    return render(request, 'viewcat.html', {'cats': cats})




@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def addbook(request):
    if 'adminid' not in request.session:
        messages.error(request, 'You are not logged in.')
        return redirect('adminlogin')
    cat = Category.objects.all()
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        category_id = request.POST.get('Category')
        description = request.POST.get('description')
        original_price = request.POST.get('original_price')
        price = request.POST.get('price')
        published_date = request.POST.get('published_date')
        language = request.POST.get('language')
        cover_image = request.FILES.get('cover_image')
        stock = request.POST.get('stock')

        cat = Category.objects.get(id=category_id)
        
        book = Book(
            title=title,
            author=author,
            category=cat,
            description=description,
            original_price=original_price,
            price=price,
            published_date=published_date,
            language=language,
            cover_image=cover_image,
            stock=stock
        )
        book.save()
        messages.success(request, 'Book added successfully!')
        return redirect('addbook')
    return render(request, 'addbook.html',{'cats':cat})



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewbook(request):
    if 'adminid' not in request.session:
        messages.error(request, 'You are not logged in.')
        return redirect('adminlogin')
    books = Book.objects.all()
    return render(request, 'viewbook.html',{'books':books})









@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def adminorder(request):
    if not 'adminid' in request.session:
        messages.error(request,"You are not logged in")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    context = {
        'adminid':adminid,
        'orders' :Order.objects.all().order_by('-ordered_at')     
    }
    return render(request,'adminorder.html',context)
        
                
                
            