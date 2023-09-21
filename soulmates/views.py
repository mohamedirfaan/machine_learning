from django.shortcuts import render,redirect
from django.forms import ModelForm
from .forms import regform,postform
from .models import post_photos_and_videos,Member,friendlist,Friendrequest,MemberManager,public_chat_room,public_room_chat_messages,private_chat,private_chat_messages
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import HttpResponsePermanentRedirect
import profile
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
cid=0
def home(request):
    try:
        if request.user.is_authenticated:
            try:
                form = request.session.get('form')
                print(form)
                mem=Member.objects.filter(id__in=form)
                currentuser=request.session.get('currentuser')
                currentuser=Member.objects.get(id=currentuser)
                condition = request.session.get('condition')
                condition=int(condition)
                posts = post_photos_and_videos.objects.all()
                return render(request,'index.html',{'form':mem,'currentuser':currentuser,'condition':condition,'posts':posts})
            except Exception as e:
                print(e)
                return render(request,"index.html")
        else:
            return redirect(login_user)
    except Exception as e:
        return redirect(login_user)
    #return render(request,"login.html")

def logout_user(request):
    logout(request)
    #return render(request,'index.html',{'status':'login successful'})
    return redirect(home)



@csrf_exempt
def login_user(request):
    if request.method=="POST":
        print("entered login phase ")
        username=request.POST['username']
        password=request.POST['password']
        #print(username,password)
        print(username,password)
        user=authenticate(email=username,password=password)
        print(user)
        if user is not None:
            login(request,user)
            member1=Member.objects.get(id=request.user.id)
            print("member 1=",member1)
            member=Member.objects.exclude(id=member1.id).values_list('id',flat=True)
            cid=member1.id
            member1=Member.objects.get(id=request.user.id)
            
            request.session['form'] = list(member)
            request.session['currentuser'] = int(member1.id)
            request.session['condition'] = 1
            print("redirected")
            return redirect(home)
        else:
            messages.success(request,"Username not available...")
            return render(request,'login.html',{'status':'login failed'})
    else:
        return render(request,'login.html')

def register(request):
    if(request.method=="POST"):
        submitted=False
        if request.method=="POST":
            form=regform(request.POST,request.FILES)
            if form.is_valid():
                member=form.save(commit=False)
                member.owner=request.user.id
                a=MemberManager
                print(form.cleaned_data.get('profile_pic'))
                user=Member.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    email=form.cleaned_data.get('email'),
                    password=str(form.cleaned_data.get('password')),
                    gender=form.cleaned_data.get('gender'),
                    profile_pic=form.cleaned_data.get('profile_pic'),
                    )
                #user = authenticate(username=form.cleaned_data.get('username'),email=form.cleaned_data.get('email'),password=str(form.cleaned_data.get('password')))
                #login(request,user)
                #member.save()
        return redirect(login_user)
    else:
        form=regform()
        return render(request,'register.html',{'form':form})
from django.http import JsonResponse

