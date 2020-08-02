from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Birds
from .serializers import BirdsSerializer


class BirdsView(APIView):
    def get(self, request):
        try:
            birds = Birds.objects.all()

            count = birds.count()
            attribute = request.query_params.get('attribute')
            order = request.query_params.get('order', 'asc')
            limit = request.query_params.get('limit', 0)
            offset = request.query_params.get('offset', 0)

            try:
                limit = int(limit)
            except:
                return Response("'limit' must be integer", status=422)
            try:
                offset = int(offset)
            except:
                return Response("'offset' must be integer", status=422)

            if limit < 0:
                return Response("'limit' must be more than 0", status=422)
            if offset < 0:
                return Response("'offset' must be 0 or more", status=422)
            if attribute is not None and attribute not in BirdsSerializer.Meta.fields:
                return Response("'{}' column is not present in db".format(attribute), status=422)
            if order not in ('asc', 'desc'):
                return Response("Unexpected order: '{}'".format(order), status=422)

            if attribute is not None:
                if order == 'desc':
                    attribute = '-' + attribute
                birds = birds.order_by(attribute)

            if offset < count:
                birds = birds[offset:]
            else:
                return Response("No birds were found", status=204)

            if limit > 0:
                birds = birds[0:limit]

            serializer = BirdsSerializer(birds, many=True)
            return Response(serializer.data)

        except Exception as e:
            return Response("Something goes wrong: {}".format(e), status=500)

    def post(self, request):
        try:
            bird = request.data

            serializer = BirdsSerializer(data=bird)
            if serializer.is_valid(raise_exception=True):
                bird_saved = serializer.save()
            return Response({"success": "Bird '{}' created successfully".format(bird_saved.name)})

        except Exception as e:
            return Response("Something goes wrong: {}".format(e), status=500)


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


class VersionView(APIView):
    def get(self, request):
        return Response("Birds Service. Version 0.1")
