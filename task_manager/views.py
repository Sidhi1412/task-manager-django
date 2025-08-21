from graphene_django.views import GraphQLView
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser

class PrivateGraphQLView(GraphQLView):
    def dispatch(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                # Expect "Authorization: Token <token>"
                scheme, token_key = auth_header.split(' ', 1)
                if scheme.lower() == 'token':
                    token = Token.objects.get(key=token_key.strip())
                    request.user = token.user
                else:
                    request.user = AnonymousUser()
            except Exception:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()

        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required.'}, status=401)
        return super().dispatch(request, *args, **kwargs)
