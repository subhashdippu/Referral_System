from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import User, Referral
from .serializers import UserSerializer, ReferralSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


@api_view(['POST'])
def user_registration(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        referral_code = request.data.get('referral_code', None)
        if referral_code:
            referrer = User.objects.get(referral_code=referral_code)
            Referral.objects.create(referrer=referrer, referred_user=user)
        return Response({'user_id': user.id, 'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_referrals(request):
    user = request.user
    referrals = Referral.objects.filter(referrer=user)
    serializer = ReferralSerializer(referrals, many=True)
    return Response(serializer.data)
