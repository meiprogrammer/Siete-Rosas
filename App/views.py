from django.contrib.auth import authenticate, logout, login as auth_login
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Products, User, Events, Pay
from django.http import JsonResponse
import mercadopago, requests, json, random
from django.conf import settings
from django.core.mail import send_mail

def loginView(request):
    if (request.method == 'GET'):
        return render(request, "login.html")
    
    elif (request.method == 'POST'):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if (user is not None):
            auth_login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, "login.html", {
                "error": "Email ou senha incorretos, tente novamente e/ou preencha todos os campos."
            })

def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))  

def sendMail(request, email, user, password):
    if (not request.user.is_authenticated):
        verify_code = random.randint(100, 999)
            
        if ('verify_code' in request.session):
            del request.session['verify_code']
            
        request.session['verify_code'] = verify_code
            
        message = f"Olá, {user}, recebemos a tentativa de criação de uma conta no site sieterosas.com.br pelo seu email. Caso tenha sido você, use o código de verificação {verify_code}"
        send_mail("Código de Verificação",
                message,
                'sieterosas.noreply@gmail.com',
                [f'{email}'],
                fail_silently=False)

        return render(request, "email.html", {
            "email": email,
            "password": password,
            "username": user,
        })
    else:
        return index(request)

def verifyMail(request):
    if (not request.user.is_authenticated):
        if ('verify_code' in request.session):
            if (int(request.POST["code"]) == int(request.session.get('verify_code'))):
                new_user = User(
                    username=request.POST["username"],
                    email=request.POST["email"],
                    password=request.POST["password"],
                )
                new_user.set_password(request.POST["password"])
                new_user.save()

                del request.session['verify_code']
                return render(request, "login.html", {
                        "sucess": "Sua conta foi criada com sucesso."
                    })
            else:
                print(f"Código gerado: {request.session.get('verify_code')}, código digitado: {request.POST['code']}")
                del request.session['verify_code']
                return render(request, "register.html", {
                        "passkey": "O código não condiz com o digitado."
                    })
        else:
            return render(request, "register.html", {
                "passkey": "Sessão expirada, tente novamente."
            })
    else:
        return index(request)

def register(request):
    if (request.method == 'POST'):
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if (password != confirmation):
            return render(request, "register.html", {
                "passkey": "Sua senha e verificação de senha não condizem."
            })

        try:
            
            user = User.objects.create_user(username, email, password)
            user.save()
        
        except (ValueError, IntegrityError):
            return render(request, "register.html", {
                    "integrity": "Preencha todos os campos e/ou use um nome e email ainda não cadastrados."
                })

        user.delete()
        return sendMail(request, email, username, password)
    
    else:
        return render(request, "register.html")

def index(request):
    if (request.user.is_authenticated):
        return render(request, "index.html")
    else:
        return HttpResponseRedirect(reverse("login"))
    

def products(request):
    if (request.user.is_authenticated):
        products = Products.objects.all().values("name", "colors", "price", "id")
        return render (request, "products.html", {
            "products": products,
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def productLoad (request, id):
    if (request.user.is_authenticated):
        product = Products.objects.filter(id=id).values("name", "colors", "price", "id").first()
        if (product):
            return render(request, "product.html", {
                "product": product,
            })
        else:
            return HttpResponseRedirect(reverse("products"))
    else:
        return HttpResponseRedirect(reverse("login"))
    
def events(request):
    if (request.user.is_authenticated):
        events = Events.objects.all().values("name", "location", "description")
        return render(request, "events.html", {
            "events": events
        })
    else:
        return HttpResponseRedirect(reverse("login"))
    
def orderVerify(request, merchant_order_id):
    if request.user.is_authenticated:
        token = settings.MERCADOPAGO_API_KEY

        url = f"https://api.mercadopago.com/merchant_orders/{merchant_order_id}"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        try:
            pay = Pay.objects.get(merchant_order_id=merchant_order_id)
        except (Pay.DoesNotExist):
            return JsonResponse({"result": "failure", "message": "Pagamento não encontrado."})
        
        response = requests.get(url, headers=headers)
        
        if (response.status_code == 200):
            data = response.json()
            if (data.get('payments') and data['payments'][0]['status'] == "approved"):
                pay.status = "approved"
                pay.save()
                return JsonResponse({"result": "approved"})
            else:
                pay.status = "failure"
                pay.save()
                return JsonResponse({"result": "failure"})
        elif (response.status_code == 202):
            pay.status = "pending"
            pay.save()
            return JsonResponse({"result": "pending"})
        else:
            pay.status = "failure"
            pay.save()
            return JsonResponse({"result": "failure"})
    else:
        return HttpResponseRedirect(reverse("login"))
    
def checkout(request):
    if (request.user.is_authenticated):
        merchant_order_id = request.GET.get('merchant_order_id')

        if (merchant_order_id):
            response = orderVerify(request, merchant_order_id)
            result = json.loads(response.content).get("result")

            if (result == "approved"):
                return render(request, "approved.html")
            else:
                return render (request, "error.html", {
                    "status": result
            })
        else:
            return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("login"))


def checkoutAddress (request, productId):
    return render(request, "address.html", {
        "productId": productId
    })

def get_merchant_order(preference_id):
    sdk = mercadopago.SDK(settings.MERCADOPAGO_API_KEY)
    response = sdk.preference().get(preference_id)
    
    if (response['status'] == 200):
        merchant_order_id = response['response'].get('id')
        return merchant_order_id
    return None

def payment(request, id):
    if (request.user.is_authenticated):
        sdk = mercadopago.SDK(settings.MERCADOPAGO_API_KEY)
        product = Products.objects.get(id=id)

        payment_data = {
            "items": [
                {
                    "id": product.id,
                    "title":product.name,
                    "quantity": 1,
                    "currency_id": "BRL",
                    "unit_price": int(product.price),
                    "description": f"O sapato flamenco {product.name} é feito de forma artesanal, tem como foco o uso para dança, e não deve ser usado como um sapato normal.",
                },
            ],
            
            "back_urls": {
                "success": f"https://sieterosas.com.br/checkout",
                "failure": f"https://sieterosas.com.br/checkout",
                "pending": f"https://sieterosas.com.br/checkout",
            },

            "payer": {
                "name": f"{request.user.username}",
                "email": f"{request.user.email}",
                "address": {
                    "street_name": request.POST.get("street"),
                    "street_number": request.POST.get("number"),
                    "zip_code": request.POST.get("cep"),
                }
            },
            
            "auto_return": "approved",
        }

        result = sdk.preference().create(payment_data)
        checkout = result["response"]
        merchant_order_id = get_merchant_order(checkout["id"])

        new_pay = Pay (
            user=request.user.username,
            state=request.POST.get("state"),
            city=request.POST.get("city"),
            cep=request.POST.get("cep"),
            number=request.POST.get("number"),
            complement=request.POST.get("comments"),
            product=request.POST.get("productId"),
            status="pending",
            merchant_order_id=merchant_order_id,
        )
        new_pay.save()
    
        return HttpResponseRedirect(checkout["init_point"])
    else:
        return HttpResponseRedirect(reverse("login"))
    
import random