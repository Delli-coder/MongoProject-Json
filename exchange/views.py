
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .models import Profile, OrderBuy, OrderSell
from django.contrib.auth.decorators import login_required
import random, datetime


def register(request):  # se viene inserito un Username gia' scelto genera un errore
    utente = []
    username = input('Inserisci username  ')
    email = input('Inserisci email  ')
    password1 = input('Inserisci password  ')
    password2 = input("inserisci password(again)  ")
    if password1 == password2:
        user_new = User.objects.create_user(username=username, email=email, password=password1)
        user_new.save()
        new_user = Profile()
        new_user.user = user_new
        new_user.btc_wallet = random.randint(1, 10)
        new_user.original_btc = new_user.btc_wallet
        new_user.wallet = 100000
        new_user.save()
        print('Utente creato correttamente')
        utente.append(
            {
                'Nuovo utente': f"{new_user.user}",
                'Email': email,
                'BTC posseduti': new_user.original_btc
            }
        )
        return JsonResponse(utente, safe=False)
    else:
        print('Password sbagliate!')
        return JsonResponse(utente, safe=False)


def log(request):
    credenziali = []
    username = input('Inserisci Username  ')
    password = input('Inserisci la password  ')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        profile = Profile.objects.get(user=user)
        credenziali.append(
            {
                'usarname': f"{username}",
                'password': password,
                'BTC': profile.btc_wallet,
                'status': 'login'
            }
        )
        login(request, user)
        print('Utente loggato')
        return JsonResponse(credenziali, safe=False)
    else:
        print('Riprova!')
    return JsonResponse(credenziali, safe=False)


@login_required()
def new_order_buy(request):
    ordine = []
    user = request.user
    profile_buyer = Profile.objects.get(user=user)
    all_order_sell = OrderSell.objects.filter(active='True').order_by('price', 'datetime')
    price = input('Inserisci il prezzo $  ')
    quantity = input('Inserisci la quantita di BTC  ')
    if float(price) * float(quantity) <= profile_buyer.wallet:
        new_order_buy = OrderBuy()
        new_order_buy.user = user
        new_order_buy.price = float(price)
        new_order_buy.quantity = float(quantity)
        new_order_buy.original_quantity = float(quantity)
        new_order_buy.datetime = datetime.datetime.now()
        new_order_buy.save()
        ordine.append(
            {
                'User nuovo ordine': f"{new_order_buy.user}",
                'Prezzo nuovo ordine': new_order_buy.price,
                'Quantita BTC': new_order_buy.quantity,
                'Data': new_order_buy.datetime,
                'Active': 'True'
            }
        )
        print('Ordine creato')
        if len(all_order_sell) > 0:
            for order in all_order_sell:
                if new_order_buy.price >= order.price and profile_buyer.user != order.user:
                    profile_seller = Profile.objects.get(user=order.user)
                    if new_order_buy.quantity == order.quantity:
                        profile_buyer.wallet -= (new_order_buy.quantity * order.price)
                        profile_buyer.btc_wallet += new_order_buy.quantity
                        profile_seller.wallet += (new_order_buy.quantity * order.price)
                        profile_seller.btc_wallet -= new_order_buy.quantity
                        new_order_buy.active = 'False'
                        order.active = 'False'
                        profile_seller.save()
                        profile_buyer.save()
                        new_order_buy.save()
                        order.save()
                        ordine.append(
                            {
                                'User nuovo ordine': f"{new_order_buy.user}",
                                'Prezzo nuovo ordine': new_order_buy.price,
                                'Quantita BTC': new_order_buy.quantity,
                                'Data': new_order_buy.datetime,
                            }
                        )
                        print('Ordine eseguito')
                        return JsonResponse(ordine, safe=False)
                    elif new_order_buy.quantity > order.quantity:
                        profile_buyer.wallet -= (order.quantity * order.price)
                        profile_buyer.btc_wallet += order.quantity
                        profile_seller.wallet += (order.quantity * order.price)
                        profile_seller.btc_wallet -= order.quantity
                        new_order_buy.quantity -= order.quantity
                        order.active = 'False'
                        profile_seller.save()
                        profile_buyer.save()
                        new_order_buy.save()
                        order.save()
                        continue
                    elif new_order_buy.quantity < order.quantity:
                        profile_buyer.wallet -= (new_order_buy.quantity * order.price)
                        profile_buyer.btc_wallet += new_order_buy.quantity
                        profile_seller.wallet += (new_order_buy.quantity * order.price)
                        profile_seller.btc_wallet -= new_order_buy.quantity
                        order.quantity -= new_order_buy.quantity
                        new_order_buy.active = 'False'
                        profile_seller.save()
                        profile_buyer.save()
                        new_order_buy.save()
                        order.save()
                        ordine.append(
                            {
                                'User nuovo ordine': f"{new_order_buy.user}",
                                'Prezzo nuovo ordine': new_order_buy.price,
                                'Quantita BTC': new_order_buy.quantity,
                                'Data': new_order_buy.datetime,
                            }
                        )
                        print('Ordine vendita eseguito parzialmente')
                        return JsonResponse(ordine, safe=False)
                else:
                    print('in attesa..')
                    return JsonResponse(ordine, safe=False)
        else:
            print('in attesa..')
            return JsonResponse(ordine, safe=False)
    else:
        print("Attenzione! fondi non disponibili per l'operazione")
        return JsonResponse(ordine, safe=False)


