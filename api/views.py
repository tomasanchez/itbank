from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from branches.models import Branch, Address
from prestamos.models import Prestamo
from tarjetas.models import Tarjeta
from .serializers import UserSerializer, PrestamoSerializer, BranchSerializer, TarjetaSerializer, \
    PrestamoCreateSerializer, AddressSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    lookup_field = 'username'
    allowed_methods = ['GET']
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'],
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[IsAuthenticated]
            )
    def me(self, request):
        serializer = self.get_serializer(request.user, many=False)
        return Response(serializer.data)

    @action(detail=True, methods=['get'],
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def cards(self, request, username=None):
        serializer_class = TarjetaSerializer
        if username is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if username == 'me':
            user = request.user
        else:
            if not request.user.is_staff and request.user.employee is None:
                return Response({'status': "You don't have enough permissions."}, status=status.HTTP_403_FORBIDDEN)
            user = User.objects.get(username=username)

        cards = user.tarjeta_set.filter(type=Tarjeta.CardType.CREDIT.value)
        serializer = serializer_class(cards, many=True)
        return Response(serializer.data)


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'pk'
    allowed_methods = ['GET', 'PUT']
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk):

        if not request.user.is_staff and request.user.employee is None:
            query = request.user.cliente.address
        else:
            query = Address.objects

        try:
            address = query.get(pk=pk)
            serializer = AddressSerializer(address, many=False)
            return Response(serializer.data)
        except Address.DoesNotExist:
            return Response({'status': 'Address does not exists'}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk):

        if not request.user.is_staff and request.user.employee is None:
            query = request.user.cliente.address
        else:
            query = Address.objects

        try:
            address = query.get(pk=pk)
        except Address.DoesNotExist:
            return Response({'status': 'Address does not exists'}, status=status.HTTP_404_NOT_FOUND)

        address_serializer = AddressSerializer(address, data=request.data)

        if address_serializer.is_valid():
            address_serializer.update(instance=address, validated_data=request.data)
            return Response(address_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BranchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    lookup_field = 'pk'
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        if not request.user.is_staff and request.user.employee is None:
            return Response({'status': "You don't have enough permissions."}, status=status.HTTP_403_FORBIDDEN)
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

    @action(detail=True, methods=['get'],
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[IsAuthenticated])
    def loans(self, request, pk=None):

        if pk is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_staff or request.user.employee is not None:
            try:
                Branch.objects.get(pk=pk)
                loans = Prestamo.objects.prefetch_related('customer').filter(customer__branch__pk=pk)
                serializer = PrestamoSerializer(loans, many=True)
                return Response(serializer.data)
            except Branch.DoesNotExist:
                return Response({'status': 'No branch found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'status': "You don't have enough permissions."}, status=status.HTTP_403_FORBIDDEN)


class CardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tarjeta.objects.filter(type=Tarjeta.CardType.CREDIT.value)
    serializer_class = TarjetaSerializer
    lookup_field = 'pk'
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        if not request.user.is_staff and request.user.employee is None:
            return Response({'status': "You don't have enough permissions."}, status=status.HTTP_403_FORBIDDEN)
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

    def retrieve(self, request, pk):
        if not request.user.is_staff and request.user.employee is None:
            return Response({'status': "You don't have enough permissions."}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, pk)


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


def add_loan(request):
    serializer = PrestamoCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_loan(request, pk):
    if not request.user.is_staff and request.user.employee is None:
        query = request.user.cliente.prestamo_set
    else:
        query = Prestamo.objects

    try:
        loan = query.get(pk=pk)
        serializer = PrestamoSerializer(loan, many=False)
        return Response(serializer.data)
    except Prestamo.DoesNotExist:
        return Response({'status': 'No loan found'}, status=status.HTTP_404_NOT_FOUND)


def get_loans(request):
    loans = Prestamo.objects.all()
    serializer = PrestamoSerializer(loans, many=True)
    return Response(serializer.data)


def delete_loan(request, pk):
    if not request.user.is_staff and request.user.employee is None:
        try:
            loan = request.user.cliente.prestamo_set.get(pk=pk)
        except Prestamo.DoesNotExist:
            return Response({'status': 'Requested LoanLoan does not exists'}, status=status.HTTP_404_NOT_FOUND)
    else:
        try:
            loan = Prestamo.objects.get(pk=pk)
        except Prestamo.DoesNotExist:
            return Response({'status': 'Loan does not exists'}, status=status.HTTP_404_NOT_FOUND)

    loan.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', ])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated, ])
def loans_data(request):
    if not request.user.is_staff and request.user.employee is None:
        return Response({'status': "You don't have enough permissions."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        return get_loans(request)
    elif request.method == 'POST':
        return add_loan(request)
    else:
        return Response({'status': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def loan_data(request, pk):
    if request.method == 'GET':
        return get_loan(request, pk)
    elif request.method == 'DELETE':
        return delete_loan(request, pk)
    else:
        return Response({'status': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