def pprofile(request,id):
    if request.method=="POST":
        print(id)
        print("in post method")
        user=request.user
        payload={}
        if user.is_authenticated:
            user_id=id
            if user_id:
                receiver=Member.objects.get(pk=user_id)
                try:
                    friend_request=Friendrequest.objects.filter(sender=user,receiver=receiver)
                    try:
                        for request in friend_request:
                            if request.is_active:
                                raise Exception("already a friend")
                        friend_request=Friendrequest(sender=user,receiver=receiver)
                        friend_request.save()
                        payload['response']="friend request sent"
                    except Exception as e:
                        payload['response']=str(e)
                except Friendrequest.DoesNotExist:
                    friend_request=Friendrequest(sender=user,receiver=receiver)
                    friend_request.save()
                    payload['response']="sent"
                if payload['response']==None:
                    payload['response']="something went wrong"
            else:
                payload['response']="unable to send friend request"
        else:
            payload['response']="you must be autheticated to send a friend request"
        #return redirect(home)
        result={'status':payload['response']}
        return JsonResponse(payload)
        # return HttpResponse(json.dumps(payload),content_type="application/json")
        #return HttpResponse(payload['response'])
        #return HttpResponsePermanentRedirect(request.path)
    else:
        print("viewing profile of : ",id)
        print(id)
        member1=Member.objects.get(id=id)
        context={}
        try:
            my_profile=Member.objects.get(pk=id)
        except Exception as e:
            return HttpResponse("something went wrong..")
        if my_profile:
            is_self=True
            is_friend=False
            user=request.user
            print(user)
            if my_profile!=user and user.is_authenticated:
                is_self=False
            elif not user.is_authenticated:
                is_self=False
            context['is_self']=is_self
            context['is_friend']=is_friend
        context['usera']=member1
        context['profile']=profile
        print("prifile",profile)
        context['condition']=0
        context['requestcount']=Friendrequest.objects.filter(receiver=my_profile.id).count()
        membertablevalues=Member.objects.all()
        friendrequestvalues=Friendrequest.objects.filter(receiver=my_profile.id)#.values()
        joinedvalues=membertablevalues.filter(id__in=friendrequestvalues.values_list('sender_id',flat=True))
        print("request.user = ",request.user)
        try:
            f=friendlist.objects.get(user=request.user.id)
            print("request user id",request.user.id)
            m=f.get_friends().values_list('id',flat=True)
            m=list(m)
            print("member1.id ",member1.id,"m=",m)
            print(member1.id in m)
            if member1.id in m:
                is_friend=True
            friendsindeed=Member.objects.filter(id__in=m)
            context['friendsindeed']=friendsindeed
        except Exception as e:
            context['friendsindeed']=[]
        try:
            is_request=Friendrequest.objects.get(sender=request.user.id,receiver=my_profile.id)
            print("is_request = ",is_request)
            if is_request:
                is_request=True
        except Exception as e:
            print(e)
            is_request=False
        context['request']=joinedvalues
        context['is_request']=is_request
        context['is_friend']=is_friend
        try:
            frnd=friendlist.objects.get(user=member1.id)
            context['frndcount']=frnd.get_friends_count()
        except:
            context['frndcount']=0
        return render(request,'profile.html',context)

def message1(request,id):
    print("message 1")
    if(request.method=="POST"):
        submitted=False
        if request.method=="POST":
            form=postform(request.POST,request.FILES)
            if form.is_valid():
                member=form.save(commit=False)
                member.owner=request.user.id
                #a=MemberManager
                print(form.cleaned_data.get('post_or_video'),form.cleaned_data.get('tags'))
                post=post_photos_and_videos.objects.create(
                    post_or_video=form.cleaned_data.get('post_or_video'),
                    tags=form.cleaned_data.get('tags'),
                    )
        return redirect(message1)
    else:
        try:
            fri=friendlist.objects.get(user=request.user)
            fri_list=fri.get_friends()
        except Exception as e:
            fri_list=[]  
        print(request.user) 
        rooms=public_chat_room.objects.filter(users=request.user)
        print(rooms)
        rooms=list(rooms)
        private_chat_details = private_chat.objects.get(id=id)
        try:
            private_messages=private_chat_messages.objects.filter(private_chat=private_chat_details)
        except Exception as e:
            print("this is an exception")
            print(e)
            private_messages=[]
        print("private messages : ",private_messages)
        try:
            private_chatters = private_chat.objects.filter(user=request.user)
            private_chatters=list(private_chatters)
            private_chatters1 = private_chat.objects.filter(title=request.user)
            private_chatters1=list(private_chatters1)
            private_chatters.extend(private_chatters1)
        except Exception as e:
            private_chatters=[]
            print("excepttion aa paru da ",e)
        post_form = postform()
        print("private chatters : ",private_chatters)
        currentuser=Member.objects.get(id=request.user.id)
        return render(
                request,"message.html",
                {
                    'room_details':private_chat_details,
                    'friends':fri_list,
                    'rooms':rooms,
                    'private_messages':private_messages,
                    'currentuser':currentuser,
                    'private_chatters':private_chatters,
                    'is_room':0,
                    'is_private':1,
                    'post_form':post_form,
                }
            )

