from django.db import models
from nanoid import generate

# Create your models here.
class Story(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    key = models.CharField(max_length=40, unique=True, editable=False, primary_key=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(null=True, blank=True)
    content = models.TextField(blank=True)
    author = models.ForeignKey('Creator.Creator', on_delete=models.CASCADE, related_name="stories")
    image = models.ForeignKey('Common.Image', on_delete=models.SET_NULL, null=True, blank=True)
    state = models.CharField(max_length=20, default='draft', choices=[
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
        ('scheduled', 'Scheduled')
    ])
    privacy = models.CharField(max_length=20, default='public', choices=[
        ('public', 'Public'),
        ('private', 'Private'),
        ('unlisted', 'Unlisted')
    ])
    tags = models.ManyToManyField('Common.Tag', blank=True,)
    category = models.ForeignKey('Common.Category', on_delete=models.SET_NULL, null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'stories'
        verbose_name = 'story'
        verbose_name_plural = 'stories'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.key = generate(size=28)
        super().save(*args, **kwargs)
        return self
    

class StoryClap(models.Model):
    id = models.CharField(max_length=40, unique=True, editable=False, primary_key=True)
    story = models.ForeignKey('Story', on_delete=models.CASCADE, related_name="claps")
    user = models.ForeignKey('User.User', on_delete=models.CASCADE, related_name="story_claps")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'story_claps'
        verbose_name = 'story clap'
        verbose_name_plural = 'story claps'
    
    def __str__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = generate(size=40)
        super().save(*args, **kwargs)
        return self
    
class StoryComment(models.Model):
    id = models.CharField(max_length=40, unique=True, editable=False, primary_key=True)
    story = models.ForeignKey('Story', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('User.User', on_delete=models.CASCADE, related_name='story_comments')
    author = models.ForeignKey('Creator.Creator', on_delete=models.CASCADE, null=True, blank=True, related_name='story_comments')
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'story_comments'
        verbose_name = 'story comment'
        verbose_name_plural = 'story comments'
    
    def __str__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        if not self.pk:  
            self.id = generate(size=40)
        super().save(*args, **kwargs)
        return self
    
    def get_votes(self):
        votes = StoryCommentVote.objects.filter(comment=self).count()
        return votes
    
    def user_vote(self, user):
        votes = StoryCommentVote.objects.filter(comment=self, user=user)
        user_vote = votes.first().id if votes.exists() else None
        return user_vote
    
class StoryCommentVote(models.Model):
    id = models.CharField(max_length=40, unique=True, editable=False, primary_key=True)
    comment = models.ForeignKey('StoryComment', on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey('User.User', on_delete=models.CASCADE)
    vote = models.CharField(max_length=20, choices=[
        ('up', 'Up'),
        ('down', 'Down')
    ], default='up')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'story_comment_votes'
        verbose_name = 'story comment vote'
        verbose_name_plural = 'story comment votes'
    
    def __str__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = generate(size=40)
        super().save(*args, **kwargs)
        return self
    


class Post(models.Model):
    key = models.CharField(max_length=40, unique=True, editable=False, primary_key=True)
    text = models.TextField(blank=True, null=True)
    type_of = models.CharField(max_length=20, default='text', choices=[
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('link', 'Link'),
        ('poll', 'Poll'),
        ('event', 'Event')
    ])
    type_poll = models.OneToOneField('PostPoll', on_delete=models.CASCADE, null=True, blank=True)
    type_image = models.OneToOneField('PostImage', on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey('Creator.Creator', on_delete=models.CASCADE, related_name="posts")
    state = models.CharField(max_length=20, default='published', choices=[
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
        ('scheduled', 'Scheduled')
    ])
    privacy = models.CharField(max_length=20, default='public', choices=[
        ('public', 'Public'),
        ('private', 'Private'),
        ('unlisted', 'Unlisted')
    ])
    tags = models.ManyToManyField('Common.Tag', blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'posts'
        verbose_name = 'post'
        verbose_name_plural = 'posts'
    
    def __str__(self):
        return self.key
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.key = generate(size=30)
        super().save(*args, **kwargs)
        return self
    

class PostClap(models.Model):
    id = models.CharField(max_length=40, unique=True, editable=False, primary_key=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="claps")
    user = models.ForeignKey('User.User', on_delete=models.CASCADE, related_name="post_claps")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'post_claps'
        verbose_name = 'post clap'
        verbose_name_plural = 'post claps'
    
    def __str__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = generate(size=40)
        super().save(*args, **kwargs)
        return self
    

class PostComment(models.Model):
    id = models.CharField(max_length=40, unique=True, editable=False, primary_key=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey('User.User', on_delete=models.CASCADE, related_name="post_comments")
    author = models.ForeignKey('Creator.Creator', on_delete=models.CASCADE, null=True, blank=True, related_name="post_comments")
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'post_comments'
        verbose_name = 'post comment'
        verbose_name_plural = 'post comments'
    
    def __str__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = generate(size=40)
        super().save(*args, **kwargs)
        return self
    
    def get_votes(self):
        votes = PostCommentVote.objects.filter(comment=self).count()
        return votes
    
    def user_vote(self, user):
        votes = PostCommentVote.objects.filter(comment=self, user=user)
        user_vote = votes.first().id if votes.exists() else None
        return user_vote
    

class PostCommentVote(models.Model):
    id = models.CharField(max_length=40, unique=True, editable=False, primary_key=True)
    comment = models.ForeignKey('PostComment', on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey('User.User', on_delete=models.CASCADE)
    vote = models.CharField(max_length=20, choices=[
        ('up', 'Up'),
        ('down', 'Down')
    ], default='up')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'post_comment_votes'
        verbose_name = 'post comment vote'
        verbose_name_plural = 'post comment votes'
    
    def __str__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = generate(size=40)
        super().save(*args, **kwargs)
        return self
    

class PostPoll(models.Model):
    id = models.CharField(max_length=40, unique=True, editable=False, primary_key=True)
    question = models.CharField(max_length=255)
    options = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'post_polls'
        verbose_name = 'post poll'
        verbose_name_plural = 'post polls'
    
    def __str__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        if not self.pk:
           self.id = generate(size=40)
        super().save(*args, **kwargs)
        return self
    
    def option_by_id(self, option_id):
        for option in self.options:
            if option['id'] == option_id:
                return option
        return None
    
    def get_votes(self):
        votes = PostPollVote.objects.filter(poll=self)
        count = votes.count()
        return votes, count
    
    def user_vote(self, user):
        votes = PostPollVote.objects.filter(poll=self, user=user)
        user_vote_id = votes.first().option if votes.exists() else None
        return user_vote_id

    

class PostPollVote(models.Model):
    id = models.CharField(max_length=40, unique=True, editable=False, primary_key=True)
    poll = models.ForeignKey('PostPoll', on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey('User.User', on_delete=models.CASCADE, related_name="poll_votes")
    option = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'post_poll_votes'
        verbose_name = 'post poll vote'
        verbose_name_plural = 'post poll votes'
    
    def __str__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = generate(size=40)
        super().save(*args, **kwargs)
        return self
    

class PostEvent(models.Model):
    id = models.CharField(max_length=40, unique=True, editable=False, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'post_events'
        verbose_name = 'post event'
        verbose_name_plural = 'post events'
    
    def __str__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = generate(size=40)
        super().save(*args, **kwargs)
        return self


class PostEventAttendee(models.Model):
    id = models.CharField(max_length=40, unique=True, editable=False, primary_key=True)
    event = models.ForeignKey('PostEvent', on_delete=models.CASCADE)
    user = models.ForeignKey('User.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'post_event_attendees'
        verbose_name = 'post event attendee'
        verbose_name_plural = 'post event attendees'
    
    def __str__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = generate(size=40)
        super().save(*args, **kwargs)
        return self
    

class PostEventSpeaker(models.Model):
    id = models.CharField(max_length=40, unique=True, editable=False, primary_key=True)
    event = models.ForeignKey('PostEvent', on_delete=models.CASCADE)
    user = models.ForeignKey('User.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'post_event_speakers'
        verbose_name = 'post event speaker'
        verbose_name_plural = 'post event speakers'
    
    def __str__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = generate(size=40)
        super().save(*args, **kwargs)
        return self
    

class PostImage(models.Model):
    id = models.CharField(max_length=40, unique=True, editable=False, primary_key=True)
    caption = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    images = models.ManyToManyField('Common.Image', related_name='images')
    
    class Meta:
        db_table = 'post_images'
        verbose_name = 'post image'
        verbose_name_plural = 'post images'
    
    def __str__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = generate(size=40)
        super().save(*args, **kwargs)
        return self
    