def new_order_sell(request):
    ordine = []
    user = request.user
    seller_profile = Profile.objects.get(user=user)
    all_order_buy = OrderBuy.objects.filter(active='True').order_by('price', 'datetime')
    sell_price = input('Inserisci il prezzo $  ')
    sell_quantity = input('Inserisci la quantita di BTC  ')
    if float(sell_quantity) <= seller_profile.btc_wallet:
        new_order_sell = OrderSell()
        new_order_sell.user = user
        new_order_sell.quantity = float(sell_quantity)
        new_order_sell.price = float(sell_price)
        new_order_sell.original_quantity = float(sell_quantity)
        new_order_sell.datetime = datetime.datetime.now()
        new_order_sell.save()
        ordine.append(
            {
                'User nuovo ordine': f"{new_order_sell.user}",
                'Prezzo nuovo ordine': new_order_sell.price,
                'Quantita BTC': new_order_sell.quantity,
                'Data': new_order_sell.datetime,
                'Active': 'True'
            }
        )
        print('Ordine creato')
        if len(all_order_buy) > 0:
            for order in all_order_buy:
                if new_order_sell.price <= order.price and seller_profile.user != order.user:
                    buyer_profile = Profile.objects.get(user=order.user)
                    if new_order_sell.quantity == order.quantity:
                        seller_profile.btc_wallet -= new_order_sell.quantity
                        seller_profile.wallet += (order.quantity * order.price)
                        buyer_profile.btc_wallet += new_order_sell.quantity
                        buyer_profile.wallet -= (order.quantity * order.price)
                        new_order_sell.active = 'False'
                        order.active = 'False'
                        seller_profile.save()
                        buyer_profile.save()
                        new_order_sell.save()
                        order.save()
                        ordine.append(
                            {
                                'User nuovo ordine': f"{new_order_sell.user}",
                                'Prezzo nuovo ordine': new_order_sell.price,
                                'Quantita BTC': new_order_sell.quantity,
                                'Data': new_order_sell.datetime,
                                'Active': 'False'
                            }
                        )
                        print('Ordine vendita eseguito')
                        return JsonResponse(ordine, safe=False)
                    elif new_order_sell.quantity > order.quantity:
                        seller_profile.btc_wallet -= order.quantity
                        seller_profile.wallet += (order.quantity * order.price)
                        buyer_profile.btc_wallet += order.quantity
                        buyer_profile.wallet -= (order.price * order.quantity)
                        new_order_sell.quantity -= order.quantity
                        order.active = 'False'
                        seller_profile.save()
                        buyer_profile.save()
                        new_order_sell.save()
                        order.save()
                        print('Ordine eseguito parzialmente')
                        continue
                    elif new_order_sell.quantity < order.quantity:
                        seller_profile.btc_wallet -= new_order_sell.quantity
                        seller_profile.wallet += (new_order_sell.quantity * order.price)
                        buyer_profile.btc_wallet += new_order_sell.quantity
                        buyer_profile.wallet -= (new_order_sell.quantity * order.price)
                        order.quantity -= new_order_sell.quantity
                        new_order_sell.active = 'False'
                        seller_profile.save()
                        buyer_profile.save()
                        new_order_sell.save()
                        order.save()
                        ordine.append(
                            {
                                'User nuovo ordine': f"{new_order_sell.user}",
                                'Prezzo nuovo ordine': new_order_sell.price,
                                'Quantita BTC': new_order_sell.quantity,
                                'Data': new_order_sell.datetime,
                                'Active': 'False'
                            }
                        )
                        print('Ordine vendita eseguito')
                        return JsonResponse(ordine, safe=False)
                else:
                    print('In attesa..')
                    return JsonResponse(ordine, safe=False)
        else:
            print('In attesa..')
            return JsonResponse(ordine, safe=False)
    else:
        print('Attenzione! BTC non sufficienti!')
        return JsonResponse(ordine, safe=False)


def order_active(request):
    orders_buy = OrderBuy.objects.filter(active='True')
    orders_sell = OrderSell.objects.filter(active='True')
    lis = []
    for order in orders_buy:
        lis.append(
            {
                'User': f"{order.user}",
                'Price': order.price,
                'Quantity': order.quantity,
                'Date': order.datetime,
                'Type': "BUY"
            }
        )
    for order_s in orders_sell:
        lis.append(
            {
                'User': f"{order_s.user}",
                'Price': order_s.price,
                'Quantity': order_s.quantity,
                'Date': order_s.datetime,
                'Type': "SELL"
            }
        )
    return JsonResponse(lis, safe=False)


def order_inactive(request):
    orders_buy = OrderBuy.objects.filter(active='False')
    orders_sell = OrderSell.objects.filter(active='False')
    lis2 = []
    for order in orders_buy:
        lis2.append(
            {
                'User': f"{order.user}",
                'Price': order.price,
                'Quantity': order.quantity,
                'Date': order.datetime,
                'Active': 'False',
                'Type': "BUY"
            }
        )
    for order_s in orders_sell:
        lis2.append(
            {
                'User': f"{order_s.user}",
                'Price': order_s.price,
                'Quantity': order_s.quantity,
                'Date': order_s.datetime,
                'Active': 'False',
                'Type': "SELL"
            }
        )
    return JsonResponse(lis2, safe=False)
# Create your views here.