def message(request,id=-1):
    print("unique message")
    if(request.method=="POST"):
        submitted=False
        if request.method=="POST":
            form=postform(request.POST,request.FILES)
            if form.is_valid():
                member=form.save(commit=False)
                member.owner=request.user.id
                #a=MemberManager
                print(form.cleaned_data.get('post_or_video'),form.cleaned_data.get('tags'))
                post=post_photos_and_videos.objects.create(
                    post_or_video=form.cleaned_data.get('post_or_video'),
                    tags=form.cleaned_data.get('tags'),
                    )
        return redirect(message)
    else:
        try:
            fri=friendlist.objects.get(user=request.user)
            fri_list=fri.get_friends()
        except Exception as e:
            fri_list=[]  
        print(request.user) 
        rooms=public_chat_room.objects.filter(users=request.user)
        print(rooms)
        try:
            private_chatters = private_chat.objects.filter(user=request.user)
            print("privvate chatters 1 ",private_chatters)
            private_chatters = list(private_chatters)
            private_chatters1 = private_chat.objects.filter(title=request.user)
            print("privvate chatters 2 ",private_chatters1)
            private_chatters1=list(private_chatters1)
            private_chatters.extend(private_chatters1)
        except Exception as e:
            print("Exception ",e)
        print("private chatters : ",private_chatters)
        
        if(id==-1):
            currentuser=Member.objects.get(id=request.user.id)
            post_form = postform()
            return render(request,'message.html',{'friends':fri_list,'rooms':rooms,'currentuser':currentuser,'private_chatters':private_chatters,'post_form':post_form})
        else:
            print("id = ",id)
            
            try:
                room_details=public_chat_room.objects.get(id=id)
                message_content=public_room_chat_messages.objects.filter(room=room_details)
                message_content=message_content.order_by('id')
            except Exception as e:
                print("no messages in group")
                room_details=None
                message_content=None
            print("user id=",request.user.id)
            print("image url = ",room_details.profile_pic.url)
            currentuser=Member.objects.get(id=request.user.id)  
            post_form = postform()   
            print("room daetail")
            print(room_details) 
            return render(
                request,"message.html",
                {
                    'room_details1':room_details,
                    'friends':fri_list,
                    'rooms':rooms,
                    'room_messages':message_content,
                    'currentuser':currentuser,
                    'private_chatters':private_chatters,
                    'is_room':1,
                    'is_private':0,
                    'post_form':post_form,
                }
            )



def send_friend_request(request):
    print("send request ")
    user=request.user
    payload={}
    print("type : ",request.method)
    user_id=request.POST.get('receiver_user_id')
    if user.is_authenticated and user_id!=request.user.id:
        
        if user_id:
            receiver=Member.objects.get(pk=user_id)
            try:
                friend_request=Friendrequest.objects.filter(sender=user,receiver=receiver)
                try:
                    for request in friend_request:
                        if request.is_active:
                            raise Exception("already a friend")
                    friend_request=Friendrequest(sender=user,receiver=receiver)
                    friend_request.save()
                    payload['response']="friend request sent"
                except Exception as e:
                    payload['response']=str(e)
            except Friendrequest.DoesNotExist:
                friend_request=Friendrequest(sender=user,receiver=receiver)
                friend_request.save()
                payload['response']="sent"
            if payload['response']==None:
                payload['response']="somethinf went wrong"
        else:
            payload['response']="unable to send friend request"
    else:
        payload['response']="you must be autheticated to send a friend request"
    result={'status':payload['response']}
    return JsonResponse(payload)

'''def searchresult(request,*args,**kwargs):
    context={}
    id=int(request.GET.get('currentid'))
    try:
        my_profile=Member.objects.filter(id=id).values()
    except:
        return HttpResponse("something went wrong..")
    value=request.GET.get('value')
    context['search']=value
    print(value)
    is_self=True
    is_friend=False
    user=request.user
    print(user)
    print(user,my_profile[0]['username'],str(user)!=str(my_profile[0]['username']))
    if user.is_authenticated and str(user)!=str(my_profile[0]['username']):
        is_self=False
    elif not user.is_authenticated:
        is_self=False
    context['is_self']=is_self
    context['is_friend']=is_friend
    member=Member.objects.filter(username__icontains=value)
    member1=Member.objects.get(id=id)
    context['currentuser']=member1
    context['res']=member
    return render(request,"search-result.html",context) '''

