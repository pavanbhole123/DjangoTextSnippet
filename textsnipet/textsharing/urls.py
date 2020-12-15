from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('create_sharable_text/',views.create_sharable_url,name="create_sharabe_text"),
    path('view/<str:hash>',views.view_shared_text,name="view_shared_text"),
    path('thanks/<str:hash>',views.thanks,name="thanks"),
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout")
]