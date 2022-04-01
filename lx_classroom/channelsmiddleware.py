from django.db import close_old_connections
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from decouple import config
from django.contrib.auth import get_user_model
from urllib.parse import parse_qs
from channels.db import database_sync_to_async


@database_sync_to_async
def get_user(user_id):
    return get_user_model().objects.get(id=user_id)


class TokenAuthMiddleware:
    def __init__(self, inner):
        # store the ASGI application we were passed
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # check if the user has authenticated before
        if not scope['user']._wrapped.is_anonymous:
            return await self.inner(scope, receive, send)
            
        # close ol database connections to prevent usage of timed out connections
        close_old_connections()

        # get the token
        try:
            token = parse_qs(scope['query_string'].decode('utf8'))['token'][0]
        except KeyError as exc:
            print('You must be authenticated or request must contain a token!')
            return None

        # try to authenticate the user
        try:
            # validate the token and raise an error if token is invalid
            UntypedToken(token)
        except (InvalidToken, TokenError) as exc:
            print(exc)
            return None
        else:
            # decode token
            decoded_data = jwt_decode(token, config('SECRET_KEY'), algorithms=['HS256'])

            # get the user using ID
            user = await get_user(decoded_data['user_id'])
        
        # return the inner application directly and let it run everything else
        return await self.inner(dict(scope, user=user), receive, send)
