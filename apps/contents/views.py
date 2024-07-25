from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post, Image, Comment, Like, Team
from apps.accounts.models import Membership, Player
from .forms import PostForm, ImageForm, CommentForm
from django.http import JsonResponse

def post_detail_json(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    is_member = Membership.objects.filter(user=request.user, team=post.team, is_active=True).exists()
    user_has_liked = Like.objects.filter(user=request.user, post=post).exists()
    likes_count = post.likes.count()

    data = {
        'username': post.user.username,
        'content': post.content,
        'images': [image.image_url.url for image in post.images.all()],
        'comments': [{'username': comment.user.username, 'content': comment.content} for comment in comments],
        'is_member': is_member,
        'user_has_liked': user_has_liked,
        'likes_count': likes_count,
    }
    return JsonResponse(data)


class UserPostListView(ListView):
    model = Post
    template_name = 'contents/user_post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        team_id = self.kwargs['team_id']
        return Post.objects.filter(user__role='user', team_id=team_id).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_id = self.kwargs['team_id']
        context['team_id'] = self.kwargs['team_id']
        context['team'] = get_object_or_404(Team, id=team_id)

         # 현재 사용자에 대한 좋아요 상태 추가
        if self.request.user.is_authenticated:
            user_likes = Like.objects.filter(user=self.request.user, post__team_id=team_id).values_list('post_id', flat=True)
            context['user_likes'] = user_likes
        else:
            context['user_likes'] = []
        
        return context
        

class PlayerPostListView(ListView):
    model = Post
    template_name = 'contents/player_post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        team_id = self.kwargs['team_id']
        return Post.objects.filter(user__role='player', team_id=team_id).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team_id = self.kwargs['team_id']
        context['team_id'] = self.kwargs['team_id']

        # 현재 사용자에 대한 좋아요 상태 추가
        if self.request.user.is_authenticated:
            user_likes = Like.objects.filter(user=self.request.user, post__team_id=team_id).values_list('post_id', flat=True)
            context['user_likes'] = user_likes
        else:
            context['user_likes'] = []
        
        
        return context

# 로그인 + 멤버쉽 가입 확인
# @login_required
# def create_post(request):
#     if request.user.role not in ['player', 'user']:
#         return HttpResponseForbidden("You are not allowed to create a post.")
    
#     team_id = request.GET.get('team_id')
#     if not team_id:
#         return HttpResponseForbidden("No team specified.")
    
#     team = get_object_or_404(Team, id=team_id)

#     is_member = Membership.objects.filter(user=request.user, team=team, is_active=True).exists()
#     is_player = Player.objects.filter(user=request.user, team=team).exists()

#     if request.user.role == 'player' and not is_player:
#         return HttpResponseForbidden("You are not a player of this team.")
    
#     if request.user.role == 'user' and not is_member:
#         return HttpResponseForbidden("You are not a member of this team.")

#     ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=3)
    
#     if request.method == 'POST':
#         post_form = PostForm(request.POST)
#         formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())

#         if post_form.is_valid() and formset.is_valid():
#             post = post_form.save(commit=False)
#             post.user = request.user
#             post.team = team
#             post.save()

#             for form in formset.cleaned_data:
#                 if form:
#                     image = form['image_url']
#                     photo = Image(post=post, image_url=image)
#                     photo.save()

#             if request.user.role == 'player':
#                 return redirect('player_post_list')
#             else:
#                 return redirect('user_post_list')
#     else:
#         post_form = PostForm()
#         formset = ImageFormSet(queryset=Image.objects.none())

#     return render(request, 'contents/post_form.html', {
#         'post_form': post_form,
#         'formset': formset,
#     })

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt
def create_post_player(request):
    if request.user.role != 'player':
        return HttpResponseForbidden("You are not allowed to create a post.")
    
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user

            try:
                player = Player.objects.get(user=request.user)
                post.team = player.team
            except Player.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Player does not exist'})
            
            post.save()

            files = request.FILES.getlist('images')
            for file in files:
                Image.objects.create(post=post, image_url=file)

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': post_form.errors})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
@csrf_exempt
def create_post_user(request):
    if request.user.role != 'user':
        return JsonResponse({'success': False, 'error': "You are not allowed to create a post."})
    
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            
            team_id = request.POST.get('team_id')
            team = get_object_or_404(Team, id=team_id)
                
            if Membership.objects.filter(user=request.user, team=team).exists():
                post.team = team
            else:
                return JsonResponse({'success': False, 'error': 'You are not a member of this team.'})
            
            post.save()

            files = request.FILES.getlist('images')
            for file in files:
                Image.objects.create(post=post, image_url=file)

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': post_form.errors})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
@csrf_exempt
def join_team(request, team_id):
    if request.method == 'POST':
        team = get_object_or_404(Team, id=team_id)

        # 이미 팀의 멤버인지 확인
        if Membership.objects.filter(user=request.user, team=team).exists():
            return JsonResponse({'success': False, 'error': 'You are already a member of this team.'})
        
        # 팀에 사용자 추가
        Membership.objects.create(user=request.user, team=team)
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})


@login_required
@csrf_exempt
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # 사용자가 플레이어인 경우 팀 확인
    if request.user.role == 'player':
        is_member = Player.objects.filter(user=request.user, team=post.team).exists()
    else:
        # 사용자가 일반 사용자(user)인 경우 멤버십 확인
        is_member = Membership.objects.filter(user=request.user, team=post.team, is_active=True).exists()

    if not is_member:
        return JsonResponse({'success': False, 'error': 'You are not a member of this team.'}, status=403)
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return JsonResponse({'success': True, 'username': comment.user.username, 'content': comment.content})
        else:
            return JsonResponse({'success': False, 'errors': comment_form.errors.as_json()})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})



@login_required
@csrf_exempt
def add_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # 사용자가 플레이어인 경우 팀 확인
    if request.user.role == 'player':
        is_member = Player.objects.filter(user=request.user, team=post.team).exists()
    else:
        # 사용자가 일반 사용자(user)인 경우 멤버십 확인
        is_member = Membership.objects.filter(user=request.user, team=post.team, is_active=True).exists()

    if not is_member:
        return JsonResponse({'success': False, 'error': 'You are not a member of this team.'}, status=403)
    
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        like.delete()
        user_has_liked = False
    else:
        user_has_liked = True
    
    likes_count = post.likes.count()
    
    return JsonResponse({'success': True, 'likes_count': likes_count, 'user_has_liked': user_has_liked})
