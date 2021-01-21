from django.urls import path,include
from .views import (
						register  ,dashboard  ,intropage  ,
						profile_page  ,NoteCreateView  ,
						notes_by_user  ,NoteDetailView  ,
						NoteUpdateView  ,set_note_password  ,
						set_note_password_change  ,
						confirm_password_view  , SearchResultsListView  ,
						move_to_trash  , move_to_archive,
						show_objects_category,show_favorites_notes,
						show_lock_notes,move_to_untagged,remove_all_notes_trash_to_untagged,
						delete_notes_from_trash,share_note_by_email,
						sort_by_color,demo_user_login

					)

urlpatterns = [
	path('note/demo_user_login/',demo_user_login,name='demo_user_login'),
	path('note/share/<uuid:pk>/',share_note_by_email,name='share_note_by_email'),
	
	path('note/delete_notes_from_trash/<uuid:pk>/',delete_notes_from_trash,name='delete_notes_from_trash'),
	path('note/delete_notes_from_trash/',delete_notes_from_trash,name='delete_notes_from_trash'),
	path('note/remove_all_notes_trash_to_untagged/',remove_all_notes_trash_to_untagged,name='remove_all_notes_trash_to_untagged'),

	path('note/move_to_untagged/<uuid:pk>/',move_to_untagged,name='move_to_untagged'),

	path('note/sort_by/sort_by_color/<str:color>/',sort_by_color,name='sort_by_color'),
	path('note/sort_by/lock_note/',show_lock_notes,name='show_lock_notes'),
	path('note/sort_by/favorites/',show_favorites_notes,name='show_favorites_notes'),

	path('note/sort_by/category/<str:category>/',show_objects_category,name='show_objects_category'),
	path('note/move_to_archive/<uuid:pk>/',move_to_archive,name='move_to_archive'),
	path('note/move_to_trash/<uuid:pk>/',move_to_trash,name='move_to_trash'),
	path('note/search/',SearchResultsListView,name='search_results'),
	path('note/check_password/',confirm_password_view,name='check_password'),
	path('note/change_password/',set_note_password_change,name='set_change_password'),
	path('note/set_password/',set_note_password,name='set_password'),

	path('note/update/<uuid:pk>/',NoteUpdateView,name='note_update'),

	path('note/detail/<uuid:pk>/',NoteDetailView,name='note_detail'),

	path('note/add',NoteCreateView,name='add_note'),

	path('dashboard',notes_by_user,name='dashboard'),
	path('register/',register,name='register'),
	path('profile_page/',profile_page,name='profile_page'),
	# path('dashboard/',dashboard,name='dashboard'),
	path('',intropage,name='intropage'),
	
]