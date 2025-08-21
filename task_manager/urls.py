from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from .views import PrivateGraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),
    path("graphql/", csrf_exempt(PrivateGraphQLView.as_view(graphiql=True))),
]
