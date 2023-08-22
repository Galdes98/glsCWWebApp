from django.shortcuts import render, redirect
from .forms import RegisterForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Post
from django.views import View
from django.http import StreamingHttpResponse
import cv2
import threading

# Create your views here.

@login_required(login_url="/login")
def home(request):
    #posts = Post.objects.all()

    # if request.method  == "POST":
    #     post_id = request.POST.get("post-id")
    #     post = Post.objects.filter(id=post_id).first()
    #     if post and post.author == request.user:
    #         post.delete()

    return render(request, 'main/home.html')

@login_required(login_url="/login")
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
    else:
        form = PostForm()
    
    return render(request, 'main/create_post.html', {"form": form})


def sign_up(request):
    if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('/home')

    else:
            form = RegisterForm()
        
    return render(request, 'registration/sign_up.html', {"form": form})

class webcam_view(View):
    def get(self, request, *args, **kwargs):
        def generate_frames():
            cap = cv2.VideoCapture(0)  # 0 indicates the default camera (webcam)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                _, buffer = cv2.imencode('.jpg', frame)
                frame_data = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
        return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')