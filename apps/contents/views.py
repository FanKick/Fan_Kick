from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post, Image
from .forms import PostForm, ImageForm


class PostDetailView(DetailView):
    model = Post
    template_name = 'contents/post_detail.html'
    context_object_name = 'post'


class PlayerPostListView(ListView):
    model = Post
    template_name = 'contents/player_post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(user__role='player')

class UserPostListView(ListView):
    model = Post
    template_name = 'contents/user_post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(user__role='user')


@login_required
def create_post(request):
    if request.user.role not in ['player', 'user']:
        return HttpResponseForbidden("You are not allowed to create a post.")
    
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=3)
    
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())

        if post_form.is_valid() and formset.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user  # 현재 로그인한 유저를 작성자로 설정
            post.save()

            for form in formset.cleaned_data:
                if form:
                    image = form['image_url']
                    photo = Image(post=post, image_url=image)
                    photo.save()

            # 역할에 따라 다른 리스트 뷰로 리디렉션
            if request.user.role == 'player':
                return redirect('player_post_list')
            else:
                return redirect('user_post_list')
            
    else:
        post_form = PostForm()
        formset = ImageFormSet(queryset=Image.objects.none())

    return render(request, 'contents/post_form.html', {
        'post_form': post_form,
        'formset': formset,
    })