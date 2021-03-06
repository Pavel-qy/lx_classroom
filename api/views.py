from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import decorators, response, reverse, serializers


@extend_schema(responses=inline_serializer(
    name='InlineRootSerializer',
    fields={
        'register': serializers.URLField(),
        'login': serializers.URLField(),
        'login/refresh': serializers.URLField(),
        'users': serializers.URLField(),
        'courses': serializers.URLField(),
        'lectures': serializers.URLField(),
        'hometasks': serializers.URLField(),
        'homeworks': serializers.URLField(),
        'comments': serializers.URLField(),
        'swagger-ui': serializers.URLField(),
        'redoc': serializers.URLField(),
    }
))
@decorators.api_view(['GET'])
def api_root(request):
    return response.Response({
        'register': reverse.reverse('register', request=request),
        'login': reverse.reverse('token_obtain_pair', request=request),
        'login/refresh': reverse.reverse('token_refresh', request=request),
        'users': reverse.reverse('users', request=request),
        'courses': reverse.reverse('courses', request=request),
        'lectures': reverse.reverse('lectures', request=request),
        'hometasks': reverse.reverse('hometasks', request=request),
        'homeworks': reverse.reverse('homeworks', request=request),
        'comments': reverse.reverse('comments', request=request),
        'swagger-ui': reverse.reverse('swagger-ui', request=request),
        'redoc': reverse.reverse('redoc', request=request),
    })
