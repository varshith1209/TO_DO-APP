from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import taskserializer
from .models import tasks
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# -------------------------------
# APIView with caching
# -------------------------------
class taskAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cache_key = f'tasks_user_{request.user.id}'
        data = cache.get(cache_key)

        if not data:
            task = tasks.objects.filter(user=request.user)
            serializer = taskserializer(task, many=True)
            data = serializer.data
            cache.set(cache_key, data, 60*5)  # cache for 5 minutes

        return Response(data)

    def post(self, request):
        serializer = taskserializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            # Invalidate cache after adding a new task
            cache.delete(f'tasks_user_{request.user.id}')
            return Response({'message':'Successfully posted tasks'}, status=status.HTTP_201_CREATED)
        return Response({'message':'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------
# ViewSet with caching
# -------------------------------
class taskviewset(viewsets.ModelViewSet):
    serializer_class = taskserializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        'completed': ['exact'],             # ?completed=true
        'created_at': ['gte','lte'],        # ?created_at__gte=2025-09-01
    }
    search_fields = ['title','description']

    # Cache the queryset per user
    def get_queryset(self):
        user = self.request.user
        cache_key = f'todos_user_{user.id}'
        todos = cache.get(cache_key)

        if not todos:
            todos = list(user.todos.all())  # convert queryset to list for caching
            cache.set(cache_key, todos, 60*5)  # cache for 5 minutes

        return todos

    # Invalidate cache on create
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        cache.delete(f'todos_user_{self.request.user.id}')

    # Optional: cache the list response for faster GET API
    @method_decorator(cache_page(60*5), name='list')
    class Meta:
        pass
