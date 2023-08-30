from django.shortcuts import render, redirect
from .forms import RegisterForm, PostForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Post
from django.views import View
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt  # Import the csrf_exempt decorator
from .models import CapturedPicture, WeightHistory
from main.coweightRoboYolo import pesaje
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

def takePicture(request):
    if request.method == 'POST':
        cam = cv2.VideoCapture(0)

        ret, frame = cam.read()

        img_counter = 0

        if not ret:
            print("failed to grab frame")
            return JsonResponse({'message': 'failed to grab frame'})

        img_name = "cowImage.jpg"
        cv2.imwrite(img_name, frame)

        values = pesaje(img_name)

        insert_weight = WeightHistory(user=request.user, weight=values['weight'])
        insert_weight.save()

    return JsonResponse({'message': 'Imagen guardada correctamente', 'values': values})

class webcam_view(View):
    @csrf_exempt  # Apply the csrf_exempt decorator
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
        
    def post(self, request, *args, **kwargs):
        image_data = request.FILES.get('image')   # Assuming you're sending the image via a POST request
        print(image_data)
        user = request.user

        captured_picture = CapturedPicture(user=user, image=image_data)
        captured_picture.save()

        #values = 1
        values = pesaje(image_data.name)
        weight_str = str(values['weight'])

        insert_weight = WeightHistory(user=request.user, weight=values['weight'])
        insert_weight.save()

        return JsonResponse({'message': 'Imagen guardada correctamente ' + weight_str, 'values': values})

    
     