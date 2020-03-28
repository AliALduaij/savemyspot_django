from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,

)
from rest_framework.views import APIView

from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
)

from .serializers import (
    RestaurantListSerializer,
    QueueCreateSerializer,
    RestaurantDetailSerializer,
    QueueListSerializer


)
from .models import (
    Restaurant,
    Queue,
    RestaurantUser

)
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http import Http404


class RestraurantListView(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantListSerializer


class RestaurauntDetailView(RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'restaurant_id'


class QueueView(APIView):
    def get(self, request):
        obj = request.data
        restaurant = Restaurant.objects.get(id=obj['restaurant'])
        queue = Queue.object.filter(restaurant=restuarant)

        return Response(QueueListSerializer(queue, many=True).data)

    def post(self, request):
        obj = request.data
        user = User.object.get(id=obj['user'])
        restaurant = Restaurant.objects.get(id=obj['restaurant'])
        queue_obj = Queue(user=user, restaurant=restaurant,
                          guests=obj['guests'])
        queue_obj.increment_position()
        queue_obj.save()

        return Response(RestaurantListSerializer(restaurant).data)

    def delete(self, request, queue_id):
        queue = Queue.objects.get(id=queue_id)
        pos = queue.position
        restaurant_queues = queue.restaurant.queues.filter(
            position__gt=pos).order_by('position')
        queue.delete()

        for queue in restaurant_queues:
            queue.position -= 1
            queue.save()

        return Response(RestaurantDetailSerializer(queue.restaurant).data)


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer


class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        my_data = request.data
        serializer = UserLoginSerializer(data=my_data)
        if serializer.is_valid(raise_exception=True):
            valid_data = serializer.data
            return Response(valid_data, status=HTTP_200_OK)
        return Response(serializer.errors, HTTP_400_BAD_REQUEST)
