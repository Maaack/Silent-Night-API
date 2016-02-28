from django.http import HttpResponse, Http404
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def default_process_list_request(request, serializer_class, object_class):
    if request.method == 'GET':
        objects = object_class.objects.all()
        serializer = serializer_class(objects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def default_process_detail_request(request, serializer_class, object_instance):
    if request.method == 'GET':
        serializer = serializer_class(object_instance)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = serializer_class(object_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        object_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BaseListView(APIView):
    """
    List all object instances, or create a new object instance.
    """
    object_class = None
    serializer_class = None
    permission_classes = (AllowAny,)

    class Meta:
        abstract = True

    def get(self, request, format=None):
        if self.object_class is None or self.serializer_class is None:
            if self.object_class is None:
                return Response('No object_class defined', status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response('No serializer_class defined', status=status.HTTP_400_BAD_REQUEST)

        object_instances = self.object_class.objects.all()
        serializer = self.serializer_class(object_instances, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if self.serializer_class is None:
            return Response('No serializer_class defined', status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseDetailView(APIView):
    """
    Retrieve, update or delete an object instance.
    """
    object_class = None
    serializer_class = None
    permission_classes = (AllowAny,)

    class Meta:
        abstract = True

    def get_object(self, pk):
        if self.object_class is None:
            return Response('No object_class defined', status=status.HTTP_400_BAD_REQUEST)
        try:
            return self.object_class.objects.get(pk=pk)
        except self.object_class.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if self.serializer_class is None:
            return Response('No serializer_class defined', status=status.HTTP_400_BAD_REQUEST)
        object_instance = self.get_object(pk)
        serializer = self.serializer_class(object_instance)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        if self.serializer_class is None:
            return Response('No serializer_class defined', status=status.HTTP_400_BAD_REQUEST)
        object_instance = self.get_object(pk)
        serializer = self.serializer_class(object_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        object_instance = self.get_object(pk)
        object_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)