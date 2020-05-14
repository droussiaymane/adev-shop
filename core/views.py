from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import Item,Imagedetail,OrderItem,Order,Coupon,BillingAdress,Payment
from django.views.generic import ListView,DetailView
from .forms import add_to_cart,billing_adress
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.conf import settings
from django.core.paginator import Paginator
from django.core.mail import send_mail

# Create your views here.
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# class Home(ListView):
#     model=Item
#     template_name="core/home.html"
#     context_object_name="items"
#     paginate_by=2

def Home(request):
    item=Item.objects.all()
    
    paginator = Paginator(item, 8) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={"page_obj":page_obj}

    if request.user.is_authenticated:
        order=Order.objects.filter(user=request.user,is_ordered=False)
        if order.exists():
            order_qs=order[0]
            context.update({'order':order_qs})
    return render(request,'core/home.html',context)

def about_us(request):
    context={}
    if request.user.is_authenticated:
            
            order=Order.objects.filter(user=request.user,is_ordered=False)
            if order.exists():
                order_qs=order[0]
                context={'order':order_qs}
    return render(request,'core/about-us.html',context)


def contact_us(request):
    context={}
    if request.method=="GET":
        if request.user.is_authenticated:
            
            order=Order.objects.filter(user=request.user,is_ordered=False)
            if order.exists():
                order_qs=order[0]
                context={'order':order_qs}

        return render(request,'core/contact-us.html',context)  

    if request.method=="POST":
        subject=request.POST['subject']
        email_client=request.POST['email']
        message=request.POST['message']
        send_mail(subject,message,email_client,recipient_list=['adev.off@gmail.com'],fail_silently=False)
        messages.info(request,'Thanks for your Feedback')
        return redirect('core:contact_us')


def Your_Orders(request):
    orders_qs=Order.objects.filter(user=request.user)
    print(orders_qs)
  

    context={'orders':orders_qs}
    return render(request,'core/orders.html',context)



def DetailItem(request,pk):
    item=Item.objects.get(pk=pk)
    
    if request.method =="GET":
        context={'item':item}

        if request.user.is_authenticated:
            order=Order.objects.filter(user=request.user,is_ordered=False)
            if order.exists():
                order_qs=order[0]
                context.update({'order':order_qs})
        return render(request,'core/detail_item.html',context)

    if request.method=='POST':
        if request.user.is_authenticated:
            
            form=add_to_cart(data=request.POST)
            #create order
            order_qs=Order.objects.filter(user=request.user,is_ordered=False)
            #retourne un query set <queryset [<oder:adev>]> donc pour avoir adev , on doit ajouter [0] 
            if form.is_valid():
                item=Item.objects.get(pk=pk)
                color=form.cleaned_data['color']
                size=form.cleaned_data['size']
                quantity=form.cleaned_data.get('quantity')
                Order_item=OrderItem(user=request.user,item=item,size=size,color=color,quantity=quantity)
                Order_item.save()
                if order_qs.exists():
                    order=order_qs[0]


                    order.order_items.add(Order_item)

                    messages.success(request,"Your order has been created ")
                        #add order in the cart

                        #redirect them to the checkout form
                    return redirect('core:detail_item' ,pk)
                else:
                    order_new=Order.objects.create(user=request.user,date_creation=timezone.now())
                    order_new.save()

                    order_new.order_items.add(Order_item)
        
        else:
            messages.info(request,"please login first !")
            return redirect('/login/')

return redirect('core:detail_item',pk)

@login_required(login_url="/login/")
def Cart(request):
    context={}
    order_item=OrderItem.objects.filter(user=request.user,is_ordered=False)
    

   
        
    
        
        
    
    
    
    if request.method=="GET":

        if request.user.is_authenticated:
            
            order=Order.objects.filter(user=request.user,is_ordered=False)
            if order.exists():
                order_qs=order[0]
                context={'order':order_qs}
        
        return render(request,'core/cart.html',context)

    if request.method=="POST":
        return redirect("core:checkout")

    


@login_required(login_url="/login/")
def Update_Cart(request):
    item_order=OrderItem.objects.filter(user=request.user,is_ordered=False)
    order=Order.objects
    i=1
    for item_qs in item_order:
        input_name="quantity"+str(i)
        item_qs.quantity=request.POST[input_name]
        item_qs.save()
        i+=1
    return redirect('core:cart')

@login_required(login_url="/login/")
def Remove_from_cart(request,pk):
    item_order=get_object_or_404(OrderItem, pk=pk,user=request.user)
    item_order.delete()

    messages.warning(request,"Your item has been Deleted !")
    return redirect('core:cart')




