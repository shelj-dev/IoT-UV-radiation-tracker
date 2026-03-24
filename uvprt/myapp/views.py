from urllib import request

from django.shortcuts import render, redirect
from myapp.forms import uvForm
from myapp.models import uv, sensor_data

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET


def home(request):
    sensor_data_list = sensor_data.objects.order_by('-timestamp')[:10]
    context = {'sensor_data_list': sensor_data_list}
    return render(request, 'home.html', context)   


def update_threshold(request):
    data = uv.objects.first() 

    if request.method == 'POST':
        form = uvForm(request.POST , instance=data)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:        
        form = uvForm(instance=data)
        return render(request, 'update_threshold.html'  , {'form': form})
    

@csrf_exempt
def get_sensor_data(request):
    if request.method == "POST":
        data = json.loads(request.body)

        value = data.get("sensor")

        sensor_data.objects.create(value=value)

        return JsonResponse({
            "status": "received",
            "sensor": value
        })

    return JsonResponse({"error": "POST required"})


def get_sensor(request):
    data = sensor_data.objects.order_by('-timestamp')[:1]
    data_list = [{"value": d.value, "timestamp": d.timestamp} for d in data]

