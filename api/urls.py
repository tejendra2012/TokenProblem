from django.contrib import admin
from django.urls import path
from . import views as api_views

urlpatterns = [
    path('create-token', api_views.CreateTokenView.as_view(),name='create-token'),
    path('assign-token', api_views.AssignTokenView.as_view(),name='assign-token'),
    path('unblock-token', api_views.UnblockTokenView.as_view(),name='unblock-token'),
    path('remove-token', api_views.RemoveTokenView.as_view(),name='remove-token'),
    path('keep-alive-token', api_views.KeepaliveTokenView.as_view(),name='keep-alive-token'),
]