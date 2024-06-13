from django.db.models import OuterRef, Subquery, Max
from django.db.models.functions import Coalesce
from django.shortcuts import render, get_object_or_404, redirect
from .models import Topic, Post
from .forms import TopicForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'forum/signup.html', {'form': form})


def home(request):
    # Sous-requête pour obtenir la date du dernier message pour chaque sujet
    last_post_date_subquery = Post.objects.filter(topic=OuterRef('pk')).order_by('-created_at').values('created_at')[:1]
    
    # Annotation pour ajouter la date du dernier message à chaque sujet
    topics = Topic.objects.annotate(
        last_message_date=Coalesce(Subquery(last_post_date_subquery), 'created_at')
    ).order_by('-last_message_date', '-created_at')
    
    paginator = Paginator(topics, 10)  

    page_number = request.GET.get('page')
    try:
        topics = paginator.page(page_number)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)

    return render(request, 'forum/home.html', {'topics': topics})



def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    return render(request, 'forum/topic_detail.html', {'topic': topic})


@login_required
def new_topic(request):
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirigez vers la page d'accueil ou une autre page appropriée
    else:
        form = TopicForm()
    return render(request, 'forum/new_topic.html', {'form': form})

@login_required
def new_post(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    
    if request.method == 'POST':
        message = request.POST.get('message')
        Post.objects.create(message=message, created_by=request.user, topic=topic)
        return redirect('topic_detail', topic_id=topic.id)
    
    return render(request, 'forum/new_post.html', {'topic': topic})

