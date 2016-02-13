from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def default_process_list_request(request, serializer_class, object_class):
    from rest_framework.parsers import JSONParser
    if request.method == 'GET':
        objects = object_class.objects.all()
        serializer = serializer_class(objects, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


def default_process_detail_request(request, serializer_class, object_instance):
    from rest_framework.parsers import JSONParser
    if request.method == 'GET':
        serializer = serializer_class(object_instance)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = serializer_class(object_instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        object_instance.delete()
        return HttpResponse(status=204)