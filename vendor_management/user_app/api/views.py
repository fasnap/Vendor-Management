from django.http import HttpResponse
from rest_framework.decorators import api_view
from user_app.api.serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from user_app import models

@api_view(['POST',])
def registration_view(request):
    
    if request.method == 'POST': 
        serializer = RegistrationSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account=serializer.save()
            data['response']="registration successfull"
            data['username']=account.username
            data['email']=account.email
            # These below commented two lines were used in Token authentication to pass token along with user data while registration.
            token = Token.objects.get(user=account).key
            data['token']=token
            
        else:
            data=serializer.errors
        return Response(data)
    
@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response("logout")