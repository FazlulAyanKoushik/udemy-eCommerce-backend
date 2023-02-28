
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import Http404
from rest_framework import status

from rest_framework.views import APIView

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.hashers import make_password

from account.models import UserProfile
from .serializers import UserSerializer, UserSerializerWithToken



# Create your views here.
# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#
#         # refresh = self.get_token(self.user)
#         data["email"] = self.user.email
#         data["first_name"] = self.user.first_name
#         data["last_name"] = self.user.last_name
#         return data

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # refresh = self.get_token(self.user)
        serializer = UserSerializerWithToken(self.user).data

        for k,v in serializer.items():
            data[k] = v
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Function Based Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    data = request.data

    '''
        CUSTOMIZED NAME PARTS START
    '''
    first_name, last_name = divide_name_parts(data["name"], user.email)
    '''
        CUSTOMIZED NAME PARTS END
    '''

    user.first_name = first_name
    user.last_name = last_name

    if data['password'] != "":
        user.password = make_password(data["password"])
    user.save()
    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getAllUserProfile(request):
    users = UserProfile.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def registerUser(request):
    data = request.data

    '''
        CUSTOMIZED NAME PARTS START
    '''
    first_name, last_name = divide_name_parts(data["name"], data["email"])
    '''
        CUSTOMIZED NAME PARTS END
    '''

    try:
        user = UserProfile.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=data["email"],
            password=make_password(data["password"])
        )

        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        # print("django.db.IntegrityError as e : ",e)
        message = {'details': 'User with this email already exist'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = UserProfile.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


# class Based Views
@permission_classes([IsAuthenticated])
class UserProfileView(APIView):
    def get(self, request, format=None):
        user = request.user
        if user.is_anonymous:
            return Response({'error': 'Unauthorized'}, status=401)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data

        '''
            CUSTOMIZED NAME PARTS START
        '''
        first_name, last_name =divide_name_parts(data["name"], data["email"])
        '''
            CUSTOMIZED NAME PARTS END
        '''

        try:
            user = UserProfile.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=data["email"],
                password=make_password(data["password"])
            )

            serializer = UserSerializerWithToken(user, many=False)
            return Response(serializer.data)
        except:
            # print("django.db.IntegrityError as e : ",e)
            message = {'details': 'User with this email already exist'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
class UserProfileDetails(APIView):
    def put(self, request, format=None):
        user = request.user
        data = request.data

        '''
            CUSTOMIZED NAME PARTS START
        '''
        first_name, last_name = divide_name_parts(data["name"], user.email)
        '''
            CUSTOMIZED NAME PARTS END
        '''

        user.first_name = first_name
        user.last_name = last_name

        if data['password'] != "":
            user.password = make_password(data["password"])
        user.save()
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)




@permission_classes([IsAdminUser])
class AllUserProfileView(APIView):
    def get(self, request, format=None):
        users = UserProfile.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)



def divide_name_parts(name, email):
    full_name = name
    name_parts = full_name.split(" ")
    num_parts = len(name_parts)
    first_name = ""
    last_name = ""
    if num_parts == 0:
        first_name = email
    if num_parts == 1:
        first_name = name_parts[0]
    if num_parts == 2:
        first_name, last_name = name_parts[0], name_parts[1]
    if num_parts > 2:
        first_name, last_name = " ".join(name_parts[:-1]), name_parts[-1]

    return first_name, last_name


permission_classes([IsAdminUser])
class GetUserByAdminView(APIView):
    def get_object(self, pk):
        try:
            return UserProfile.objects.get(id=pk)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        data = request.data

        '''
            CUSTOMIZED NAME PARTS START
        '''
        first_name, last_name = divide_name_parts(data["name"], user.email)
        '''
            CUSTOMIZED NAME PARTS END
        '''

        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = data['isAdmin']
        user.save()

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        user=self.get_object(pk)
        user.delete()
        return Response("User deleted successfully")








