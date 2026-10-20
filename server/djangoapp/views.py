import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
    return JsonResponse({"userName": None, "status": "Failed"})

@csrf_exempt
def logout_user(request):
    logout(request)
    return JsonResponse({"userName": ""})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({"userName": username, "error": "Already Registered"})
        
        try:
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        except Exception as e:
            return JsonResponse({"userName": username, "error": str(e)})
    return JsonResponse({"error": "Invalid Request"})

from .models import CarMake, CarModel
from .populate import initiate

def get_cars(request):
    count = CarMake.objects.filter().count()
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})

from .models import CarMake, CarModel
from .populate import initiate

def get_cars(request):
    count = CarMake.objects.filter().count()
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})
