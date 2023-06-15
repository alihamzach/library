from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),

    path('user_login/', user_login, name='user_login'),
    path('user_logout/', user_logout, name='user_logout'),
    path('user_signup/', user_signup, name='user_signup'),

    path('student_list/', student_list, name='student_list'),
    path('add_student/', add_student, name='add_student'),
    path('delete_student/<int:pk>/', delete_student, name='delete_student'),
    path('edit_student/<int:pk>/', edit_student, name='edit_student'),

    path('book_list/', book_list, name='book_list'),
    path('add_book/', add_book, name='add_book'),
    path('delete_book/<int:pk>/', delete_book, name='delete_book'),
    path('edit_book/<int:pk>/', edit_book, name='edit_book'),

    path('order_list/', order_list, name='order_list'),
    path('add_order/', add_order, name='add_order'),
    path('delete_order/<int:pk>/', delete_order, name='delete_order'),
    path('edit_order/<int:pk>/', edit_order, name='edit_order'),

    path('issue_book_submission/', issue_book_submission, name='issue_book_submission'),

    # path('borrow/book/', borrow_book, name='borrow_book'),
    # path('borrow/book/list/', borrow_book_list, name='borrow_book_list'),
    # path('collect/fine/', collect_fine, name='collect_fine'),
    # path('collect/fine/list/', fine_collect_list, name='fine_collect_list'),

    # path("profile/", profile, name="profile"),
    # path("edit_profile/", edit_profile, name="edit_profile"),

]

