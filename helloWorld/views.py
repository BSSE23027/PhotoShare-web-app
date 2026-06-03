import os
from django.conf import settings
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, get_object_or_404, redirect
from .models import Users, Images
from .forms import ProductImageForm, SignupForm, LoginForm, ProfilePictureForm, ProfileUpdateForm
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from django.core.mail import send_mail
import time
import google.generativeai as genai
GEMINI_API_KEY = "AIzaSyBmbyMdAb5Mnj3_y7c1MqUind738_eeimw"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")



def profile_page(request, user_id):
    user_profile = get_object_or_404(Users, id=user_id)

    session_user = None
    if 'user_id' in request.session:
        session_user = get_object_or_404(Users, id=request.session['user_id'])

    can_edit = session_user and session_user.email == user_profile.email
    images = user_profile.images.all().order_by('-id')

    return render(
        request,
        'profile_page.html',
        {
            'user_profile': user_profile,
            'images': images,
            'can_edit': can_edit
        }
    )



def edit_profile(request, user_id):
    user_profile = get_object_or_404(Users, id=user_id)

    # Only allow self-edit
    if 'user_id' not in request.session or request.session['user_id'] != user_profile.id:
        messages.error(request, "You are not authorized to edit this profile.")
        return redirect('profile_page', user_id=user_id)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile_page', user_id=user_profile.id)
    else:
        form = ProfileUpdateForm(instance=user_profile)

    return render(request, 'edit_profile.html', {
        'form': form,
        'user_profile': user_profile  # <-- add this
    })



def upload_profile_picture(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to upload a profile picture.")
        return redirect('login')

    user = get_object_or_404(Users, id=request.session['user_id'])

    if request.method == 'POST':
        old_picture_path = user.profile_picture.path if user.profile_picture else None

        form = ProfilePictureForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            # If the clear checkbox is checked
            if 'profile_picture-clear' in request.POST:
                if old_picture_path and os.path.isfile(old_picture_path):
                    os.remove(old_picture_path)  # Delete file from storage
                user.profile_picture = None
                user.save()
                request.session['prof_pic'] = None
                messages.success(request, "Profile picture removed successfully!")
                return redirect('details', id=user.id)

            # If new file uploaded, delete old one
            if 'profile_picture' in request.FILES and old_picture_path:
                if os.path.isfile(old_picture_path):
                    os.remove(old_picture_path)

            form.save()

            # Update session with new picture
            if user.profile_picture:
                request.session['prof_pic'] = user.profile_picture.url
            else:
                request.session['prof_pic'] = None

            messages.success(request, "Profile picture updated successfully!")
            return redirect('details', id=user.id)
    else:
        form = ProfilePictureForm(instance=user)

    return render(request, 'upload_profile_picture.html', {'form': form})



def members(request):
    template = loader.get_template('myfirst.html')
    return HttpResponse(template.render())


def users(request):
    mymembers = Users.objects.all()
    template = loader.get_template('all_users.html')

    current_user_id = request.session.get('user_id')
    if not current_user_id:
        return redirect('login')  # Redirect to login if not logged in
    current_user = get_object_or_404(Users, id=current_user_id)

    context = {
        'mymembers': mymembers,
        'following': current_user.following.all(),
        'logged_in_user': current_user,

    }
    return HttpResponse(template.render(context, request))


def details(request, id):
    mymember = Users.objects.get(id=id)
    images = mymember.images.all().order_by('-id')
    template = loader.get_template('details.html')
    context = {
        'mymember': mymember,
        'images': images,
    }
    return HttpResponse(template.render(context, request))


def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())


def testing(request):
    object = Users.objects.all()
    template = loader.get_template('template.html')
    context = {
        'object': object,
        'hardcode': 'hast'
    }
    return HttpResponse(template.render(context, request))


