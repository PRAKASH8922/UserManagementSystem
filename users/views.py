import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .models import CtUserDetails


# Template Views
def index_view(request):
    """Render Dashboard Page."""
    return render(request, 'index.html')


def login_view(request):
    """Render Login Page."""
    return render(request, 'login.html')


def signup_view(request):
    """Render Signup Page."""
    return render(request, 'signup.html')


# REST API Views
@csrf_exempt
def user_list_create(request):
    """
    GET: Return all users as JSON.
    POST: Create a new user with securely hashed password and return HTTP 201.
    """
    if request.method == 'GET':
        users = CtUserDetails.objects.all().order_by('id')
        data = [
            {
                'id': user.id,
                'name': user.name,
                'phone': user.phone,
                'email': user.email,
            }
            for user in users
        ]
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        try:
            payload = json.loads(request.body.decode('utf-8'))
            name = payload.get('name', '').strip()
            phone = payload.get('phone', '').strip()
            email = payload.get('email', '').strip()
            password = payload.get('password', '').strip()

            if not name or not phone or not email or not password:
                return JsonResponse({'error': 'All fields are required'}, status=400)

            if CtUserDetails.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already registered'}, status=400)

            user = CtUserDetails.objects.create(
                name=name,
                phone=phone,
                email=email,
                password=make_password(password)
            )

            return JsonResponse({
                'id': user.id,
                'name': user.name,
                'phone': user.phone,
                'email': user.email,
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def user_detail(request, user_id):
    """
    PUT: Update user details. Password is only updated if provided.
    DELETE: Delete user by id.
    """
    try:
        user = CtUserDetails.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({'error': 'User not found'}, status=404)

        if request.method == 'PUT':
            payload = json.loads(request.body.decode('utf-8'))
            if 'name' in payload:
                user.name = payload['name'].strip()
            if 'phone' in payload:
                user.phone = payload['phone'].strip()
            if 'email' in payload:
                user.email = payload['email'].strip()
            if payload.get('password'):
                user.password = make_password(payload['password'].strip())

            user.save()

            return JsonResponse({
                'id': user.id,
                'name': user.name,
                'phone': user.phone,
                'email': user.email,
            }, status=200)

        elif request.method == 'DELETE':
            user.delete()
            return HttpResponse(status=204)

        return JsonResponse({'error': 'Method not allowed'}, status=405)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def user_login(request):
    """
    POST: Validate user credentials against ct_user_details.
    Returns matched user array or empty array [] matching original API behavior.
    """
    if request.method == 'POST':
        try:
            payload = json.loads(request.body.decode('utf-8'))
            email = payload.get('email', '').strip()
            password = payload.get('password', '').strip()

            user = CtUserDetails.objects.filter(email=email).first()
            if user:
                is_valid = False
                if check_password(password, user.password):
                    is_valid = True
                elif user.password == password:
                    # Upgrade legacy plaintext password to secure hash
                    user.password = make_password(password)
                    user.save(update_fields=['password'])
                    is_valid = True

                if is_valid:
                    return JsonResponse([
                        {
                            'id': user.id,
                            'name': user.name,
                            'email': user.email,
                        }
                    ], safe=False)

            return JsonResponse([], safe=False)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON body'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)
