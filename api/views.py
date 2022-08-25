from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from branches.models import Branch
from prestamos.models import Prestamo
from tarjetas.models import Tarjeta
from .serializers import UserSerializer, PrestamoSerializer, BranchSerializer, TarjetaSerializer


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def customer_data(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def customer_me_data(request):
    try:
        user = User.objects.get(pk=request.user.pk)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'status': 'User does not exists'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
def loans_data(request):
    loans = Prestamo.objects.all()
    serializer = PrestamoSerializer(loans, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def loan_data(request, pk):
    try:
        loan = Prestamo.objects.get(pk=pk)
        serializer = PrestamoSerializer(loan, many=False)
        return Response(serializer.data)
    except Prestamo.DoesNotExist:
        return Response({'status': 'No loan found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def branches_data(request):
    if not request.user.is_staff and request.user.employee is None:
        return Response({'status': "You don't have enough permissions."}, status=status.HTTP_403_FORBIDDEN)

    branches = Branch.objects.all()
    serializer = BranchSerializer(branches, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def branch_data(request, pk):
    if not request.user.is_staff and request.user.employee is None:
        return Response({'status': "You don't have enough permissions."}, status=status.HTTP_403_FORBIDDEN)

    try:
        loans = Prestamo.objects.prefetch_related('customer').filter(customer__branch__pk=pk)
        serializer = PrestamoSerializer(loans, many=True)
        return Response(serializer.data)
    except Branch.DoesNotExist:
        return Response({'status': 'No branch found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def cards_data(request):
    if not request.user.is_staff and request.user.employee is None:
        return Response({'status': "You don't have enough permissions."}, status=status.HTTP_403_FORBIDDEN)

    credit_cards = Tarjeta.objects.filter(type=Tarjeta.CardType.CREDIT)
    serializer = TarjetaSerializer(credit_cards, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def user_data(request, username):
    if not request.user.is_staff and request.user.employee is None:
        return Response({'status': "You don't have enough permissions."}, status=status.HTTP_403_FORBIDDEN)
    try:
        user = User.objects.get(username=username)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'status': 'User does not exists'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def cards_customer_data(request, username):
    if not request.user.is_staff and request.user.employee is None:
        return Response({'status': "You don't have enough permissions."}, status=status.HTTP_403_FORBIDDEN)

    try:
        credit_cards = User.objects.get(username=username).tarjeta_set.filter(type=Tarjeta.CardType.CREDIT)
        serializer = TarjetaSerializer(credit_cards, many=True)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'status': 'User does not exists'}, status=status.HTTP_404_NOT_FOUND)



