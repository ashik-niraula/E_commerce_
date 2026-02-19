from django.shortcuts import render,redirect,get_object_or_404
from e_auth.forms import UserRegistration , AddressForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login , logout ,aauthenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from e_auth.utils import send_otp 
from django.core.cache import cache
from e_auth.models import Profile , Vendor , Customer , Address,User
from main.models import Order ,ShippingOption , OrderItem
from django.db.models import Q
# Create your views here.
def signup_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = UserRegistration()    
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            role = request.POST.get('role')
            is_seller = request.POST.get('seller')
            if role == 'customer':
                request.session['acc_type'] = 'customer'
            if role == 'vendor':
                request.session['acc_type'] = 'vendor'    
            email = form.cleaned_data['email']
            request.session['email'] = email
            request.session['signup_data'] = request.POST
            send_otp(email)
            return redirect('otpverify')
    context = {'form': form}
    return render(request, 'auth/signup.html', context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = AuthenticationForm()    
    if request.method == "POST":
        form = AuthenticationForm(request,data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    context = {'form':form}        
    return render(request,'auth/login.html',context)

@login_required(login_url="login")
def logout_page(request):
    logout(request)
    return redirect('home')

def verify_otp(request):
    email = request.session.get('email')
    signup_data = request.session.get('signup_data')
    acc_type = request.session.get('acc_type')

    if not email or not signup_data:
        messages.error(request, "Something went wrong")
        return redirect('signup')

    if request.method == "POST":
        otp = request.POST.get('otp')
        saved_otp = cache.get(email)
       
        if not saved_otp:
            messages.error(request, "OTP expired ❌")
            return redirect('otpverify')
        if str(otp) == str(saved_otp):
            form = UserRegistration(signup_data)

            if form.is_valid():
                user = form.save()
                if acc_type == "customer":
                    profile = Profile.objects.create(user=user)
                if acc_type == 'vendor':
                    profile = Profile.objects.create(user=user,is_costomer=False,is_vendor=True)     
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                # cleanup
                cache.delete(email)
                del request.session['signup_data']
                del request.session['email']

                return redirect('home') 
            else:
                messages.error(request, "Invalid Credintials")
                return redirect('signup')

        messages.error(request, "Invalid OTP ❌")

    return render(request, "auth/verify_otp.html", {"email": email})

@login_required(login_url='login')
def user_detail_page(request):
    form = AddressForm()
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.profile = request.user.profile.first()
            address.save()
            return redirect('user_profile',request.user.username)
        else:
            return redirect('add_address')
    return render(request,'auth/user_form.html',{'form':form})        

@login_required(login_url='login')
def edit_address(request, pk):
    address = get_object_or_404(Address, pk=pk, profile__user=request.user)

    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('user_profile', request.user.username)
    else:
        form = AddressForm(instance=address)

    return render(request, 'auth/user_form.html', {'form': form})


@login_required(login_url="login")
def user_profie(request,username):
    user = get_object_or_404(User,username=username)
    profile, created = Profile.objects.get_or_create(user=user)
    customer = get_object_or_404(Customer,profile=profile)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    shipping = ShippingOption.objects.all()
    
    if request.method == "POST" :
        data = request.POST  
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.save()

        profile.phonenumber = data.get('phone_number')
        profile.bio = data.get('bio')
        profile.save()
        return redirect('user_profile',user.username)
    address = None
    if Address.objects.filter(profile=profile).exists():
        address = Address.objects.filter(profile=profile)
    
    context = {
        'customer':customer,
        'orders':orders[:5],
        'shipping_options': shipping,
        "addresses": address,
        "total_orders_count": orders.filter(
            Q(status="PAID")|
            Q(status="Delevired")
        ).count()
    }

    return render(request,'auth/user_profile.html',context)    

@login_required(login_url="login")
def user_orders(request):
    customer = get_object_or_404(Customer,profile__user = request.user)
    orders = Order.objects.filter(user = request.user).exclude(status="DELETED").order_by('-created_at')

    transit = orders.filter(status="PAID").count()
    delevired = orders.filter(status="SHIPPED").count()
    pending = orders.filter(status="PENDING").count()

    context = {
        'customer':customer,
        'orders': orders,
        'transit': transit,
        'pending': pending,
        'delevired': delevired
    }
    return render(request,'auth/orders.html',context)

@login_required(login_url="login")
def user_order_detail(request,order_id):
    order = get_object_or_404(Order,id= order_id)
    if not order.user == request.user:
        redirect('logout')
    profile = request.user.profile.first()
    orderitem = OrderItem.objects.filter(order=order)    
    context = {
        'orderitem': orderitem,
        'profile': profile,
        'order': order,
        'sub_total': sum(item.get_total() for item in orderitem.all()),
    }    
    return render(request,'auth/order_detail.html',context)