def searchresult(request):
    print("fetching result")
    name=request.POST.get('name')
    print(name)
    try:
        mem=Member.objects.filter(username__icontains=name).values()
        mem=list(mem)
    except:
        mem=[]
    print(mem)
    return JsonResponse({"search_result":mem})

from soulmates.models import Friendrequest
def get_friend_request_or_false(sender,receiver):
    try:
        return Friendrequest.objects.get(sender=sender,receiver=receiver,is_active=True)
    except Friendrequest.DoesNotExist:
        return False
    

def acceptfriendrequest(request):
    sender_user_id=int(request.user.id)
    receiver_user_id=request.POST.get('receiver_user_id')
    print("sender = ",sender_user_id,type(sender_user_id))
    print("receiver = ",receiver_user_id,type(receiver_user_id))
    receiver_user_id=int(receiver_user_id)
    print(sender_user_id,receiver_user_id)
    friendrequest=Friendrequest.objects.get(sender=receiver_user_id,receiver=sender_user_id)
    st=""
    try:
        st="accepted"
        print("accepter")
        friendrequest.accept()
        friendrequest.delete()
    except Exception as e:
        st="rejected"
        print(e)
        print("There has been some error")
    return JsonResponse({"status":st})
l=[]
def select_friends(request):
    global l
    id=request.POST.get('receiver_user_id')
    if int(id) not in l:
        l.append(int(id))
    else:
        print("in")
        l.remove(int(id))
    l=list(set(l))
    print(l)
    return JsonResponse({'list': l})

def create_room(request):
    name=request.POST.get('chat_room_name')
    print(l)
    member=Member.objects.filter(id__in=l)
    try:
        pcr=public_chat_room.objects.get(title=name)
    except Exception as e:
        pcr=public_chat_room.objects.create(title=name)
    for mem in member:
        print(mem)
        pcr.connect_user(mem)
    pcr.connect_user(request.user)
    return JsonResponse({'status':'success'})

from channels.db import database_sync_to_async

@database_sync_to_async
def send_message(roomid,userid,mess):
    print("saving message ")
    try:
        room_id=roomid
        message=mess
        try:
            current_room=public_chat_room.objects.get(id=room_id)
        except:
            current_room=public_chat_room.objects.create(id=room_id)
        message=public_room_chat_messages(user=userid,room=current_room,content=message)
        message.save()
        print("message saved ")
        #return JsonResponse({"status":"success"})
    except Exception as e:
        print("exception = ",e)
        #return JsonResponse({"status":"failed"})
    
from asgiref.sync import sync_to_async

'''async def send_message(roomid, userid, mess):
    print("sending message ")
    try:
        room_id = roomid
        message = mess
        try:
            current_room = await sync_to_async(public_chat_room.objects.get)(id=room_id)
        except public_chat_room.DoesNotExist:
            current_room = await sync_to_async(public_chat_room.objects.create)(id=room_id)

        message_obj = public_room_chat_messages(user=userid, room=current_room, content=message)
        await sync_to_async(message_obj.save)()
        print("message saved")
    except Exception as e:
        print("exception =", e)'''

def get_message(request):
    print("getting messages ")
    room_id=request.POST.get('id')
    print(room_id,type(room_id))
    messages=public_room_chat_messages.objects.filter(room=room_id)
    print(messages)
    return JsonResponse({'messages':messages})
    
def initiatemessage(request):
    receiver_user_id=request.POST.get('receiver_user_id')
    receiver_user_id=int(receiver_user_id)
    print(request.user.id,receiver_user_id)
    mem=Member.objects.get(id=receiver_user_id)
    try:
        pc=private_chat.objects.get(user=request.user,title=mem)
        return JsonResponse({'status':'already there'})
    except Exception as e:
        private_chat.objects.create(user=request.user,title=mem)
        return JsonResponse({'status':'created'})
    
from .models import post_and_video_comments

def send_comment(request):
    try:
        post_id = request.POST.get('post_id')
        post_id=int(post_id)
        comment=request.POST.get("comment")
        print(post_id,comment)
        com=post_and_video_comments.objects.create(sender=request.user,content=comment)
        current_post=post_photos_and_videos.objects.get(id=post_id)
        current_post.add_comment(com)
        return JsonResponse({'status':'success'})
    except Exception as e:
        print(e)
        return JsonResponse({'status':'failure'})
