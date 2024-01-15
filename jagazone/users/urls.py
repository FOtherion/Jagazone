from django.urls import path
from jagazone.users import views


app_name = "users"
urlpatterns = [
    # path("~redirect/", view=views.user_redirect_view, name="redirect"),
    path("register/", view=views.user_register_view, name='register'),
    path("create/", view=views.user_create_view, name="create"),
    path("<uuid:pk>/", view=views.user_detail_view, name="detail"),
    path("update/<uuid:pk>/", view=views.user_update_view, name="update"),
    path("delete/<uuid:pk>/", view=views.user_delete_view, name="delete"),
    path("", view=views.user_list_view, name="user-list")

]
