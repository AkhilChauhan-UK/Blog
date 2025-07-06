from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import BlogPost, Comment, ContactMessage

def category_posts(request, category):
    posts = BlogPost.objects.filter(category=category)
    return render(request, 'category_posts.html', {'posts': posts, 'category': category})

def home(request):
    latest_posts = BlogPost.objects.all().order_by('-created_at')[:5]  # Get latest 5 posts
    featured_post = BlogPost.objects.order_by('-created_at').first()  # Get most recent post as featured
    categories = BlogPost.objects.values_list('category', flat=True).distinct()  # Get unique categories
    
    return render(request, 'home.html', {
        'featured_post': featured_post,
        'latest_posts': latest_posts,
        'categories': categories,
    })

def contact(request):
    if request.method == "POST":
        email = request.POST.get("email")
        message = request.POST.get("message")
        ContactMessage.objects.create(email=email, message=message)
        messages.success(request, "Your message has been sent successfully")
        return redirect('contact')
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def blog(request):
    posts = BlogPost.objects.all()
    return render(request, 'list.html', {'posts': posts})

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.all()
    
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
            return redirect('blog_detail', pk=pk)  # ✅ Fixed
    
    return render(request, 'detail.html', {'post': post, 'comments': comments})

def blog_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category = request.POST.get("category", "General")
        image = request.FILES.get("image")  # ✅ Get uploaded image
        
        if title and content:
            BlogPost.objects.create(
                title=title, 
                content=content, 
                author=request.user, 
                category=category,
                image=image  # ✅ Save image
            )
            messages.success(request, "Blog post created successfully!")
            return redirect('blog')
    
    return render(request, 'form.html')

def blog_update(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category = request.POST.get("category", post.category)
        image = request.FILES.get("image")  # ✅ Get new image if uploaded
        
        if title and content:
            post.title = title
            post.content = content
            post.category = category
            if image:
                post.image = image  # ✅ Update image if provided
            post.save()
            messages.success(request, "Blog post updated successfully!")
            return redirect('blog')
    
    return render(request, 'form.html', {'post': post})

def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    
    if request.method == "POST":
        post.delete()
        messages.success(request, "Blog post deleted successfully!")
        return redirect('blog')  # ✅ Redirect to blog page after deletion
    
    return render(request, 'confirm_delete.html', {'post': post})

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('home')
            else:
                messages.error(request, "Incorrect password. Please try again.")
        except User.DoesNotExist:
            messages.error(request, "User doesn't exist. Please create an account.")
            return redirect('register')
    
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'signup.html')