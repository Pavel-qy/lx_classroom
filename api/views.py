from rest_framework import decorators, response, reverse


@decorators.api_view(['GET'])
def api_root(request):
    return response.Response({
        'swagger-ui': reverse.reverse('swagger-ui', request=request),
        'register': reverse.reverse('register', request=request),
        'login': reverse.reverse('token_obtain_pair', request=request),
        'login/refresh': reverse.reverse('token_refresh', request=request),
        'users': reverse.reverse('users', request=request),
        'courses': reverse.reverse('courses', request=request),
        'lectures': reverse.reverse('lectures', request=request),
        'hometasks': reverse.reverse('hometasks', request=request),
        'homeworks': reverse.reverse('homeworks', request=request),
        'comments': reverse.reverse('comments', request=request),
    })
