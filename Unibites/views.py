from django.shortcuts import render, redirect
from django.http import *
from unicodedata import category
from collections import defaultdict
from .models import *
from django.utils import timezone
import random
import smtplib
from email.message import EmailMessage

def index(request):
    canteens = Canteen.objects.filter().order_by('?')[:4]
    categories = Category.objects.all()
    return render(request, 'index.html', {'canteens': canteens , 'categories':categories})


def loginPage(request):
    if "user" in request.session:
        return redirect('index')
    else:
        return render(request, 'LoginPage.html')


def about(request):
    return render(request, 'about.html')


def contactUs(request):
    return render(request, 'contactUs.html')


def CanteenPage(request):
    if "canteen" in request.session:
        return redirect('canteenDash')
    else:
        return render(request, 'CanteenLogin.html')


def canteenDash(request):
    if "canteen" in request.session:
        canteen = Canteen.objects.get(id=request.session['canteen']['id'])
        return render(request, 'canteenDashboard.html', {'canteen':canteen})
    else:
        return render(request, 'CanteenLogin.html')


def logoutUser(request):
    request.session["user"] = None
    del request.session["user"]
    return redirect('index')


def logoutCanteen(request):
    request.session["canteen"] = None
    del request.session["canteen"]
    return redirect('CanteenPage')


def registerUser(request):
    name = request.POST['name']
    email = request.POST['email']
    number = request.POST['number']
    password = request.POST['password']
    oldUser = User.objects.filter(email=email)
    if len(oldUser) == 0:
        user = User(name=name, email=email, number=number, password=password)
        user.save()
        return JsonResponse({"code": 2, "message": "User has been created. Please LOGIN"})
    else:
        return JsonResponse({"code": 3, "message": "Account with this email already exists!"})


def loginUser(request):
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.filter(email=email, password=password)
    if len(user) == 0:
        return JsonResponse({"code": 3, "message": "Invalid Email or Password"})
    else:
        if user[0].status == "0":
            return JsonResponse({"code": 3, "message": "User has been disabled."})
        else:
            d = {
                "id": user[0].id,
                "name": user[0].name,
                "email": user[0].email,
                "number": user[0].number,
            }
            request.session['user'] = d
            return JsonResponse({"code": 2, "message": "LOGIN Successful"})


def CanteenLogin(request):
    name = request.POST['name']
    email = request.POST['email']
    password = request.POST['password']
    canteen = Canteen.objects.filter(name=name, email=email, password=password)
    if len(canteen) == 0:
        return JsonResponse({"code": 3, "message": "Invalid Email or Password"})
    else:
        if canteen[0].status == "0":
            return JsonResponse({"code": 3, "message": "Canteen has been disabled."})
        else:
            d = {
                "id": canteen[0].id,
                "name": canteen[0].name,
                "email": canteen[0].email,
                "number": canteen[0].number,
                "location": canteen[0].location,
            }
            request.session['canteen'] = d
            return JsonResponse({"code": 2, "message": "LOGIN Successful"})


def addItemPage(request):
    category = Category.objects.all()
    return render(request, 'Food/AddItems.html', {'category': category})


def addFood(request):
    name = request.POST['name']
    description = request.POST['description']
    image = request.FILES['image']
    price = request.POST['price']
    discount = request.POST['discount']
    category = request.POST['category']
    canteen = request.POST['canteen']
    food = FoodItem(name=name, description=description, price=price, discount=discount, category_id=category,
                    canteen_id=canteen, image=image)
    food.save()
    return JsonResponse({"code": 2, "message": "Food Item has been added."})


def addReview(request):
    name = request.POST['name']
    email = request.POST['email']
    review = request.POST['review']
    canteen = request.POST['canteenId']
    rev = Reviews(name=name,email=email,review=review,canteen_id=canteen )
    rev.save()
    return JsonResponse({"code": 2, "message": "Review has been added."})


def manageFood(request):
    category = Category.objects.all()
    return render(request, 'Food/manageFood.html', {'category': category}, )