@login_required(login_url="/login/")
def Coupon_add(request):
    coupon_code=request.POST['coupon_code']
    coupon_disponnible=Coupon.objects.filter(expiration=False,coupon=coupon_code)
    if coupon_disponnible.exists():
        coupon=coupon_disponnible[0]
        order_qs=Order.objects.get(user=request.user,is_ordered=False)
        if order_qs.get_total() >= coupon.minimal_amount_required:
            order_qs.coupon.add(coupon)
            coupon.expiration=True
            coupon.save()
            messages.success(request,"your coupon has been added")
            return redirect('core:cart')
        else:
            messages.info(request,"sorry this coupon required $" + str(coupon.minimal_amount_required) +" of minimal amount , Add some Order items to use it !!")
            return redirect('core:cart')
       

    else:
        messages.warning(request,"This coupon doesn't exist, please try again !")
        return redirect('core:cart')


    
    

@login_required(login_url="/login/")
def Checkout(request):
    form=billing_adress()
    context={'form':form}
    order=Order.objects.filter(user=request.user,is_ordered=False)


    if request.user.is_authenticated:
        if order.exists():
            order_qs=order[0]
            context.update({'order':order_qs})
    if order.exists():
       context.update({'order':order[0]})
    if request.method=="GET":

        return render(request,'core/checkout.html',context)

    

@login_required(login_url="/login/")
def Payment_stripe(request):
    order=Order.objects.get(user=request.user,is_ordered=False)
    if order.adress is None:
        messages.info(request,"please Submit Your Billing Adress first !")
        return redirect('core:checkout')
    else:

    
        try:
            token=request.POST['stripeToken']
            #creer une charge
            charge = stripe.Charge.create(
            amount=int(order.get_total())*100, #per cent 
            currency="usd",
            description="My First Test Charge (created for API docs)",
            source=token, # obtained with Stripe.js
            )

            payment=Payment(user=request.user,stripe_id_charge=charge['id'],amount=order.get_total(),date_payment=timezone.now())
            payment.save()
            order.payment=payment
            order.is_ordered=True
            order.save()

            # change is_ordered from false to true
            for items in order.order_items.all():
                items.is_ordered=True
                items.save()
            messages.success(request,"your order has been done !")
            return redirect('core:home')

            
        except stripe.error.CardError as e:
            messages.warning(request,"Card error")
            return redirect('core:checkout')

        except stripe.error.RateLimitError as e:
            messages.warning(request,"RateLimitError")
            return redirect('core:checkout')
        except stripe.error.InvalidRequestError as e:
            messages.warning(request,"InvalidRequestError")
            return redirect('core:checkout')
        except stripe.error.AuthenticationError as e:
            messages.warning(request,"AuthenticationError")
            return redirect('core:checkout')
        except stripe.error.APIConnectionError as e:
            messages.warning(request,"APIConnectionError")
            return redirect('core:checkout')
        except stripe.error.StripeError as e:
            messages.warning(request,"StripeError")
            return redirect('core:checkout')
        except Exception as e:
            messages.warning(request,"error ! Try again please !")
            return redirect('core:checkout')
        



def Payment_paypal(request):
    pass





def Billing_Adress(request):
    order=Order.objects.filter(user=request.user,is_ordered=False)
    form=billing_adress(request.POST)
    if form.is_valid():
        order_qs=order[0]
        first_name=form.cleaned_data['first_name']
        last_name=form.cleaned_data['last_name']
        adress1=form.cleaned_data['adress1']
        adress2=form.cleaned_data['adress2']
        city=form.cleaned_data['city']
        zip=form.cleaned_data['zip']
        country=form.cleaned_data['country']
        phone=form.cleaned_data['phone']
        
        adress_order=BillingAdress(user=request.user,
            first_name=first_name,
            last_name=last_name,
            adress1=adress1,
            adress2=adress2,
            zip=zip,
            city=city,
            country=country,
            phone=phone
        )
        adress_order.save()
        order_qs.adress=adress_order
        order_qs.save()
    
        
        messages.success(request,"your adress has been submitted , please Complete Your Payment !")
        return redirect('core:checkout')
    else:
        messages.warning(request,'please , put The correct information of your Billing Adress')
        return redirect('core:checkout')

def Remove_Order(request,pk):
    order=Order.objects.get(user=request.user,pk=pk)
    items=order.order_items.all()
    items.delete()
    order.delete()
    messages.info(request,'Your Order Has been Deleted !')
    return redirect('core:cart')


def views_404(request,*args,**kwargs):
    return render(request,'errors_404.html',status=404)
