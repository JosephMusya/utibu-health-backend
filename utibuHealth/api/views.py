from urllib import response
from django.shortcuts import render
from rest_framework import status, viewsets, generics
from django.contrib.auth.models import User
from .models import CartItem, Dosage, Order
from .serializers import DosageSerializer, OrderCreateSerializer, OrderSerializer, CartSerializer, PostCartSerializer, RegisterSerializer, UserSerializer
from rest_framework.response import Response
# Create your views here.
from rest_framework.permissions import IsAuthenticated, AllowAny

class OrderApiViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    http_method_names = ['get','post']
    queryset = Order.objects.all()
    
    # def list(self, request, *args, **kwargs):
    
    # def get_queryset(self):
    #     user = self.request.user
    #     order = Order.objects.filter(user= user).order_by('-created_at')
        
    #     return order
    
    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            # order = serializer.save()
            data = serializer.data
            print(data)
            user = User.objects.get(username=data['user'])
            order = Order.objects.create(
                user = user,
                delivery_method = data['delivery_method'],
                status = data['status'],
                paid = data['paid']
            )
                                
            cart_item_ids = request.data.get('cart_item',[])
            for cart_item_id in cart_item_ids:
                try:
                    cart_item = CartItem.objects.get(pk=cart_item_id)
                    cart_item.checked = True
                    cart_item.save()
                    order.cart_item.add(cart_item)
                    order.save()
                    # return  Response(status=status.HTTP_201_CREATED)
                except CartItem.DoesNotExist:
                    return Response({"error": f"CartItem with ID {cart_item_id} does not exist."}, status=400)
            
            return Response(serializer.data, status=201)
        else:
            print(serializer.errors)
            return Response({"error": "Can't create order"}, status=status.HTTP_400_BAD_REQUEST)
        
    
    # def perform_create(self, serializer):
        # 

class DosageViewSet(viewsets.ModelViewSet):
    queryset = Dosage.objects.all()
    serializer_class = DosageSerializer
    
class CartViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartSerializer
    http_method_names = ['get','put','post','delete']
    
    def list(self, request, *args, **kwargs):
        # return super().list(request, *args, **kwargs)
    
        cart_items = self.get_queryset().filter(checked=False)
        
        # Serialize the filtered queryset
        serialized_cart = self.get_serializer(cart_items, many=True)
        
        # Return the serialized data in the response
        return Response(serialized_cart.data, status=200)
    
    # filter with user and checked = false
    def create(self, request, *args, **kwargs):
        serializer = PostCartSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.data
            user = User.objects.get(username=data['user'])
            dosage  = Dosage.objects.get(id=data['dosage'])
            cart = CartItem.objects.create(
                user=user,
                dosage=dosage
            )
            return Response(status=201)
        
        else:
            print(serializer.errors)
            return Response(status=400)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes= [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):  
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        user = self.queryset.filter(username=self.request.user)  
        return user    
    
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer