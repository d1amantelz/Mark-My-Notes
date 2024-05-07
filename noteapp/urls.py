from django.urls import path
from .views import *

urlpatterns = [

    # NOTE VIEWS
    path('notes/', NoteListView.as_view(), name='notes'),
    path('notes/create/', NoteCreateView.as_view(), name='create_note'),
    path('notes/<int:note_id>/edit_mode/', NoteUpdateView.as_view(), name='note_edit_mode'),
    path('notes/<int:note_id>/view_mode/', NoteViewMode.as_view(), name='note_view_mode'),
    path('notes/<int:note_id>/update_note/', NoteInfoUpdateView.as_view(), name='update_note'),
    path('notes/by_category/<int:category_id>', NotesByCategoryView.as_view(), name='notes_by_category'),
    path('notes/delete/<int:note_id>/', delete_note, name='delete_note'),
    path('notes/export/<int:note_id>/', export_note, name='export_note'),
    path('notes/search/', note_search, name='note_search'),

    # CATEGORY VIEWS
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/create/', CategoryCreateView.as_view(), name='create_category'),
    path('categories/<int:category_id>/update_category/', CategoryUpdateView.as_view(), name='update_category'),
    path('categories/delete/<int:category_id>/', delete_category, name='delete_category'),

    # PROFILE VIEWS
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('profile/update/username/', UsernameUpdateView.as_view(), name='update_username'),
    path('profile/update/avatar/', AvatarUpdateView.as_view(), name='update_avatar'),

    # AUTH VIEWS
    path('sign_up/', SignUpPageView.as_view(), name='sign_up'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),

    # OTHER VIEWS
    path('create/', create_screen, name='create_screen'),
]
