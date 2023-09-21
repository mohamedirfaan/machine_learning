from django.contrib import admin

from .models import Member,friendlist,public_chat_room,Friendrequest,private_chat,private_chat_messages,post_photos_and_videos,post_and_video_comments
from django.core.paginator import Paginator
from django.core.cache import cache
from django.db import models
from .models import public_room_chat_messages
'''class MemberDetails(admin.ModelAdmin):
    readonly_fails = ('id')

admin.site.register(Member,MemberDetails)'''

class Publicchatroomadmin(admin.ModelAdmin):
    list_display=['id','title']
    search_fields=['id','title']
    list_display=['id',]
    class Meta:
        model=public_chat_room

from django.contrib.auth.admin import UserAdmin
from soulmates.models import Member
class regulator(UserAdmin):
    list_display=('email','username','date_joined','last_login','is_admin','is_staff')
    search_fields=('email','username')
    readonly_fields=('id','date_joined','last_login')
    filter_horizontal=()
    list_filter=()
    fieldsets=()
admin.site.register(Member,regulator)
class Friendlistadmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            # Only set the user field if it's a new instance
            obj.user = request.user
        super().save_model(request, obj, form, change)
    list_filter=['user']
    list_display=['user']
    search_fields=['user']
    readonly_fields=['user']
    class Meta:
        model=friendlist
class FriendRequestAdmin(admin.ModelAdmin):
    list_filter=['sender','sender','receiver']
    list_display=['sender','receiver']
    search_fields=['sender__username','sender__email','receiver__email','receiver__username']
    class Meta:
        model=Friendrequest

class CachingPaginator(Paginator):
    def _get_count(self):
        if not hasattr(self,"_count"):
            self._count=None
        if self._count is None:
            try:
                key="adm:{0}:count".format(hash(self.object_list.query.__str__()))
                self._count=cache.get(key,-1)
                if self._count==-1:
                    self._count=super().count
                    cache.set(key,self._count,3600)
            except:
                self._count=len(self.object_list)
        return self.count
    count=property(_get_count)

class publicroomchatmessagesadmin(admin.ModelAdmin):
    list_filter=['room','user','timestamp']
    list_display=['room','user','timestamp','content']
    search_fields=['room__title','user__username','content']
    readonly_fields=['id','user','room','timestamp']
    show_full_result_count=False
    #paginator=CachingPaginator
    class Meta:
        model=public_room_chat_messages

admin.site.register(friendlist,Friendlistadmin)
admin.site.register(Friendrequest,FriendRequestAdmin)
admin.site.register(public_chat_room,Publicchatroomadmin)
admin.site.register(public_room_chat_messages,publicroomchatmessagesadmin)
admin.site.register(private_chat)
admin.site.register(private_chat_messages)
admin.site.register(post_and_video_comments)
admin.site.register(post_photos_and_videos)