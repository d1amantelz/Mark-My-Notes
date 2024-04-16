from django.urls import path
from .views import *

urlpatterns = [
    # notes views
    path('', notes, name='notes'),
    path('create/', create_note, name='create_note'),
    path('note_detail/<int:note_id>', note_detail, name='note_detail'),
    path('note/<int:note_id>/view_mode/', note_view_mode, name='note_view_mode'),
    path('note/<int:note_id>/delete/', delete_note, name='delete_note'),
    path('note/<int:note_id>/note_info/', change_note_info, name='change_note_info'),

    # category views
    path('categories/', categories, name='categories'),
    path('category_detail/<int:category_id>', category_detail, name='category_detail'),
    path('create_category/', create_category, name='create_category'),
    path('change_category_info/<int:category_id>', change_category_info, name='change_category_info'),
    path('category/<int:category_id>/delete/', delete_category, name='delete_category'),
    path('notes_by_category/<int:category_id>', notes_by_category, name='notes_by_category'),

    path('create_screen/', create_screen, name='create_screen'),

    # note views
    path('profile/', profile_view, name='profile'),
    path('profile/change_username/', change_username, name='change_username'),
    path('profile/change_avatar/', change_avatar, name='change_avatar'),

    # login and signup views
    path('login/', LoginPageView.as_view(), name='login'),
    path('sign_up/', SignUpPageView.as_view(), name='sign_up'),
    path('logout/', logout_view, name='logout'),
]
