# myapp/views.py
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from manager.models import Book, BookUser,  MyBook


from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse, HttpResponse
import json

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login,logout 
from rest_framework.authtoken.models import Token

# if request.method=='POST':
#         username=request.POST.get('username')
#         password = request.POST.get('password')
#         print(username,password)
#         user = authenticate(request, username=username,password=password)

# @csrf_exempt
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def book_list(request):
#     print(request.method)
#     if request.method == 'GET':
#         books = list(Book.objects.all().values('book_categories__name', 'title', 'author', 'image'))
#         return JsonResponse({'books': books}, safe=False)
#     elif request.method == 'POST':
#         data = json.loads(request.body)
#         Book.objects.create(**{"title": data['book'], "author": data['author']})
#         return HttpResponse({"response": "Good"}, content_type="application/json")
#     else:
#         print("entered here")
#         return HttpResponse({"response": "BAD"}, content_type="application/json")



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def book_list(request):
    authorization_header = request.META.get('HTTP_AUTHORIZATION')
    if not authorization_header:
        return JsonResponse({'error': 'Token not provided'}, status=401) 
    try:
        _, token = authorization_header.split()
        if request.method == 'GET': 
            token = Token.objects.get(key=token)
            user = token.user
            # Check if the user is authenticated
            if user is not None:
                # User is not authenticated, return a 401 Unauthorized response
                books = list(Book.objects.all().values('book_categories__name', 'title', 'author', 'image',  'pk'))
                print(books)
                return JsonResponse({'detail': books}, status=200)
                # return HttpResponse({'detail': str(books)}, content_type="application/json", status=200)
            else:
                return JsonResponse({'status': "BAD"}, status=400)
        elif request.method == 'POST':
            data = json.loads(request.body)
            Book.objects.create(**{"title": data['book'], "author": data['author']})
            return JsonResponse({"response": "Good"}, content_type="application/json")
        else:
            print("entered here")
            return JsonResponse({"response": "Request not idetifieed"}, content_type="application/json")        
    except ValueError:
        return JsonResponse({'error': 'Invalid Authorization header'}, status=401)

    # Your view logic here

# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def book_list(request):
#     print(request.method)
#     if request.method == 'GET':
#         books = list(Book.objects.all().values('book_categories__name', 'title', 'author', 'image'))
#         return JsonResponse({'books': books}, safe=False)
#     elif request.method == 'POST':
#         data = json.loads(request.body)
#         Book.objects.create(**{"title": data['book'], "author": data['author']})
#         return HttpResponse({"response": "Good"}, content_type="application/json")
#     else:
#         print("entered here")
#         return HttpResponse({"response": "BAD"}, content_type="application/json")





@csrf_exempt
def User_List(request):
    print(request.method)
    if request.method == 'POST':
        data = json.loads(request.body)
        user = User.objects.create(**{'username': data['email'], 'email': data['email'], 'first_name': data['name']})
        user.set_password(data['password'])
        user.save()
        BookUser.objects.create(**{"user": user, "address": data['address'], "college": data['college'], "phone":data['phone']  })
        return JsonResponse({"response": "Good"}, content_type="application/json")



@api_view(['POST'])
@permission_classes([AllowAny])  # Allow unauthenticated users to access this view
def custom_login(request):
    # Authenticate the user
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request,username=username, password=password)
    print("entered here ----", user)
    # if user is not None:
    #     # Generate a JWT token
    #     token = TokenObtainPairView.as_view()(request).data
    #     return Response(token)
    # else:
    #     return Response({'detail': 'Invalid credentials'}, status=401)
    if user is not None:
        # Generate a JWT token using TokenObtainPairView
        # token_view = TokenObtainPairView.as_view()
        # token_response = token_view(request).data  # Pass the request object
        token, created = Token.objects.get_or_create(user=user)
        print(token)
        data = {"data": {"token": str(token.key)}}
        return JsonResponse(data, content_type='application/json', status=200)
    else:
        return JsonResponse({'detail': 'Invalid credentials'}, status=401)



@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def My_list(request):
    authorization_header = request.META.get('HTTP_AUTHORIZATION')
    if not authorization_header:
        return JsonResponse({'error': 'Token not provided'}, status=401) 
    try:
        _, token = authorization_header.split()
        token = Token.objects.get(key=token)
        user = token.user
        if request.method == 'GET': 
            # Check if the user is authenticated
            if user is not None:
                # User is not authenticated, return a 401 Unauthorized response
                books = list(MyBook.objects.filter(book_user__user=user).values(
                    'book__book_categories__name', 'book__title', 'book__author', 'image'))
                print(books)
                return JsonResponse({'detail': books}, status=200)
                # return HttpResponse({'detail': str(books)}, content_type="application/json", status=200)
            else:
                return JsonResponse({'status': "BAD"}, status=400)
        elif request.method == 'POST':
            data = json.loads(request.body)
            book_user = BookUser.objects.get(user=user)
            MyBook.objects.create(**{"book_user": book_user, "book_id": data['book_id']})
            return JsonResponse({"response": "Good"}, content_type="application/json")
        else:
            vfprint("entered here")
            return JsonResponse({"response": "Request not idetifieed"}, content_type="application/json")        
    except ValueError:
        return JsonResponse({'error': 'Invalid Authorization header'}, status=401)