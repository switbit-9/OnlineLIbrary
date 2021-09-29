from datetime import timedelta
from decimal import Context
from django.core.files.base import ContentFile
from django.http import request
from App.forms import *
from django.db.models import fields, F
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render, resolve_url
from .models import *
from django.views import View
from django.contrib import messages

messagess = []

class Home(View):
    
    def get(self, request):
        books = Books.objects.all()
        user= User.objects.filter(id = request.session.get('user_id'))
        username = request.session.get('username')
        #----------------------------------------HTML {% if books.availability==0%}

        if username == None:
            return redirect('login')

        else:
            context = {
                'books' : books,
                'username' : username,
                'user' : user
            }
            return render(request, 'home.html', context)




class LoginView(View):

    def get(self, request):
        if request.session.get('is_logged_in'):
            return redirect('home')

        form = LoginForm
        return render(request, 'login.html', context= {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = User.objects.filter(username= username)
            admin = User.objects.filter(username= 'admin', password=password)
            if admin:
                return redirect('admin')

            if user:
                if user[0].password == password:
                    request.session['is_logged_in'] = True
                    request.session['username'] = username
                    request.session['user_id'] = user[0].id
                    return redirect('home')
                else: 
                    messages.add_message(request, messages.ERROR, "Password doesn't exist")
            
            else:
                   messages.add_message(request, messages.ERROR, "Username doesn't exist") 
                

        return render(request, 'login.html', context={'form': form })

class RegisterView(View):
    
    def get(self, request):
        if request.session.get('is_logged_in'):
            return redirect('home')        
        form = RegisterForm
        context = {
            'form' : form
        }
        return render(request, 'registration.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        username =request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        users = User.objects.all()
        for user in users: 
            if user.username == username:
                messages.add_message(request, messages.ERROR, "This username is taken")
                return render(request, 'register.html', context={'form': form})
            if user.email == email:
                messages.add_message(request, messages.ERROR, "You already have an account")
        if password == request.POST['password'] :
            form.save()
            return redirect('login')
        else: 
            messages.add_message(request, messages.ERROR, "Password doesn't match")
        
        return redirect('register')


def profile(request):
    result = Borrow.objects.filter(user_id = request.session.get('user_id'))
    allbooks= Books.objects.all()
    book = []
    messages = []
    for r in result:
        books = Books.objects.filter(id = r.book_id).first()
        book.append(books)
        return_date = r.date - timedelta(days=20)
        dif = return_date.day - datetime.now().day
        if dif >= 0:
            message = {
                'message' : 'You have ' + str(dif) + ' days to return ' + books.title
            }
            messages.append(message)
        else: 
            message = {
                'message' : 'You have successfully read' 
            }
            messages.append(message)

    context = {
        'messages' : messages,
        'username' : request.session.get('username'),
        'books' : allbooks,
        'book' : book
    }
   
    return render(request, 'profile.html', context)


def logout(request):
    del(request.session['is_logged_in'])
    del(request.session['username'])
        
    return redirect('login')



def save(request, id):
    test = Save.objects.filter(user_id = request.session['user_id'], book_id=id)
    if test:
        messages.add_message(request, messages.INFO, "This book is already saved")

        return redirect('home')

    else:
        Save.objects.filter(user_id = request.session['user_id']).create(book_id=id, user_id = request.session['user_id'])
        books = Books.objects.all()


        messages.add_message(request, messages.INFO, "Book was saved successfully")

        context= {
            'books' : books,
            'username' : request.session.get('username')     
        }
    
        return render(request, 'home.html', context)
        

def unsave(request, id):
    Save.objects.filter(user_id=request.session['user_id'], book_id=id).delete()
    user = Save.objects.filter(user_id = request.session.get('user_id'))
    books = []
    for r in user:
        book = Books.objects.filter(id = r.book_id).first()
        books.append(book)
    context= {
      'books' : books,
      'username' : request.session.get('username'),
    }


    return render(request, 'favorites.html', context)


def saved(request):
    result = Save.objects.filter(user_id = request.session.get('user_id'))
    books = []
    for r in result:
        book = Books.objects.filter(id = r.book_id).first()
        books.append(book)
    context= {
      'books' : books,
      'username' : request.session.get('username'),
      'result' : result,
    }

    return render(request, 'favorites.html', context)

def borrow(request, id):
    test = Borrow.objects.filter(user_id = request.session['user_id'], book_id=id)
    book = Books.objects.filter(id=id).first()

    if test:
        messages.add_message(request, messages.ERROR, "You already borrowed this book")
        return redirect('home')
    
    else:  
        if book.availability == 0:
            messages.add_message(request, messages.ERROR, "This book is out of stock")
            return redirect('home')
        
        else:
            user = Borrow.objects.filter(user_id = request.session['user_id']).create(book_id=id, user_id = request.session['user_id'])
            book = Books.objects.update(quantity = F('quantity') - 1) 
            return redirect('home')

def unborrow(request, id):
    Borrow.objects.filter(user_id=request.session['user_id'], book_id=id).delete()
    book = Books.objects.filter(id=id).update(quantity = F('quantity') + 1) 


    return redirect('profile')


def books(request):
    books = Books.objects.all()
    context = {
        'books' : books
    }
    return render(request, 'books.html', context)

def authors(request):
    authors = Publisher.objects.all()

    context = {
        'authors' : authors,
        'username' : request.session.get('username')
    }
    return render(request, 'authors.html', context)

def author(request, id):
    author = Publisher.objects.filter(id=id).first()
    books = Books.objects.filter(publisher = author.id)

    context = {
        'author': author,
        'books': books,
        'username' : request.session.get('username')
    }
    return render(request, 'author.html', context)

def search(request):
    q = request.GET.get('q')
    if q:
        books = Books.objects.filter(title__icontains = q)
        context = {
            'books' : books,
            'username' : request.session.get('username'),
        }
        return render(request, 'search.html', context)
    else:
        books = Books.objects.all()
        context = {
            'books' : books
        }
        return render(request, 'search.html', context)


def book(request, id):
    book = Books.objects.filter(id=id).first()
    books = Books.objects.all()
    context = {
        'book' : book,
        'books' : books,
        'username' : request.session.get('username')
    }
    return render(request, 'book.html', context)

def calendar(request) :
        user= User.objects.filter(id = request.session.get('user_id'))
      
        context = {           
            'user' : user
        }

        return render(request, 'calendar.html', context)

def settings(request):
    user = User.objects.filter(id = request.session.get('user_id'))
    context = {
            'user' : user,
            'username' : request.session.get('username'),
        }
    return render(request, 'settings.html', context)

class EditView(View):

    def get(self, request):
        user = User.objects.filter(id = request.session.get('user_id'))
        form = RegisterForm
        context = {
            'user' : user,
            'form' : form,
            'username' : request.session.get('username')
        }
        return render(request, 'edit.html', context)

    def post(self, request):
        form = RegisterForm(request.POST)
        email = User.objects.filter(id=request.session.get('user_id')).update(email=request.POST['email'])   
        password = User.objects.filter(id=request.session.get('user_id')).update(password=request.POST['password'])

        return redirect('edit')

def delete(request):
    del(request.session['is_logged_in'])
    del(request.session['username'])
    User.objects.filter(id=request.session.get('user_id')).delete()

    return redirect('login')


def prove(request):
    user = User.objects.filter(username='seharborici')
    book = Books.objects.filter(id=2)
    context = {
        'user' : user,
        'book' : book
    }
    return render(request, 'prove.html', context)


def admin(request):
    book = Books.objects.all()
    context = {
        'book' : book
    }
    return render(request, 'admin.html', context)

 

def manage_books(request):
    book = Books.objects.all()
    form = BooksForm
    context = {
        'book' : book,
        'form' : form
    }
    return render(request, 'manageb.html', context)

class Addbook(View): #addbook by user
    
    def get(self, request):
        addbooks = BooksForm
        context = {
            'form' : addbooks
        }
        return render(request, 'addnewbook.html', context)
    
    def post(self, request):
        addbook = BooksForm(request.POST)
        addbook.save()
        #return redirect('addbook')

#    def get(self, request):
#        form = BooksForm
#        context = {
#           'form' : form
#        }
#        return render(request, 'prove.html', context)
#
#    def post(self,request):
#        form = BooksForm(request.POST)
#        if form.is_valid():
#            form.save()
#        context = {
#            'form' : form
#        }
#        return render(request, 'prove.html', context)

def delete_book(request, id):
    book = Books.objects.filter(id=id)
    if book:
        book.delete()
        return redirect('manageu')

class AddNew(View):

    def get(self, request):
        form = BooksForm
        context = {
            'form' : form
        }
        return render(request, 'addnewbook.html', context)

    def post(self, request):
        form = BooksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manageb')
        else:
            messages.add_message(request, messages.ERROR, 'Error while adding book' )
            return redirect('manageu')





def update_books(request, id):
    pass


def manage_user(request):
    users = User.objects.all()
    context = {
        'users' : users
    }
    return render(request, 'manageu.html', context)

def delete_user(request, id):
    user = User.objects.get(id=id)
    print(type(user))
    if user:
        user.delete()
        return redirect('manageu')
    return redirect('manageu')

def block_user(request, id):
    user = User.objects.filter(id=id)
    if user:
        user.update(password = '4321')
        return redirect('manageu')
    return redirect('manageu')

def archive(request, id):
    book = Archive.objects.create(book_id=id)
    if book:
        books= Books.objects.filter(id=id).delete()

        return redirect('manageb')
    return redirect('manageb')


def archived_books(request):
    result = Archive.objects.all()
    book = []
    for r in result:
        books = Books.objects.filter(id = r.book_id).first()
        book.append(books)

    return render(request, 'archive.html', context={'book': book})

def unarchive(request, id):
    book = Archive.objects.filter(book_id=id)
    Books.objects.create(id = id)
    book.delete()
    
    return redirect('archived')

def allactivity(request):
    message = messagess
    return render(request,'allactivity.html', context={ 'message': message})


def issued(request):
    pass




    # Create your views here.