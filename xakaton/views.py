from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Hackathon
import json
from django.core.serializers import serialize
from django.forms.models import model_to_dict

def is_admin(user):
    return user.is_staff

def xaki(request):
    hackathons = Hackathon.objects.filter(is_active=True)
    return render(request, 'xakaton/xaki.html', {'hackathons': hackathons})

def aboutproject(request):
    return render(request, 'xakaton/aboutproject.html')

def registcommand(request):
    return render(request, 'xakaton/registcommand.html')

def aboutmirea(request):
    return render(request, 'xakaton/aboutmirea.html')

def aboutcommand(request):
    return render(request, 'xakaton/aboutcommand.html')

def teamaccept(request):
    return render(request, 'xakaton/teamaccept.html')

def createteam(request):
    return render(request, 'xakaton/createteam.html')

@login_required
@user_passes_test(is_admin)
def admin_hack(request):
    hackathons = Hackathon.objects.all()
    return render(request, 'users/adminHack.html', {'hackathons': hackathons})

# API Views
@login_required
@user_passes_test(is_admin)
@csrf_exempt
def hackathon_list(request):
    if request.method == 'GET':
        hackathons = Hackathon.objects.all()
        return JsonResponse([model_to_dict(h) for h in hackathons], safe=False)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            hackathon = Hackathon.objects.create(
                title=data['title'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                format=data['format'],
                prize_fund=data['prize_fund'],
                description=data['description']
            )
            return JsonResponse(model_to_dict(hackathon), status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@login_required
@user_passes_test(is_admin)
@csrf_exempt
def hackathon_detail(request, pk):
    hackathon = get_object_or_404(Hackathon, pk=pk)
    
    if request.method == 'GET':
        return JsonResponse(model_to_dict(hackathon))
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            for key, value in data.items():
                setattr(hackathon, key, value)
            hackathon.save()
            return JsonResponse(model_to_dict(hackathon))
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'DELETE':
        hackathon.delete()
        return JsonResponse({}, status=204)

    return JsonResponse({'error': 'Invalid method'}, status=405)

