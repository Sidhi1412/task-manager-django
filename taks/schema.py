import graphene
from graphene_django import DjangoObjectType
from django.core.exceptions import PermissionDenied
from .models import Task
from .serializers import TaskSerializer

class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = ("id", "title", "status", "created_at", "assigned_to")

class Query(graphene.ObjectType):
    all_tasks = graphene.List(TaskType)

    def resolve_all_tasks(root, info):
        user = info.context.user
        if not user.is_authenticated:
            raise PermissionDenied("Authentication credentials were not provided")
        return Task.objects.filter(assigned_to=user)

# -------- Mutations reusing DRF Serializer --------
class CreateTask(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        status = graphene.String(required=False)

    ok = graphene.Boolean()
    task = graphene.Field(TaskType)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, title, status=None):
        user = info.context.user
        if not user or not user.is_authenticated:
            raise PermissionDenied("Authentication required")

        data = {"title": title}
        if status is not None:
            data["status"] = status

        serializer = TaskSerializer(data=data, context={"request": info.context})
        if serializer.is_valid():
            task = serializer.save(assigned_to=user)
            return CreateTask(ok=True, task=task, errors=[])
        return CreateTask(ok=False, task=None, errors=[f"{k}: {', '.join(v)}" for k, v in serializer.errors.items()])

class UpdateTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String(required=False)
        status = graphene.String(required=False)

    ok = graphene.Boolean()
    task = graphene.Field(TaskType)
    errors = graphene.List(graphene.String)

    @classmethod
    def mutate(cls, root, info, id, title=None, status=None):
        user = info.context.user
        if not user or not user.is_authenticated:
            raise PermissionDenied("Authentication required")
        try:
            task = Task.objects.get(pk=id, assigned_to=user)
        except Task.DoesNotExist:
            raise PermissionDenied("Not found or not allowed")

        data = {}
        if title is not None:
            data["title"] = title
        if status is not None:
            data["status"] = status

        serializer = TaskSerializer(task, data=data, partial=True, context={"request": info.context})
        if serializer.is_valid():
            task = serializer.save()
            return UpdateTask(ok=True, task=task, errors=[])
        return UpdateTask(ok=False, task=None, errors=[f"{k}: {', '.join(v)}" for k, v in serializer.errors.items()])

class DeleteTask(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        user = info.context.user
        if not user or not user.is_authenticated:
            raise PermissionDenied("Authentication required")
        try:
            task = Task.objects.get(pk=id, assigned_to=user)
        except Task.DoesNotExist:
            raise PermissionDenied("Not found or not allowed")
        task.delete()
        return DeleteTask(ok=True)

class Mutation(graphene.ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
