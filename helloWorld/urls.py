from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('helloWorld/', views.members, name='helloWorld'),
    path('showUsers/', views.users, name='showUsers'),
    path('details/<int:id>', views.details, name='details'),
    path('product/<int:product_id>/upload-images/', views.upload_product_images, name='upload_product_images'),
    path('test/', views.testing, name='testing'),
    path('details/logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('follow/<int:user_id>/', views.toggle_follow, name='toggle_follow'),
    path('following-gallery/', views.following_gallery, name='following_gallery'),
    path('upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path('profile/<int:user_id>/', views.profile_page, name='profile_page'),
    path('profile/<int:user_id>/edit/', views.edit_profile, name='edit_profile'),
    path('chat/', views.chat_view, name='chat'),

]