def upload_product_images(request, product_id):
    user = get_object_or_404(Users, id=product_id)
    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            Images.objects.create(user=user, image=form.cleaned_data['image'])

            # Notify followers
            followers = user.followers.all()  # Assuming Users model has related_name='followers'
            if followers:
                subject = f"{user.firstname} {user.lastname} posted a new image!"
                message = (
                    f"Hi,\n\n"
                    f"{user.firstname} {user.lastname} has uploaded a new image.\n"
                    f"View it here: https://sirus.pythonanywhere.com/"
                )
                from_email = "bsse23027@itu.edu.pk"
                recipient_list = [f.email for f in followers if f.email]

                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return redirect('details', id=user.id)
    else:
        form = ProductImageForm()

    return render(request, 'upload_images.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])  # Hash password
            user.save()
            messages.success(request, "Your account has been created successfully! You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect('login')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = Users.objects.get(email=email)
                if check_password(password, user.password):
                    messages.success(request, f"Welcome back, {user.firstname}!")
                    # Store user ID in session
                    request.session['user_id'] = user.id
                    request.session['user_fname'] = user.firstname
                    request.session['user_lname'] = user.lastname
                    if user.profile_picture:
                        request.session['prof_pic'] = user.profile_picture.url

                    return redirect('details', id=user.id)
                else:
                    messages.error(request, "Incorrect password.")
            except Users.DoesNotExist:
                messages.error(request, "No account found with that email.")
                return redirect('signup')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm()
    return render(request, 'main.html', {'form': form})


def toggle_follow(request, user_id):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to follow someone.")
        return redirect('login')

    current_user = get_object_or_404(Users, id=request.session['user_id'])
    user_to_follow = get_object_or_404(Users, id=user_id)

    if current_user == user_to_follow:
        messages.error(request, "You can't follow yourself!")
        return redirect('showUsers')

    if user_to_follow in current_user.following.all():
        # Already following → unfollow
        current_user.following.remove(user_to_follow)
        messages.success(request, f"You have unfollowed {user_to_follow.firstname}.")
    else:
        # Not following → follow
        current_user.following.add(user_to_follow)
        messages.success(request, f"You are now following {user_to_follow.firstname}.")

    return redirect('showUsers')

def following_gallery(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to view your gallery.")
        return redirect('login')

    current_user = get_object_or_404(Users, id=request.session['user_id'])

    images = Images.objects.filter(
        user__in=current_user.following.all()
    ).order_by('-created_at')[:20]  # Newest first, limit to 20

    return render(request, 'following_gallery.html', {'images': images})



def chat_view(request):
    # Require login
    if 'user_id' not in request.session:
        messages.error(request, "Please log in to use the chat.")
        return redirect('login')

    user = get_object_or_404(Users, id=request.session['user_id'])

    # Initialize chat history in session
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []

    response_text = ""

    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()

        # Rate-limit check: prevent spamming the API
        last_time = request.session.get('last_chat_time', 0)
        now = time.time()
        if now - last_time < 5:  # 5-second delay between messages
            request.session['chat_history'].append({
                "role": "bot",
                "parts": ["Please wait a few seconds before sending another message."]
            })
            request.session.modified = True
            return redirect('chat')

        request.session['last_chat_time'] = now

        if len(user_message) > 500:
            response_text = "Message too long."
        else:
            try:
                chat = model.start_chat(history=request.session['chat_history'])
                response = chat.send_message(user_message)
                response_text = response.text

                # Save user & bot messages to session
                request.session['chat_history'].append({
                    "role": "user",
                    "parts": [user_message]
                })
                request.session['chat_history'].append({
                    "role": "bot",
                    "parts": [response_text]
                })

                request.session.modified = True

            except Exception as e:
                # Friendly quota/error message
                msg = str(e)
                if "429" in msg:
                    bot_msg = "AI quota exceeded. Please try again later."
                else:
                    bot_msg = "Something went wrong. Please try again."

                request.session['chat_history'].append({
                    "role": "bot",
                    "parts": [bot_msg]
                })
                request.session.modified = True

    return render(request, "chat.html", {
        "history": request.session['chat_history'],
        "user": user
    })
