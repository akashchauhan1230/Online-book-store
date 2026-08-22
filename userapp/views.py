# pyrefly: ignore [missing-import]
from django.shortcuts import render,redirect
# pyrefly: ignore [missing-import]
from django.contrib import messages
from mainapp.models import *
from adminapp.models import*
from .models import*
# pyrefly: ignore [missing-import]
import stripe
# pyrefly: ignore [missing-import]
from django.conf import settings
# pyrefly: ignore [missing-import]
from django.views.decorators.csrf import csrf_exempt
# pyrefly: ignore [missing-import]
from django.http import JsonResponse
stripe.api_key = settings.STRIPE_SECRET_KEY


# pyrefly: ignore [missing-import]
from django.core.mail import send_mail
# pyrefly: ignore [missing-import]
from django.views.decorators.cache import cache_control
# Create your views here.


def get_logged_in_user(request, message="You are not logged in"):
    userid = request.session.get('userid')
    if not userid:
        messages.error(request, message)
        return None, redirect('login')

    user = UserInfo.objects.filter(email=userid).first()
    if user is None:
        request.session.flush()
        messages.error(request, 'Your session is invalid. Please login again.')
        return None, redirect('login')

    return user, None


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def userdash(request):
    user, redirect_response = get_logged_in_user(request)
    if redirect_response is not None:
        return redirect_response

    userid = request.session.get('userid')
    
    # Live cart items count
    cart = Cart.objects.filter(user=user).first()
    cart_count = CartItem.objects.filter(cart=cart).count() if cart else 0
    
    # Live orders
    order_count = Order.objects.filter(user=user).count()
    recent_orders = Order.objects.filter(user=user).order_by('-ordered_at')[:4]

    context = {
        'user': user,
        'userid': userid,
        'profile': user.profile,
        'cart_count': cart_count,
        'order_count': order_count,
        'orders': recent_orders,
    }
    return render(request, 'userdash.html', context)



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def userlogout(request):
    if 'userid' in request.session:
        del request.session['userid']
        messages.success(request,'You are logged out')
        return redirect('login')
    else:
        return redirect('index')
    
    
    
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def viewcart(request):
    user, redirect_response = get_logged_in_user(request)
    if redirect_response is not None:
        return redirect_response

    userid=request.session.get('userid')
    ucart = Cart.objects.filter(user = user).first()
    if ucart is None:
        cart = Cart(user=user)
        cart.save()
    items=CartItem.objects.filter(cart=Cart.objects.filter(user = user).first())
    total = 0
    for i in items:
        total = total + i.get_total_price()
    context={
        'user': user,
        'name': user.name,
        'userid': userid,
        'profile': user.profile,
        'items': items,
        'total': total
    }
    return render(request,'viewcart.html',context)



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def addtocart(request,id):
    user, redirect_response = get_logged_in_user(request)
    if redirect_response is not None:
        return redirect_response

    ucart = Cart.objects.filter(user = user).first()
    if ucart is None:
        cart = Cart(user=user)
        cart.save()
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        if quantity is None:
            quantity =1
        book = Book.objects.get(id=id)
        ci = CartItem(cart = Cart.objects.filter(user=user).first(), book=book ,quantity=quantity)
        ci.save()
        messages.success(request,"Book added to cart")
        return redirect('viewcart')
    else:
        return redirect('index')



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def removeitem(request,id):
    user, redirect_response = get_logged_in_user(request)
    if redirect_response is not None:
        return redirect_response

    ucart = Cart.objects.filter(user = user).first()
    book = Book.objects.get(id=id)
    CartItem.objects.filter(cart=ucart,book=book).delete()
    messages.success(request,"Book removed from cart")
    return redirect('viewcart')






@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def checkout(request):
    user, redirect_response = get_logged_in_user(request)
    if redirect_response is not None:
        return redirect_response

    cart = Cart.objects.get(user=user)
    items = CartItem.objects.filter(cart=cart)

    line_items = []

    for item in items:
        line_items.append({
            'price_data': {
                'currency': 'inr',
                'unit_amount': int(item.book.price * 100),
                'product_data': {
                    'name': item.book.title,
                },
            },
            'quantity': item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card', 'sepa_debit'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/userapp/payment-success/'),
        cancel_url=request.build_absolute_uri('/viewcart/'),
    )

    return redirect(session.url, code=303)

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def payment_success(request):
    user, redirect_response = get_logged_in_user(request, message='Please login first.')
    if redirect_response is not None:
        return redirect_response

    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            messages.warning(request, "No items found in your cart.")
            return redirect('index')

  
        total_amount = sum(item.get_total_price() for item in cart_items)
        order = Order.objects.create(user=user, total_amount=total_amount)

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price,
            )

       
        cart_items.delete()

        items = OrderItem.objects.filter(order=order)

        # Add total_price attribute to each item
        for item in items:
            item.total_price = item.quantity * item.price
            
        subject = "Order Confirmation"
        msg =f"Dear{user.name},\n\nThank you  ordering book from Our application "
        
        try:
            send_mail(
                subject=subject,
                messages= msg,
                recipient_list ={f"{user.email}"},
                from_email='Reader hub',
                fail_silently =True
                
            )
            messages.success(request,"Payment Successfull ! Your order has been placed.")
            return render(request,'payment_success.html',{'order':order, 'user': user, 'userid': user.email})
        except:
            messages.success(request,"Payment Successfull ! Your order has been placed. but mail cannot send ")
            return render(request,'payment_success.html',{'order':order, 'user': user, 'userid': user.email})
    except Cart.DoesNotExist:
        messages.error(request,"Card not found")
        return redirect('index')



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def userorders(request):
    user, redirect_response = get_logged_in_user(request)
    if redirect_response is not None:
        return redirect_response

    userid = request.session.get('userid')
    orders = Order.objects.filter(user=user)
    order_items = []
    for o in orders:
        order_items.append(OrderItem.objects.filter(order=o))
    
    context = {
        'user': user,
        'name': user.name,
        'userid': userid,
        'profile': user.profile,
        'order_items': order_items
    }
    return render(request, 'userorders.html', context)



@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def userprofile(request):
    user, redirect_response = get_logged_in_user(request)
    if redirect_response is not None:
        return redirect_response

    userid = request.session.get('userid')
    context = {
        'user': user.name,
        'userid': userid,
        'profile': user.profile,
        'user':user,
        'address':user.address,
    }

    return render(request,'userprofile.html',context)




@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def editprofile(request):
    user, redirect_response = get_logged_in_user(request)
    if redirect_response is not None:
        return redirect_response

    userid = request.session.get('userid')
    context = {
        'user': user.name,
        'userid': userid,
        'profile': user.profile,
        'user':user
    }
    if request.method == 'POST':
        name =request.POST.get('name')
        contactno =request.POST.get('contactno')
        address =request.POST.get('address')
        profile =request.FILES.get('profile')
        user.name = name
        user.contactno =contactno
        user.address = address
        if profile:
            user.profile = profile
        user.save()
        messages.success(request,'Profile updated successfully')
    return render(request,'editprofile.html',context)



