from django.urls import path


from . import views


app_name = 'offers'

urlpatterns = [
#path('', views.offers_view_list, name='offers_list'),
path('create/', views.offers_create, name='offers_create' ),
path('<int:offer_id>/', views.offers_detail, name = 'offers_detail'),
path('<str:source>/', views.offers_view_list, name='offers_list'),
path('update/<int:offer_id>/', views.offers_update, name='offers_update'),
path('delete/<int:offer_id>/', views.offers_delete, name='offers_delete'),
path('feedback/', views.contact, name='offers_feedback'),
path('request/send/<int:offer_id>/', views.send_swap_request, name='send_swap_request'),
path('request/<int:request_id>/<str:action>/', views.manage_request, name='manage_request'),


]



# app_name = 'accounts'
# urlpatterns = [

# path('login/', login_view, name = 'login'),

# path('logout/', logout_view, name = 'logout'),

# path('login/', login_view, name = 'register'),

# path('login/', login_view, name = 'login'),

# path('login/', login_view, name = 'login'),


# ]