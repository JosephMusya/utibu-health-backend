from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CartItem, Dosage, Order
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name', 'address']
class DosageSerializer(serializers.ModelSerializer):
    instock = serializers.SerializerMethodField()
    class Meta:
        model = Dosage
        fields ='__all__'
        
    def get_instock(self, obj):
        if (obj.qty > 0):
            return True
        return False

class CartSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', required=False)
    dosage = DosageSerializer(required=False)
    # total = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields ="__all__"
        extra_kwargs = {'dosage': {'required': False}}

        
    def get_total(self, obj):
        total_items = 0
        cart_items = obj.cart_item.all()
        for item in cart_items:
            total_items += item.dosage.qty
        return total_items

class OrderSerializer(serializers.ModelSerializer):
    cart_item =CartSerializer(many=True, read_only=False)
    user = serializers.CharField(source='user.username')
    class Meta:
        model = Order
        fields = '__all__'
        
class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    class Meta:
        model = Order
        fields = '__all__'
        
class PostCartSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    class Meta:
        model = CartItem
        fields = '__all__'
        
class RegisterSerializer(serializers.ModelSerializer):

    password_1 = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password],
    )
    password_2 = serializers.CharField(
        write_only=True, 
        required=True
    )

    class Meta:
        model=User
        fields = (
            'username','password_1','password_2','address','first_name','last_name'
        )
    
    def validate(self, attrs):
        if attrs['password_1'] != attrs['password_2']:
            raise serializers.ValidationError({
                'password_error':"Passwords did not match"
            })
        return attrs
    
    def create(self, validated_data):
        print("Creatin,,,")
        user = User.objects.create(
            username=validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            address = validated_data['address']
        )
        # user.address(validated_data['address'])

        user.set_password(validated_data['password_1'])
        user.save()

        return user