def deleteItem(request, id):
    item = FoodItem.objects.get(id=id)
    item.delete()
    return JsonResponse({"code": 2, "message": "Food Item has been Deleted."})


def Items(request):
    queryset = FoodItem.objects.filter(canteen_id=request.session['canteen']['id'])
    values = queryset.values()
    items = list(values)
    print(items)
    return JsonResponse({"code": 2, "message": "success", "data": items}, safe=False)


def Canteens(request):
    queryset = Canteen.objects.all()
    values = queryset.values()
    canteens = list(values)
    return JsonResponse({"code": 2, "message": "success", "data": canteens}, safe=False)


def mess(request):
    return  render (request, 'UserNav/mess.html')


def updateItem(request):
    id = request.POST["id"]
    name = request.POST["name"]
    description = request.POST["description"]
    discount = request.POST["discount"]
    price = request.POST["price"]
    category = request.POST["category"]

    item = FoodItem.objects.get(id=id)

    item.name = name
    item.description = description
    item.discount = discount
    item.price = price
    item.category_id = category
    if "image" in request.FILES:
        image = request.FILES["image"]
        item.image = image
    item.save()

    return JsonResponse({"code": 2, "message": "item has been updated"}, safe=False)


def update_availability(request, id):
    item = FoodItem.objects.get(id=id)
    if str(item.canteen.id) == str(request.session['canteen']['id']):
        item.availability = request.POST.get('availability')
        item.save()
    return redirect('manageFood')


def changePassPage(request):
    user = User.objects.all()
    return render(request, 'UserNav/changePassPage.html', {'user': user})


def editProfilePage(request):
    user = User.objects.all()
    return render(request, 'UserNav/EditProfile.html', {'user': user})


def editCanProfilePage(request):
    id = request.session['canteen']['id']
    canteen = Canteen.objects.filter(id=id)
    return render(request, 'Food/EditCanProfile.html', {'canteen': canteen})


def changeCanPWPage(request):
    canteen = Canteen.objects.all()
    return render(request, 'CanteenCh_pw.html', {'canteen': canteen})


def changePass(request):
    id = request.POST['id']
    oldPass = request.POST['oldPass']
    newPass = request.POST['newPass']

    user = User.objects.filter(id=id, password=oldPass)
    if len(user) == 0:
        return JsonResponse({"code": 3, "message": "Invalid old password."})
    else:
        user[0].password = newPass
        user[0].save()
        return JsonResponse({"code": 2, "message": "Password changed successfully."})


def changeCanPW(request):
    id = request.POST['id']
    oldPw = request.POST['oldPw']
    newPw = request.POST['newPw']

    canteen = Canteen.objects.filter(id=id, password=oldPw)
    if len(canteen) == 0:
        return JsonResponse({"code": 3, "message": "Invalid old password."})
    else:
        canteen[0].password = newPw
        canteen[0].save()
        return JsonResponse({"code": 2, "message": "Password changed successfully."})


def ViewCanteen(request):
    return render(request, "UserNav/ViewCanteen.html")


def openMenu(request, id):  # this id is canteen id
    reviews = Reviews.objects.filter(canteen_id=id)
    fooditem = FoodItem.objects.filter(canteen_id=id, availability="1").order_by('price')
    category_ids = fooditem.values_list('category_id', flat=True).distinct()
    categories = Category.objects.filter(id__in=category_ids).order_by('name')
    return render(request, 'UserNav/Menu.html', {
        'fooditem': fooditem,
        'categories': categories,
        'id': id,
        'reviews': reviews,
    })


def updateProfile(request):
    id = request.session['user']['id']
    name = request.POST['name']
    email = request.POST['email']
    number = request.POST['number']

    user = User.objects.filter(id=id).first()

    if not user:
        return JsonResponse({"code": 3, "message": "User Not Found"})

    user.name = name
    user.email = email
    user.number = number
    user.save()

    request.session['user'] = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'number': user.number,
    }

    return JsonResponse({'code': 2, 'message': 'Profile updated successfully'})


def updateCanProfile(request):
    id = request.session['canteen']['id']
    name = request.POST['name']
    email = request.POST['email']
    number = request.POST['number']
    location = request.POST['location']

    canteen = Canteen.objects.filter(id=id).first()

    if not canteen:
        return JsonResponse({"code": 3, "message": "Canteen Not Found"})

    canteen.name = name
    canteen.email = email
    canteen.number = number
    canteen.location = location
    canteen.save()

    request.session['canteen'] = {
        'id': canteen.id,
        'name': canteen.name,
        'email': canteen.email,
        'number': canteen.number,
        'location': canteen.location,
    }

    return JsonResponse({'code': 2, 'message': 'Profile updated successfully'})


def AddToCartPage(request):
    if "user" in request.session:
        user_data = request.session.get("user")
        user_id = user_data.get("id")
        user = User.objects.get(id=user_id)

        if request.method == 'POST':
            food_id = request.POST.get('food_id')
            if not food_id:
                return JsonResponse({"error": "No food item specified"}, status=400)

            try:
                food_item = FoodItem.objects.select_related('canteen').get(id=food_id)
            except FoodItem.DoesNotExist:
                return JsonResponse({"error": "Food item not found"}, status=404)

            existing_cart_items = CartItem.objects.filter(user=user)

            # Check if cart is not empty and the canteen doesn't match
            if existing_cart_items.exists():
                existing_canteen = existing_cart_items.first().canteen
                if food_item.canteen != existing_canteen:
                    return JsonResponse(
                        {"error": "You cannot add items from different canteens. Please clear your cart first."},
                        status=403)

            cart_item = existing_cart_items.filter(food_item=food_item).first()

            if cart_item:
                cart_item.quantity += 1
            else:
                cart_item = CartItem(
                    user=user,
                    food_item=food_item,
                    canteen=food_item.canteen,
                    quantity=1,
                    price=food_item.price
                )

            cart_item.save()
            return JsonResponse({"message": "Item added successfully"})

        cart_items = CartItem.objects.select_related('food_item', 'canteen').filter(user=user)
        total_price = sum(item.total_price for item in cart_items)

        return render(request, 'UserNav/AddToCartPage.html', {
            'cart': cart_items,
            'total_price': total_price
        })

    else:
        return redirect('loginPage')


def UpdateCartQuantity(request):
    MAX_QUANTITY = 6

    if "user" in request.session:
        user_id = request.session['user']['id']
        user = User.objects.get(id=user_id)

        food_id = request.GET.get('food_id')
        action = request.GET.get('action')

        try:
            cart_item = CartItem.objects.get(user=user, food_item_id=food_id)

            if action == 'increase':
                if cart_item.quantity < MAX_QUANTITY:
                    cart_item.quantity += 1
                    cart_item.save()
                else:
                    return JsonResponse({
                        'success': False,
                        'error': 'Maximum quantity reached',
                        'quantity': cart_item.quantity
                    })

            elif action == 'decrease' and cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()

            cart_total = sum(item.total_price for item in CartItem.objects.filter(user=user))

            return JsonResponse({
                'success': True,
                'quantity': cart_item.quantity,
                'item_total_price': cart_item.total_price,
                'cart_total_price': cart_total
            })

        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found'})

    return JsonResponse({'success': False, 'error': 'User not logged in'})


def RemoveFromCart(request):
    if "user" in request.session:
        user_data = request.session['user']
        user = User.objects.get(id=user_data['id'])

        food_id = request.POST.get('food_id')
        if food_id:
            CartItem.objects.filter(user=user, food_item_id=food_id).delete()

    return redirect('AddToCartPage')


def place_order(request):
    if request.method == "POST":
        payment_mode = request.POST.get('payment_mode')
        user = request.session['user']['id']

        cart_items = CartItem.objects.select_related('food_item', 'canteen').filter(user=user)

        canteen = cart_items.first().canteen_id

        total_price = sum(item.total_price for item in cart_items)

        order = Order.objects.create(
            user_id=user,
            canteen_id=canteen,
            total_price=total_price,
            mode=payment_mode,
            status="0",
            date=timezone.now()
        )

        for item in cart_items:
            OrderDetails.objects.create(
                order_id=order.id,
                food_id=item.food_item.id,
                quantity=item.quantity,
                total_price=item.total_price
            )

        cart_items.delete()

        return JsonResponse({"message": "Order placed successfully"})

    return JsonResponse({"error": "Invalid request method"}, status=405)


