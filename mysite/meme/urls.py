from django.urls import path

from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('acceptCookies/',views.acceptCookies,name="accCook"),
    path('cookieReject/',views.rejectCookies,name="rejCook"),
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout")
]