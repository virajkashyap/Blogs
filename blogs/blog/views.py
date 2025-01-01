from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from  django.contrib.auth import authenticate,login,logout 
from django.contrib import messages
from blog.models import Blog,Tag,blog_user,Comment
from  django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request,"index.html")


def signup(request):
    return render(request,"signup.html")

    
def save_user(request):
    users=blog_user.objects.all()
    if request.method=="POST":
        name=request.POST['user_name']
        password=request.POST['password']
        email=request.POST['email']
        user_save=blog_user(username = name,password = password, email = email).save()
        myuser=User.objects.create_user(name,email,password).save()
        msg="user created successfully" 
        return render(request,'index.html',{"msg":msg})
    else:
        return HttpResponse("<h1>error 404 not found</h1>")
    


# login page
def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        blog_user = authenticate(username=username, password=password)
        if blog_user is not None:
            login(request, blog_user)
            return redirect('blog_list')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'index.html')
    return render(request, 'index.html')

# blog list all
@login_required(login_url='/')
def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    
    paginator = Paginator(blogs, 5)  # 5 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blogs.html', {'page_obj': page_obj})


@login_required(login_url='/')
@login_required
def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    comments = Comment.objects.filter(blog=blog)  # Filter comments related to the blog
    return render(request, 'blog_detail.html', {'blog': blog, 'comments': comments})


@login_required(login_url='/')
def combined_blog_search(request):
    query = request.GET.get('q')
    search_type = request.GET.get('type')

    if query:
        if search_type == 'tag':
            try:
                tag = Tag.objects.get(name__iexact=query)  # Case-insensitive search for tag
                blogs = tag.blogs.all()  # Use the related_name defined in the Blog model
            except Tag.DoesNotExist:
                blogs = []
        elif search_type == 'rank':
            # Full-text search simulation with `icontains`
            blogs = Blog.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        # elif search_type == 'similar':
        #     # Basic similarity search with `icontains`
        #     blogs = Blog.objects.filter(title__icontains=query)
        else:
            blogs = Blog.objects.all()
    else:
        blogs = Blog.objects.all()

    # Pagination for all search results
    paginator = Paginator(blogs, 5)  # 5 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blogs.html', {'page_obj': page_obj})

@login_required(login_url='/')
def add_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        user=request.user
        if content:
            commentinstance= Comment(blog=blog, author=user, content=content)
            commentinstance.save()
            return redirect('blog_detail',pk=blog_id)
    return redirect('blog_detail', pk=blog_id)



@login_required(login_url='/')
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    if request.method == 'POST':
        user = request.user
        if user not in comment.liked_by.all():
            comment.liked_by.add(user)
            comment.likes += 1
            comment.save()
        else:
            comment.liked_by.remove(user)
            comment.likes -= 1
            comment.save()
    
    # Redirect back to the blog detail page
    return redirect('blog_detail', pk=comment.blog.pk)


@login_required(login_url='/')
def share_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        recipient_email = request.POST.get('email')
        message = f"Check out this blog: {blog.title}\n\n{blog.content}"
        send_mail('A Blog Shared With You', message, Blog.author.email, [recipient_email])
        return redirect('blog_detail', pk=blog_id)
    return render(request, 'share_blog.html', {'blog': blog})


def logout_view(request):
    logout(request)  # Logs out the user
    return render(request,'index.html')