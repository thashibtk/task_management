from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Task, User
from .serializers import TaskSerializer, TaskReportSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .tokens import MyTokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from django.shortcuts import render, redirect

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# New endpoint to get current user info
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user_data = {
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'role': request.user.role,
    }
    return Response(user_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_tasks(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task_status(request, pk):
    try:
        task = Task.objects.get(pk=pk, assigned_to=request.user)
    except Task.DoesNotExist:
        return Response({"error": "Task not found or unauthorized."}, status=status.HTTP_404_NOT_FOUND)

    status_value = request.data.get('status')
    completion_report = request.data.get('completion_report')
    worked_hours = request.data.get('worked_hours')

    if status_value == "completed":
        if not completion_report or worked_hours is None:
            return Response(
                {"error": "Completion report and worked hours are required when marking as completed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        task.completion_report = completion_report
        task.worked_hours = worked_hours

    task.status = status_value
    task.save()
    return Response({"message": "Task updated successfully."})


def task_report_page(request, pk):
    return render(request, 'task_report.html')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_task_report(request, pk):
    user = request.user

    try:
        task = Task.objects.get(pk=pk, status='completed')
    except Task.DoesNotExist:
        return Response({"error": "Completed task not found."}, status=status.HTTP_404_NOT_FOUND)

    if user.role == 'superadmin':
        pass  
    elif user.role == 'admin':
        if not (
            task.assigned_to and task.assigned_to.assigned_admin == user
        ) and task.created_by != user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        if task.assigned_to and task.assigned_to != user:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = TaskReportSerializer(task)
    return Response(serializer.data)



def login_page(request):
    return render(request, 'login.html')


User = get_user_model()

def has_admin_permission(user):
    return user.is_authenticated and user.role in ['superadmin', 'admin']

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_list_create(request):
    user = request.user

    # Allow only SuperAdmins
    if user.role != 'superadmin':
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        role = request.GET.get('role')
        users = User.objects.all()
        if role:
            users = users.filter(role=role)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    user = request.user

    if user.role != 'superadmin':
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
def manage_users_page(request):
    return render(request, 'users.html')

def manage_admin_page(request):
    return render(request, 'admin.html')

def manage_tasks_page(request):
    return render(request, 'tasks.html')

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_list_create(request):
    user = request.user

    # Allow only superadmin and admin
    if user.role == 'user':
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        if user.role == 'superadmin':
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(
                assigned_to__assigned_admin=user
            ) | Task.objects.filter(
                created_by=user
            )
            tasks = tasks.distinct()

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_load_users(request):
    user = request.user

    if user.role != 'admin':
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    users = User.objects.filter(role='user', assigned_admin=user)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


def admin_task(request):
    return render(request, 'admin_tasks.html')

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail(request, pk):
    if not has_admin_permission(request.user):
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response({'detail': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

def user_task_dashboard(request):
    return render(request, 'user_tasks.html')

def index(request):
    return render(request, 'index.html')