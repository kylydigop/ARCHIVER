from django.urls import path, re_path


from . import views

urlpatterns = [
    path('home/', views.homePage.as_view(), name='search'),
    path('upload/', views.uploadPage.as_view(), name='upload'),
    path('abstract/<str:slug>', views.abstractPage.as_view(), name='abstract'),
    path('abstract/<str:slug>/', views.DownloadFile.as_view(), name='downloadFile'),
    path('abstract/', views.abstractPage.as_view(), name='abstract'),
    path('remove_thesis/<int:id>/', views.removeThesis.as_view(), name='remove'),
    path('about/', views.aboutPage.as_view(), name='about'),
]


