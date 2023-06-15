from django.shortcuts import render, redirect
from django.contrib.auth.forms import authenticate
from django.contrib.auth import login, logout
# from django.contrib.auth.forms import AuthenticationForm
from .models import Student, BookDetail, BookingOrder
from .forms import StudentCreate, BookCreate, UserLoginForms, UserSignupForm, OrderCreate
from django.contrib.auth.decorators import login_required


@login_required(login_url='user_login')
def home(request):
    user = request.user
    return render(request, 'base.html', {'user': user})


@login_required(login_url='user_login')
def student_list(request):
    if request.user.is_staff and request.user.is_superuser:
        student = Student.objects.all()
        if request.method == "POST":
            searched = request.POST['searched']
            if searched:
                student = Student.objects.filter(name__iexact=searched)
        return render(request, 'student_list.html', {'student': student, 'request': request})
    else:
        student = Student.objects.filter(name=request.user.username)
        return render(request, 'student_list.html', {'student': student, 'request': request})


@login_required(login_url='user_login')
def add_student(request):
    if request.method == 'POST':
        form = StudentCreate(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentCreate()
    return render(request, 'add_student.html', {'form': form})


@login_required(login_url='user_login')
def delete_student(request, pk):
    if request.method == 'POST':
        obj = Student.objects.get(pk=pk)
        obj.delete()
    return redirect('student_list')


@login_required(login_url='user_login')
def edit_student(request, pk):
    if request.method == 'POST':
        obj = Student.objects.get(pk=pk)
        form = StudentCreate(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        obj = Student.objects.get(pk=pk)
        form = StudentCreate(instance=obj)
    return render(request, 'edit_student.html', {'form': form, 'id': pk})


@login_required(login_url='user_login')
def book_list(request):
    book = BookDetail.objects.all()
    if request.method == "POST":
        searched = request.POST['searched']
        if searched:
            book = BookDetail.objects.filter(title__iexact=searched)
    return render(request, 'book_list.html', {'book': book, 'request': request})


@login_required(login_url='user_login')
def add_book(request):
    if request.method == 'POST':
        form = BookCreate(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookCreate()
    return render(request, 'add_book.html', {'form': form})


@login_required(login_url='user_login')
def delete_book(request, pk):
    if request.user.is_staff and request.user.is_superuser:
        if request.method == 'POST':
            obj = BookDetail.objects.get(pk=pk)
            obj.delete()
        return redirect('book_list')
    else:
        pass


@login_required(login_url='user_login')
def edit_book(request, pk):
    if request.user.is_staff and request.user.is_superuser:
        if request.method == 'POST':
            obj = BookDetail.objects.get(pk=pk)
            form = BookCreate(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                return redirect('book_list')
        else:
            obj = BookDetail.objects.get(pk=pk)
            form = BookCreate(instance=obj)
        return render(request, 'edit_book.html', {'form': form, 'id': pk})
    else:
        None


@login_required(login_url='user_login')
def order_list(request):
    if request.user.is_staff and request.user.is_superuser:
        order = BookingOrder.objects.all()
        if request.method == "POST":
            searched = request.POST['searched']
            if searched:
                order = BookingOrder.objects.filter(student__name__iexact=searched)
        return render(request, 'order_list.html', {'order': order, 'request': request})
    else:
        order = BookingOrder.objects.filter(student__name=request.user.username)
        return render(request, 'order_list.html', {'order': order, 'request': request})


@login_required(login_url='user_login')
def add_order(request):
    students = Student.objects.all()
    books = BookDetail.objects.all()
    if request.method == 'POST':
        form = OrderCreate(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderCreate()
    return render(request, 'add_order.html', {'form': form, 'students': students, 'books': books})


@login_required(login_url='user_login')
def delete_order(request, pk):
    if request.method == 'POST':
        obj = BookingOrder.objects.get(pk=pk)
        obj.delete()
    return redirect('order_list')


@login_required(login_url='user_login')
def edit_order(request, pk):
    if request.method == 'POST':
        obj = BookingOrder.objects.get(pk=pk)
        form = OrderCreate(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        obj = BookingOrder.objects.get(pk=pk)
        form = OrderCreate(instance=obj)
    return render(request, 'edit_order.html', {'form': form, 'id': pk})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForms(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(email=uname, password=upass)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = UserLoginForms()
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('user_login')


def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            Student.objects.create(name=request.POST.get('username'))
            return redirect('user_login')
    else:
        form = UserSignupForm()
    return render(request, 'registration/signup.html', {'form': form})


# def borrow_book(request):
#     if request.method == 'POST':
#         form = BorrowBookForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('borrow_book_list')
#     else:
#         form = BorrowBookForm()
#     return render(request, 'borrow_book.html', {'form': form})
#
# def borrow_book_list(request):
#     books = BorrowBook.objects.all()
#     return render(request, 'borrow_book_list.html', {'books': books})
#
# def collect_fine(request):
#     if request.method == 'POST':
#         form = FineCollectForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('fine_collect_list')
#     else:
#         form = FineCollectForm()
#     return render(request, 'collect_fine.html', {'form': form})
#
# def fine_collect_list(request):
#     fines = FineCollect.objects.all()
#     return render(request, 'fine_collect_list.html', {'fines': fines})


# def profile(request):
#     return render(request, "profile.html")
#
#
# def edit_profile(request):
#     student = Student.objects.get(user=request.user)
#     if request.method == "POST":
#         email = request.POST['email']
#         phone = request.POST['phone']
#         branch = request.POST['branch']
#         classroom = request.POST['classroom']
#         roll_no = request.POST['roll_no']
#
#         student.user.email = email
#         student.phone = phone
#         student.branch = branch
#         student.classroom = classroom
#         student.roll_no = roll_no
#         student.user.save()
#         student.save()
#         alert = True
#         return render(request, "edit_profile.html", {'alert': alert})
#     return render(request, "edit_profile.html")


def issue_book_submission(request):
    if request.method == 'POST':
        store = BookingOrder.objects.filter(student=request.user)

        def get_category(addbook):
            if addbook.category == "Not-Issued":
                addbook.category = "Issued"
                obj = IssueBook(user=user1, studentid=studentid, book1=book1)
                obj.save()
                addbook.save()
            else:
                messages.error(request, " Book already issued !!!")

        category_list = list(set(map(get_category, store)))
        Issue = IssueBook.objects.all()
        return render(request, 'bookissue.html', {'Issue': Issue})
    return redirect('/')
