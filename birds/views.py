from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Birds
from .serializers import BirdsSerializer


class BirdsView(APIView):
    def get(self, request):
        birds = Birds.objects.all()
        serializer = BirdsSerializer(birds, many=True)
        return Response({"birds": serializer.data})

    def post(self, request):
        bird = request.data

        serializer = BirdsSerializer(data=bird)
        if serializer.is_valid(raise_exception=True):
            bird_saved = serializer.save()
        return Response({"success": "Bird '{}' created successfully".format(bird_saved.name)})


class SingleBirdsView(APIView):
    def get(self, request, name):
        bird = get_object_or_404(Birds.objects.all(), name=name)
        serializer = BirdsSerializer(bird)
        return Response({"birds": serializer.data})

    def put(self, request, name):
        saved_bird = get_object_or_404(Birds.objects.all(), name=name)
        data = request.data
        serializer = BirdsSerializer(instance=saved_bird, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            bird_saved = serializer.save()

        return Response({"success": "Bird '{}' updated successfully".format(bird_saved.name)})

    def delete(self, request, name):
        bird = get_object_or_404(Birds.objects.all(), name=name)
        bird.delete()
        return Response({"success": "Bird '{}' has been deleted".format(name)}, status=204)
