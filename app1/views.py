from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm,PostForm,CommentForm,StoryForm,SearchForm,MessageForm
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from app1.models import Post,Like,Comment,CustomUser,Story,Conversation,Message
from django.db.models import Count
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone

def home1(request):
    return HttpResponse("welcomew to instagram kevin from ceo")

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    users = CustomUser.objects.annotate(followers_count=Count('followers')).order_by('-followers_count')
    recent_stories = Story.objects.order_by('-created_at')[:3]
    context = {
        'posts':posts,
        'users':users,
        'recent_stories':recent_stories
        
    }
    return render(request, 'home_copy1.html', context)
    
# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('home')  # Redirect to home page after successful registration
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    users = CustomUser.objects.annotate(followers_count=Count('followers')).order_by('-followers_count')
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        
        'users':users,
        'form':form
        
    }
    return render(request, 'profile.html', context)

# @login_required
# def all_post(request):
#     posts=Post.objects.all()
#     return render(request,'home1.html',{'posts':posts})

# @login_required
# def create_post(request):
#     if request.method=="POST":
#         form=PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('all_post')
#     else:
#         form=PostForm()
#     return render(request,'create_post.html',{'form':form})



@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Your post has been created!')
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been updated!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been deleted!')
        return redirect('home')
    return render(request, 'delete_post.html', {'post': post})


# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'post_detail.html', {'post': post})

@login_required
def user_posts(request):
    posts = Post.objects.filter(user=request.user)
    return render(request, 'user_posts.html', {'posts': posts})

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        # User has already liked the post, so unlike it
        like.delete()
    
    likes_count = post.likes.count()
    return JsonResponse({'likes_count': likes_count})

@login_required
def share_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Implement your sharing logic here
    # For example, you could create a new post that references this one
    # or send a notification to the user's followers
    return JsonResponse({'success': True, 'message': 'Post shared successfully'})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return JsonResponse({'likes_count': post.likes.count()})

@login_required
def share_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Implement sharing functionality (e.g., create a new post with reference to the original)
    messages.success(request, 'Post shared successfully!')
    return redirect('post_detail', pk=post.pk)

def user_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    posts = user.posts.all()
    is_following = request.user.is_authenticated and request.user.following.filter(username=username).exists()
    return render(request, 'user_profile.html', {'profile_user': user, 'posts': posts, 'is_following': is_following})

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(CustomUser, username=username)
    if request.user != user_to_follow:
        if request.user.following.filter(username=username).exists():
            request.user.following.remove(user_to_follow)
            is_following = False
        else:
            request.user.following.add(user_to_follow)
            is_following = True
        return JsonResponse({'is_following': is_following, 'followers_count': user_to_follow.followers.count()})
    return JsonResponse({'error': 'You cannot follow yourself'}, status=400)

def explore_users(request):
    users = CustomUser.objects.annotate(followers_count=Count('followers')).order_by('-followers_count')
    return render(request, 'explore_users.html', {'users': users})


@login_required
def create_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            messages.success(request, 'Your story has been created!')
            return redirect('home')
    else:
        form = StoryForm()
    return render(request, 'create_story.html', {'form': form})

def story_detail(request, pk):
    story = get_object_or_404(Story, pk=pk)
    return render(request, 'story_detail.html', {'story': story})


def all_stories(request):
    # Fetch all stories
    stories = Story.objects.all()
    return render(request, 'all_stories.html', {'stories': stories})

@login_required
def delete_story(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if request.user == story.user:
        story.delete()
        messages.success(request, 'Your story has been deleted.')
    else:
        messages.error(request, 'You do not have permission to delete this story.')
    return redirect('home')



from django.db.models import Q
from app1.models import CustomUser, Post
from django.shortcuts import render

def search(request):
    form = SearchForm(request.GET)
    user_results = []
    post_results = []
    
    if form.is_valid():
        query = form.cleaned_data['query']
        
        # Search for CustomUser matches
        user_results = CustomUser.objects.filter(Q(username__icontains=query) | Q(bio__icontains=query))
        
        # Search for Post matches
        post_results = Post.objects.filter(Q(caption__icontains=query) | Q(tags__name__icontains=query))
    
    # Combine both results into a single list
    results = list(user_results) + list(post_results)
    
    return render(request, 'search_results.html', {'form': form, 'results': results})



@login_required
def inbox(request):
    conversations = request.user.conversations.all().order_by('-updated_at')
    return render(request, 'inbox.html', {'conversations': conversations})

@login_required
def conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    messages = conversation.messages.all().order_by('timestamp')
    form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            return redirect('conversation', conversation_id=conversation.id)

    return render(request, 'conversation.html', {
        'conversation': conversation,
        'messages': messages,
        'form': form
    })

@login_required
def new_conversation(request, username):
    recipient = get_object_or_404(CustomUser, username=username)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            conversation = Conversation.objects.create()
            conversation.participants.add(request.user, recipient)
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            return redirect('conversation', conversation_id=conversation.id)
    else:
        form = MessageForm()
    
    return render(request, 'new_conversation.html', {'form': form, 'recipient': recipient})

@login_required
def load_messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    messages = conversation.messages.all().order_by('-timestamp')[:20]
    message_list = []
    for message in reversed(messages):
        message_list.append({
            'id': message.id,
            'content': message.content,
            'sender': message.sender.username,
            'timestamp': message.timestamp.isoformat(),
            'is_read': message.is_read
        })
    return JsonResponse({'messages': message_list})
