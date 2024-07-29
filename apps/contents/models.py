from django.utils import timezone
from django.db import models
from apps.accounts.models import CustomUser, Team

class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    @property
    def total_comments_count(self):
        total_replies_count = sum(comment.replies_count for comment in self.comments.all())
        return self.comments.count() + total_replies_count
    
    @property
    def likes_count(self):
        return self.likes.count()

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image_url = models.ImageField(upload_to='media/post_images/')

    def __str__(self):
        return f"Image for post: {self.post.title}"
    
class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')  # 대댓글을 위한 자기 참조 필드
    content = models.TextField()  # 댓글의 내용 필드
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
    
    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def replies_count(self):
        return self.replies.count()

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)

    def __str__(self):
        if self.post:
            return f"Like by {self.user.username} on {self.post.title}"
        elif self.comment:
            return f"Like by {self.user.username} on a comment"
        else:
            return f"Like by {self.user.username}"