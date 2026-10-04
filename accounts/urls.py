from django.contrib.auth.views import LoginView, LogoutView, \
   PasswordChangeView, PasswordChangeDoneView, PasswordResetView,PasswordResetDoneView,PasswordResetCompleteView,PasswordResetConfirmView
from django.urls import path
from .views import dashboard_view, user_register, UserSignupView, edit_profile, EditProfileView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_page_view'),
    path('logout/', LogoutView.as_view(), name='logout_page_view'),
    path('profile/', dashboard_view, name='user_profile'),
    #path('profile/edit', edit_profile, name='user_profile_edit'),
    path('profile/edit', EditProfileView.as_view(), name='user_profile_edit'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('signup/', user_register, name='user_register'),
    #path('signup/', UserSignupView.as_view(), name='user_register'),

]


