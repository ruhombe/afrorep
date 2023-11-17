from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    ############START ACCOUNTS URLS
    path('register/', views.register, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/<int:id>',views.user_profile, name='profile'),
    path('update_user_profile/<int:id>',views.update_user_profile, name='update_user_profile'),
    path('handle_skill_slection/',views.handle_skill_selection, name='handle_skill_selection'),
    path('delete_user_skill/<int:skill_id>', views.delete_user_skill, name='delete_user_skill'),
    path('delete_user_experience/<int:experience_id>', views.delete_user_experience, name='delete_user_experience'),
    path('delete_user_portfolio/<int:portfolio_id>', views.delete_user_portfolio, name='delete_user_portfolio'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name= "password_reset.html"),  name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name= 'password_reset_sent.html'),  name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name= 'password_reset_form.html'),  name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name= 'password_reset_done.html'),  name="password_reset_complete")
    ################END ACCOUNTS URLS


]