from typing import Optional
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.

class MemberManager(BaseUserManager):
    def create_user(self,email,username,password,gender='Male',profile_pic=''):
        if not email:
            raise ValueError("users must have email address")
        if not username:
            raise ValueError("users must have a username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            password=password,
            gender=gender,
            profile_pic=profile_pic,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,username,password):
        
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.set_password(password)
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class Member(AbstractBaseUser):
    email=models.EmailField(max_length=255,unique=True)
    username=models.CharField(max_length=255)
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    #password=models.CharField(max_length=255)
    gender=models.CharField(max_length=255,null=False)
    profile_pic=models.ImageField(null=True,blank=True,upload_to='images/',default="C:\\Users\\mohamed irfaan\\OneDrive\\Pictures\\GHOST house.png")
    #my_friends=models.ManyToManyField('friendlist') 
    #f=models.ExpressionList()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    objects=MemberManager()
    def __str__(self):
        return self.username
    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,app_label):
        return True


    
class friendlist(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="user")
    friends=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name="friends")
    def __str__(self):
        return self.user.username
    def get_friends(self):
        return self.friends.all()
    def get_friends_count(self):
        return self.friends.all().count()
    def add_friend(self,account):
        #add friend
        print("adding friend")
        if account not in self.friends.all():
            self.friends.add(account)
    def remove_friend(self,account):
        #remove friend
        if account in self.friends.all():
            self.friends.remove(account)
    def unfriend(self,removee): 
        #unfriend a friend
        remover_friend_list = self
        self.remove_friend(removee)
        friend_list=friendlist.objects.get(user=removee)
        friend_list.remove_friend(self.user)
    def is_mutual_friend(self,friend):
        #are you my friend
        if friend in self.friends.all():
            return True
        return False
    

class Friendrequest(models.Model):
    """it has 2 parts sender and receiver"""
    sender=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="sender")
    receiver=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="receiver")
    is_active=models.BooleanField(blank=True,null=False,default=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.sender.username
    def accept(self):
        print("accept a friend request let the sender and receiver know")
        
        try:
            receiver_feriend_list=friendlist.objects.get(user=self.receiver)
        except Exception as e:
            receiver_feriend_list=friendlist.objects.create(user=self.receiver)
        print(receiver_feriend_list)
       
        if receiver_feriend_list:
            receiver_feriend_list.add_friend(self.sender)
            try:
                sender_friend_list=friendlist.objects.get(user=self.sender)
            except Exception as e:
                sender_friend_list=friendlist.objects.create(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.save()
        print("accepred")
    def decline(self):
        """Decline a friend request and let the sender and reveiver know"""
        self.is_active=False
        self.save()
    def cancel(self):
        """Cancel a friend request"""
        self.is_active=False
        self.save()

class public_chat_room(models.Model):
    profile_pic= profile_pic=models.ImageField(null=True,blank=True,upload_to='images/',default="C:\\Users\\mohamed irfaan\\OneDrive\\Pictures\\GHOST house.png")
    title=models.CharField(max_length=255,unique=True,blank=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,help_text="users online",blank=True)
    def __str__(self):
        return self.title
    def connect_user(self,user):
        is_user_added=False
        if not user in self.users.all():
            self.users.add(user)
            self.save()
            is_user_added=True
        elif user in self.users.all():
            is_user_added=True
        return is_user_added
    def disconnect_user(self,user):
        is_user_removed=False
        if user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed=True
        return is_user_removed
    @property
    def group_name(self):
        return "chatroom"+str(self.id)

class public_room_chat_message_manager(models.Model):
    def by_room(self,room):
        qs=public_room_chat_messages.objects.filter(room=room).order_by("-timestamp")
        return qs

class private_chat(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender_friend")
    title=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver_friend")
    def __str__(self):
        return self.user.username
    

class private_chat_messages(models.Model):
    private_chat=models.ForeignKey(private_chat,on_delete=models.CASCADE,related_name="private_chat")
    timestamp = models.DateTimeField(auto_now_add=True)
    message_sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="message_sender")
    message_receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="message_receiver")
    content = models.TextField(blank=False)
    def __str__(self):
        return self.content

class public_room_chat_messages(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user1")
    room = models.ForeignKey(public_chat_room, on_delete=models.CASCADE, related_name="room1")
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=False)

    def __str__(self):
        return self.content


class replies(models.Model):
    reply = models.CharField(max_length=255,null=False,blank=False)
    date_of_reply = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.reply

class post_and_video_comments(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="comment_sender")
    content = models.CharField(max_length=255,null=False,blank=False)
    date_of_post = models.DateTimeField(auto_now_add=True)
    #reply = models.ManyToManyField(replies)
    def add_reply(self,replies):
        self.reply.add(replies)
    def remove_reply(self,replies):
        self.reply.remove(replies)
    def get_replies(self):
        return self.reply.all()
    def __str__(self):
        return self.content

class post_photos_and_videos(models.Model):
    post_or_video=models.ImageField(null=True,blank=True,upload_to='posts/',default="C:\\Code\\project\\matrimony\\media\\img\\default.jpg")
    tags = models.CharField(null=False,blank=False,max_length=255)
    comments = models.ManyToManyField(post_and_video_comments)
    def __str__(self):
        return self.tags
    def get_comments(self):
        return self.comments.all()
    def add_comment(self,comment):
        self.comments.add(comment)
    def remove_comment(self,comment):
        self.comments.remove(comment)