def myOrders(request):
    id = request.session['user']['id']
    orders = Order.objects.filter(user_id=id).order_by('-id')
    details = []
    for order in orders:
        order_details_list = OrderDetails.objects.filter(order_id=order.id)
        order_data = {
            'order': order,
            'details': list(order_details_list)
        }
        details.append(order_data)
    return render (request, 'UserNav/myOrders.html',{'details': details})


def CanOrders(request):
    id = request.session['canteen']['id']
    orders = Order.objects.filter(canteen_id=id).order_by('-id')
    details = []
    for order in orders:
        order_details_list = OrderDetails.objects.filter(order_id=order.id)
        order_data = {
            'order': order,
            'details': list(order_details_list)
        }
        details.append(order_data)
    return render (request, 'Food/CanOrders.html',{'details': details})


def pendingOrder(request):
    if "canteen" in request.session:
        return render(request, 'Food/PendingOrders.html')
    else:
        return redirect('CanteenPage')


def allPendingOrder(request):
    queryset = Order.objects.select_related('user').filter(status='0').order_by('-id')
    fooditem = []

    for order in queryset:
        order_details_qs = OrderDetails.objects.filter(order=order).select_related('food')
        order_details = []

        for detail in order_details_qs:
            order_details.append({
                "id": detail.id,
                "quantity": detail.quantity,
                "total_price": detail.total_price,
                "food_id": detail.food.id,
                "food_name": detail.food.name  # ✅ correct access
            })

        fooditem.append({
            "id": order.id,
            "date": order.date,
            "total_price": order.total_price,
            "mode": order.mode,
            "user_id": order.user.id,
            "user_name": order.user.name,
            "order_details": order_details,
        })

    return JsonResponse({"code": 2, "message": 'success', "data": fooditem})


def changeOrderStatus(request):

    new_status=request.POST.get('order_delivery_status')
    order_id=request.POST.get('order_id')
    order=Order.objects.filter(id=order_id)
    if len(order)==0:
        return JsonResponse({"code": 3, "message": 'warning'}, safe=False)
    else:
        order[0].status=new_status
        order[0].save()
        return JsonResponse({"code": 2, "message": 'Status updated successfully'}, safe=False)


def searched_menu(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')

    food_items = FoodItem.objects.select_related('category', 'canteen').all()
    selected_category_obj = None

    if query:
        food_items = food_items.filter(name__icontains=query)

    if category_id:
        food_items = food_items.filter(category_id=category_id)
        try:
            selected_category_obj = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            selected_category_obj = None

    grouped_by_canteen = defaultdict(list)
    for item in food_items:
        grouped_by_canteen[item.canteen.name].append(item)

    context = {
        'grouped_items': grouped_by_canteen.items(),
        'categories': Category.objects.all(),
        'selected_category': category_id,
        'selected_category_name': selected_category_obj.name if selected_category_obj else "All Categories",
         'search_query': request.GET.get('q', ''),
    }
    return render(request, 'SearchedMenu.html', context)


def forgotPassword(request):
    email = request.POST['email']
    user = User.objects.filter(email=email)
    if len(user) == 0:
        return JsonResponse({"code": 3, "message": "Email Not Found."})
    else:
        password = random.randint(100000, 999999)
        user[0].password = password
        user[0].save()
        sendEmail(
            to=email,
            subject="Password Reset",
            message=f"Your new Password is {password}",
        )
        return JsonResponse({"code": 2, "message": "Your new Password has been sent successfully to your email."})


def sendEmail(to, message, subject):
    try:
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = subject
        msg['To'] = to
        msg['From'] = 'vmm.testing.email2@gmail.com'
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('vmm.testing.email2@gmail.com', 'tirllvbbhctznive')

        server.send_message(msg)
        print('Mail Sent')
        server.quit()
        return True
    except:
        return False