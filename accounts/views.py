from django.shortcuts import render , HttpResponse , redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages , auth
from django.contrib.auth.decorators import login_required
#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.
from carts.models import Cart , CartItem
from carts.views import _cart_id

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = Account.objects.create_user(first_name = first_name , last_name = last_name ,username = username , email = email , password = password)
            user.phone_number = phone_number
            user.save()

            #User Activation
            current_site = get_current_site(request)
            mail_subject = 'Please Activate your account'
            message = render_to_string('user/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject , message , to=[to_email])
            send_email.send()
            # messages.success(request , 'Thank you for your registration , We have sent a verification to your email address.')
            return redirect('/accounts/signin/?command=verification&email=' + email)
    else:
        form = RegistrationForm()

    context = {
        'form':form
    }
    return render(request, 'user/register.html',context)

def activate(request , uidb64 , token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode() #get user id
        user = Account._default_manager.get(pk=uid)
    except(TypeError , ValueError , OverflowError , Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request , 'Congratulations! your account is activated.')
        return redirect('signin')
    else:
        messages.error(request , 'Invalid activation link')
        return redirect('register')

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email = email , password = password)
        # print("the user is : {}".format(user))
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart = cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart = cart)
                    # getting the product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                    # Get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user = user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)
                    for pr in product_variation:
                        if pr in ex_var_list:
                          index = ex_var_list.index(pr)
                          item_id =   id[index]
                          item = CartItem.objects.get(id = item_id)
                          item.quantity += 1
                          item.user = user
                          item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart = cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass

            auth.login(request,user)
            return redirect('home')
        else:
            messages.error(request , 'Invalid login credentials')
            return redirect('signin')
    return render(request, 'user/signin.html')

@login_required(login_url = 'signin')
def logout(request):
    auth.logout(request)
    messages.success(request , 'You are Logged Out!')
    return redirect('signin')


#Dashboard
def dashboard (request):
    return render(request, 'user/dashboard.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email = email).exists():
            user = Account.objects.get(email__exact = email)
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('user/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
                })
            to_email = email
            send_email = EmailMessage(mail_subject , message , to=[to_email])
            send_email.send()
            messages.success(request , 'Password reset has been sent to your email.')
            return redirect('signin')
        else:
            messages.error(request , 'Account does not exist!')
            redirect('forgot_password')
    return render(request , 'user/forgot_password.html')

def reset_password_validate(request , udidb64 , token):
    try:
        uid = urlsafe_base64_decode(udidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError , ValueError , OverflowError ,Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request , 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request , 'This link has benn expired!')
        return redirect('signin')

def reset_password (request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password :
            uid = request.session.get('uid')
            user = Account.objects.get(pk = uid)
            user.set_password(password)
            user.save()
            messages.success(request , 'Password reset successful')
            return redirect('signin')
        else:
            messages.error(request , 'Password does not match!')
            return redirect('reset_password')
    else:
        return render(request , 'user/reset_password.html')