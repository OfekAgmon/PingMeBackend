from django.http import HttpResponseBadRequest
from rest_framework import mixins
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import list_route
from rest_framework.views import APIView
from pingme.serializers import UserSerializer, DeviceSerializer, LocationSerializer
from pingme.permissions import IsCreationOrIsAuthenticated
from pingme.models import Device, Location
from rest_framework import status, parsers, renderers
from rest_framework import permissions
from rest_framework.response import Response



# Create your views here.

class UserViewSet(mixins.CreateModelMixin,
               mixins.RetrieveModelMixin,
               mixins.ListModelMixin,
               viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsCreationOrIsAuthenticated,)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.action == 'list':
            return Location.objects.exclude(user=self.request.user)
        else:
            return Location.objects.all()

    def perform_create(self, serializer):
        try:
            first_location = Location.objects.get(user=self.request.user)
        except Location.DoesNotExist:
            first_location = None
        if first_location is None:
            # first location
            serializer.save(user=self.request.user)
            return Response(serializer.data)
        else:
            return Response("location already exists", status=status.HTTP_400_BAD_REQUEST)



class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    @list_route(methods=['put'], permission_classes=[permissions.IsAuthenticated],)
    def freeUser(self, request):
        try:
            device = Device.objects.get(user=self.request.user)
        except Device.DoesNotExist:
            device = None
        if device is None:
            return HttpResponseBadRequest()
        else:
            device.user = None
            device.save()
            return Response(status=status.HTTP_200_OK)


class ObtainAuthTokenAndUser(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            # wrong username or password
            # return HttpResponseBadRequest("Wrong username or password")
            return HttpResponseBadRequest("שם משתמש או סיסמא לא נכונים")
        user = serializer.validated_data['user']
        try:
            device_used = Device.objects.get(user=user)
        except Device.DoesNotExist:
            # user is logged in from another device
            device_used = None
        if device_used == None:
            # user is not logged in currently, login is OK, attach user to Device
            token, created = Token.objects.get_or_create(user=user)
            user_serializer = UserSerializer(user)
            dev_id = request.DATA.get('device_id', '0')
            device = Device.objects.get(device_id=dev_id)
            device.user = user
            device.save()
            return Response({'token': token.key, 'user': user_serializer.data})

        else:
            # return HttpResponseBadRequest("User is logged in from another device")
            return HttpResponseBadRequest("משתמש מחובר ממכשיר אחר")

obtain_auth_token_and_user = ObtainAuthTokenAndUser.as_view()

