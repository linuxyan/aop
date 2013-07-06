# -*- coding: UTF-8 -*- 
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
from aopform import *
from aop.models import hosts,svns,hostgroup,scripts,tasks,scriptgroup,UserProfile
import os,paramiko,time,string
from aopproject import settings
from django.contrib.auth.models import User  
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib.auth.decorators import login_required
from aopfunction import *

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def login(request):
    if request.method == 'POST':  
            username = request.POST['username']  
            password = request.POST['password']  
            user = authenticate(username=username, password=password)  
            if user is not None:  
                if user.is_active:  
                            user_login(request, user)  
                            return HttpResponseRedirect('/')  
                else:
                    return HttpResponse('用户没有启用!')  
            else:
                return HttpResponse('用户名或者密码错误！')  
    else:
        return render_to_response('login.html')  

def loginout(request):
    user_logout(request)
    return HttpResponseRedirect('/login/') 


@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        search = request.POST.get("search",'null')
        print  request.POST,search
        qset = (
            Q(host_name__icontains = search) | 
            Q(host_w_ip__icontains = search) | 
            Q(host_w_port__icontains = search) | 
            Q(host_n_ip__icontains = search) |
            Q(host_n_port__icontains = search) |
            Q(host_user__icontains = search)
            )
        host_list = hosts.objects.filter(qset)
        paginator = Paginator(host_list, 10)
        page = request.GET.get('page')
        try:
            host = paginator.page(page)
        except PageNotAnInteger:
            host = paginator.page(1)
        except EmptyPage:
            host = paginator.page(paginator.num_pages)
        host_group = hostgroup.objects.all()
        return render(request,'showhost.html',{'hosts':host,'hostgroups':host_group})
    else:
        host_list = hosts.objects.all()
        paginator = Paginator(host_list, 10)
        page = request.GET.get('page')
        try:
            host = paginator.page(page)
        except PageNotAnInteger:
            host = paginator.page(1)
        except EmptyPage:
            host = paginator.page(paginator.num_pages)
        host_group = hostgroup.objects.all()
        return render(request,'showhost.html',{'hosts':host,'hostgroups':host_group})

@login_required(login_url='/login/')
def hostadd(request):
    if request.method == 'POST':
        form = hostform(request.POST)
        if form.is_valid():
            host_name = form.cleaned_data['host_name']
            host_user = form.cleaned_data['host_user']
            host_pass = en_str(settings.SECRET_KEY,str(form.cleaned_data['host_pass']))
            host_w_ip = form.cleaned_data['host_w_ip']
            host_w_port = form.cleaned_data['host_w_port']
            host_n_ip = form.cleaned_data['host_n_ip']
            host_n_port = form.cleaned_data['host_n_port']
            host_root_pwd = en_str(settings.SECRET_KEY,str(form.cleaned_data['host_root_pwd']))
            script_dir = form.cleaned_data['script_dir']
            host_description = form.cleaned_data['host_description']
            try:
                hosts(host_name=host_name,host_user=host_user,host_pass=host_pass,host_w_ip=host_w_ip,host_w_port=host_w_port,host_n_ip=host_n_ip,host_n_port=host_n_port,host_root_pwd=host_root_pwd,script_dir=script_dir,host_description=host_description,create_user=request.user).save()
                result = "Add Server %s success!"%host_name
            except:
                result = "Add Server %s Failed!"%host_name
                form = hostform()
                return render(request,'addhost.html',{'form':form,'result':result})
            #return render_to_response('addhost.html',{'form':form,'result':result})
            return HttpResponseRedirect('/hostadd')
    else:
        form = hostform()
    return render(request,'addhost.html',{'form':form})

@login_required(login_url='/login/')
def hostedit(request,host_id):
    host = hosts.objects.get(id=host_id)
    if request.user.username != host.create_user and request.user.username != "root":
        return HttpResponse("你木有权限编辑本条记录！")
    if request.method == 'POST':
        form = hostform(request.POST)
        if form.is_valid():
            try:
                host = hosts.objects.get(id=host_id)
                host.host_name = form.cleaned_data['host_name']
                host.host_user = form.cleaned_data['host_user']
                host.host_pass = en_str(settings.SECRET_KEY,str(form.cleaned_data['host_pass']))
                host.host_w_ip = form.cleaned_data['host_w_ip']
                host.host_w_port = form.cleaned_data['host_w_port']
                host.host_n_ip = form.cleaned_data['host_n_ip']
                host.host_n_port = form.cleaned_data['host_n_port']
                host.host_root_pwd = en_str(settings.SECRET_KEY,str(form.cleaned_data['host_root_pwd']))
                host.script_dir = form.cleaned_data['script_dir']
                host.host_description = form.cleaned_data['host_description']
                host.create_user = request.user
                host.save()
            except:
                return HttpResponse("更新服务器信息失败!")
            return HttpResponseRedirect('/')
        else:
            return HttpResponse("服务器信息不完整！")
            
    else:
        try:
            host = hosts.objects.get(id=host_id)
        except:
            return HttpResponse("服务器信息不存在！")
        form=hostform(model_to_dict(host))
        return render(request,'edithost.html',{'form':form})
    
@login_required(login_url='/login/')
def showsvn(request):
    if request.method == "POST":
        search = request.POST.get("search",'null')
        qset = (
            Q(svn_name__icontains = search) | 
            Q(svn_user__icontains = search) | 
            Q(svn_local__icontains = search) | 
            Q(svn_path__icontains = search) )
        svn_list = svns.objects.filter(qset)
        paginator = Paginator(svn_list, 10)
        page = 1
        try:
            svn = paginator.page(page)
        except PageNotAnInteger:
            svn = paginator.page(1)
        except EmptyPage:
            svn = paginator.page(paginator.num_pages)
        return render(request,'showsvn.html',{'svns':svn})        
    else:
        svn_list = svns.objects.all()
        paginator = Paginator(svn_list, 10)
        page = request.GET.get('page')
        try:
            svn = paginator.page(page)
        except PageNotAnInteger:
            svn = paginator.page(1)
        except EmptyPage:
            svn = paginator.page(paginator.num_pages)
        return render(request,'showsvn.html',{'svns':svn})

@login_required(login_url='/login/')
def svnadd(request):
    if request.method == "POST":
        form = svnform(request.POST)
        if form.is_valid():
            svn_name = form.cleaned_data['svn_name']
            svn_user = form.cleaned_data['svn_user']
            svn_pass = en_str(settings.SECRET_KEY,str(form.cleaned_data['svn_pass']))
            svn_local = form.cleaned_data['svn_local']
            svn_path = form.cleaned_data['svn_path']
            host = form.cleaned_data['host']
            try:
                svns(svn_name=svn_name,svn_user=svn_user,svn_pass=svn_pass,svn_local=svn_local,svn_path=svn_path,host=host,create_user=request.user).save()
            except:
                result = "Add Svn %s Failed!"%svn_name
                form = svnform()
                return render(request,'addsvn.html',{'form':form,'result':result})
            return HttpResponseRedirect('/svnadd')
            
    else:
        form = svnform()
        return render(request,'addsvn.html',{'form':form})

@login_required(login_url='/login/')
def svnedit(request,svn_id):
    svn = svns.objects.get(id=svn_id)
    if request.user.username != svn.create_user and request.user.username != "root":
        return HttpResponse("你木有权限编辑本条记录！")
    if request.method == 'POST':
        form = svnform(request.POST)
        if form.is_valid():
            try:
                svn = svns.objects.get(id=svn_id)
                svn.svn_name = form.cleaned_data['svn_name']
                svn.svn_user = form.cleaned_data['svn_user']
                svn.svn_pass = en_str(settings.SECRET_KEY,str(form.cleaned_data['svn_pass']))
                svn.svn_local = form.cleaned_data['svn_local']
                svn.svn_path = form.cleaned_data['svn_path']
                svn.host = form.cleaned_data['host']
                svn.create_user = request.user
                svn.save()
            except:
                return HttpResponse("更新svn信息失败！")
            return HttpResponseRedirect('/showsvn/')
    else:
        try:
            svn = svns.objects.get(id=svn_id)
        except:
            return HttpResponse("SVN信息不存在！")
        form = svnform(model_to_dict(svn))
        return render(request,'editsvn.html',{'form':form})



@login_required(login_url='/login/')
def svnupdate(request,svn_id,u_type):
    svn = svns.objects.get(id =svn_id)
    host = svn.host
    u_type = u_type.encode('utf-8')
    if u_type == "1":
        cmd = r"svn update %s" %svn.svn_local
    elif u_type == "2":
        version_cmd = r"svn info %s |grep Revision: |awk '{print $2}'" %svn.svn_local
        try:
            now_version = ordinary_ssh(host=host.host_w_ip,username=host.host_user,password=host.host_pass,port=host.host_w_port,cmd=version_cmd)
        except:
            HttpResponse("获取当前版本失败！")
        print now_version
        restore_version = string.atoi(now_version)-1
        cmd = r"svn up -r %d  %s" %(restore_version,svn.svn_local)
    logname = time.strftime("%Y-%m-%d")+"-svn.log"
    svnlog = os.path.join(settings.WEB_ROOT,'..\\','aop','svnlog\\').replace('\\','/') +logname
    try:
        result = verification_ssh(host=host.host_w_ip,username=host.host_user,password=host.host_pass,port=host.host_w_port,root_pwd=host.host_root_pwd,cmd=cmd)
    except Exception as e:
        return HttpResponse(str(e))
    if not os.path.exists(svnlog):
        f = open(svnlog,'a')
        f.close()
    out = open(svnlog,'a')
    svnname = svn.svn_name
    ss = '<br>'+str(time.strftime('%Y-%m-%d %H:%M'))+'<br>'
    result = ss + svnname.encode('utf-8') + ":<br>" +result.replace('\n','<br>')
    out.write(result.replace('<br>','\n')+'\n')
    out.write('\n-----------------------------------------------------------------\n')
    out.close()
    return render(request,'svnlog.html',{'result':result,'svnname':svnname})

@login_required(login_url='/login/')
def showsvnlog(request):
    logname = time.strftime("%Y-%m-%d")+"-svn.log"
    svnlog = os.path.join(settings.WEB_ROOT,'..\\','aop','svnlog\\').replace('\\','/') +logname
    try:
        f = open(svnlog)
        result = f.read()
        result = result.replace('\n','<br>')
    except Exception as e:
        return HttpResponse("读取日志失败！<br> %s" %str(e))
    f.close()
    return render(request,'svnlog.html',{'result':result})


@login_required(login_url='/login/')
def hostdel(request,host_id):
    host = hosts.objects.get(id=host_id)
    if request.user.username != host.create_user and request.user.username != "root":
        return HttpResponse("你木有权限删除本条记录！")
    svn = svns.objects.filter(host_id=host_id)
    return render(request,'delhost.html',{'svns':svn,'host_id':host_id})

#确认删除服务器信息以及svn信息
@login_required(login_url='/login/')
def confirm_del(request,host_id):
    host = hosts.objects.get(id=host_id)
    if request.user.username != host.create_user and request.user.username != "root":
        return HttpResponse("你木有权限删除本条记录！")
    hosts.objects.filter(id=host_id).delete()
    return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def addscript(request):
    if request.method == 'POST':
        form = scriptform(request.POST,request.FILES)
        if form.is_valid():
            script_name = request.POST.get('script_name')
            script_file = request.FILES.get('script_file')
            script_date = time.strftime('%Y-%m-%d %H:%M')
            script_description = request.POST.get('script_description')
            scripts(script_name=script_name,script_file=script_file,script_date=script_date,script_description=script_description,create_user=request.user).save()
            return HttpResponseRedirect('/showscript/')
        else:
            return HttpResponse("Upload script Failed!")
    else:
        form = scriptform()
    return render(request,'script.html',{'form':form})

@login_required(login_url='/login/')
def showscript(request):
    if request.method == 'POST':
        search = request.POST.get("search",'null')
        qset = (
            Q(script_name__icontains = search) | 
            Q(script_file__icontains = search) | 
            Q(script_date__icontains = search) | 
            Q(script_description__icontains = search)
            )
        script_list = scripts.objects.filter(qset)
        paginator = Paginator(script_list, 10)
        page = request.GET.get('page')
        try:
            script = paginator.page(page)
        except PageNotAnInteger:
            script = paginator.page(1)
        except EmptyPage:
            script = paginator.page(paginator.num_pages)
        script_group = scriptgroup.objects.all()
        return render(request,'showscript.html',{'scripts':script,'scriptgroups':script_group})        
    else:
        script_list = scripts.objects.all()
        paginator = Paginator(script_list, 10)
        page = request.GET.get('page')
        try:
            script = paginator.page(page)
        except PageNotAnInteger:
            script = paginator.page(1)
        except EmptyPage:
            script = paginator.page(paginator.num_pages)        
        script_group = scriptgroup.objects.all()
        return render(request,'showscript.html',{'scripts':script,'scriptgroups':script_group})

@login_required(login_url='/login/')
def delscript(request,script_id):
    script = scripts.objects.get(id=script_id)
    if request.user.username != script.create_user and request.user.username != "root":
        return HttpResponse("你木有权限删除本条记录！")
    scripts.objects.filter(id=script_id).delete()
    return HttpResponseRedirect('/showscript/')

@login_required(login_url='/login/')
def group(request):
    if request.method == 'POST':
        grouptype = request.POST['grouptype']
        if grouptype == "servergroup":
            form = hostgroupform(request.method)
            if form.is_valid:
                host_groupname = request.POST['host_groupname']
                create_date = time.strftime('%Y-%m-%d %H:%M')
                group = hostgroup()
                group.host_groupname=host_groupname
                group.create_date = create_date
                group.create_user = request.user
                group.save()
        else:
            form = scriptgroupform(request.method)
            if form.is_valid:
                script_groupname = request.POST['script_groupname']
                create_date = time.strftime('%Y-%m-%d %H:%M')
                group = scriptgroup()
                group.script_groupname = script_groupname
                group.create_date = create_date
                group.create_user = request.user
                group.save()
        return HttpResponseRedirect('/group/')
    else:
        host_group_form = hostgroupform()
        hostgroups = hostgroup.objects.all()  
        script_group_form = scriptgroupform()
        scriptgroups = scriptgroup.objects.all()
    return render(request,'group.html',{'host_group_form':host_group_form,'script_group_form':script_group_form,'hostgroups':hostgroups,'scriptgroups':scriptgroups})

@login_required(login_url='/login/')
def hostgroup_detail(request,group_id):
    host_group = hostgroup.objects.get(id=group_id)
    host_list = host_group.host.all()
    return render(request,'hostgroup_detail.html',{'host_group':host_group,'host_list':host_list})

@login_required(login_url='/login/')
def scriptgroup_detail(request,group_id):
    script_group = scriptgroup.objects.get(id=group_id)
    script_list = script_group.script.all()
    return  render(request,'scriptgroup_detail.html',{'script_group':script_group,'script_list':script_list})

@login_required(login_url='/login/')
def hostgroup_del(request,group_id):
    host_group = hostgroup.objects.get(id=group_id)
    if request.user.username != host_group.create_user and request.user.username != "root":
        return HttpResponse("你木有权限删除本条记录！")    
    hostgroup.objects.filter(id=group_id).delete()
    return HttpResponseRedirect('/group/')

@login_required(login_url='/login/')
def hostgroup_del_host(request):    
    if request.method == 'POST':
        try:
            group_id=request.POST['group_id']
            host_id = request.POST['host_id']
            host_group = hostgroup.objects.get(id=group_id)
            host = hosts.objects.get(id=host_id)
            host_group.host.remove(host)
            result = "success"
            return HttpResponse(result,mimetype='application/html')
        except:
            result = "error"
            return HttpResponse(result,mimetype='application/html')

@login_required(login_url='/login/')
def scriptgroup_del(request,group_id):
    script_group = scriptgroup.objects.get(id=group_id)
    if request.user.username != script_group.create_user and request.user.username != "root":
        return HttpResponse("你木有权限删除本条记录！") 
    scriptgroup.objects.filter(id=group_id).delete()
    return HttpResponseRedirect('/group/')

@login_required(login_url='/login/')
def scriptgroup_del_script(request):
    if request.method == 'POST':
        try:
            group_id = request.POST['group_id']            
            script_id = request.POST['script_id']
            script_group = scriptgroup.objects.get(id=group_id)
            script = scripts.objects.get(id=script_id)
            script_group.script.remove(script)
            result = "success"
            return HttpResponse(result,mimetype='application/html')
        except:
            result = "error"
            return HttpResponse(result,mimetype='application/html')

@login_required(login_url='/login/')
def addtogroup(request):
    if request.method == 'POST':
        grouptype = request.POST['grouptype']
        if grouptype == "servergroup":
            host_id = request.POST['host_id']
            group_id = request.POST['group_id']
            host = hosts.objects.get(id=host_id)
            group = hostgroup.objects.get(id=group_id)
            try :
                group.host.get(id=host_id)
                result = str(host.host_name)+". Already Exists Server Group  ."+str(group.host_groupname)+".  Add to Server Group Failed!"
            except:
                group.host.add(host)
                group.save()
                result = str(host.host_name)+". add to Server Group ."+str(group.host_groupname)+". Success!"
            return HttpResponse(result,mimetype='application/html')
        elif grouptype == "scriptgroup":
            script_id = request.POST['script_id']
            group_id = request.POST['group_id']
            script = scripts.objects.get(id=script_id)
            group = scriptgroup.objects.get(id=group_id)
            try:
                group.script.get(id=script_id)
                result = str(script.script_name) +"Already Exists Script Group"+str(group.script_groupname)+". Add to Script Group Failed!"
            except:
                group.script.add(script)
                group.save()
                result = str(script.script_name)+". add to Server Group ."+str(group.script_groupname)+". Success!"
            return HttpResponse(result,mimetype='application/html')
            
    else:
        return HttpResponse("xx")


@login_required(login_url='/login/')
def task(request):  
    if request.method == 'POST':
        form = taskform(request.POST)
        if form.is_valid():
            try:
                task_name = form.cleaned_data['task_name']
                script_group = form.cleaned_data['script_group']
                host_group = form.cleaned_data['host_group']
                task_date = time.strftime('%Y-%m-%d %H:%M')
                task_status = "0"
                task = tasks()
                task.task_name = task_name
                task.script_group = script_group
                task.host_group = host_group
                task.task_date = task_date
                task.task_status = task_status
                task.task_create_user = request.user
                task.save()
                return HttpResponseRedirect('/task/')
            except:
                return HttpResponse("添加任务失败！")
    else:
        form = taskform()
        task_list = tasks.objects.all()
    return render(request,'task.html',{'form':form,'task_list':task_list})

@login_required(login_url='/login/')
def task_del(request,task_id):
    task = tasks.objects.get(id=task_id)
    if request.user.username != task.task_create_user and request.user.username != "root":
        return HttpResponse("你木有权限删除本条记录！")
    tasks.objects.filter(id=task_id).delete()
    return HttpResponseRedirect('/task/')


@login_required(login_url='/login/')
def task_run(request):
    if request.method == 'POST':
        task_id = request.POST['task_id']
        task = tasks.objects.get(id=task_id)
        if request.user.username != task.task_create_user and request.user.username != "root":
            result = "没有权限执行此任务!"
            return HttpResponse(result,mimetype='application/html')
        task = tasks.objects.get(id=task_id)
        host_list = task.host_group.host.all()
        script_list = task.script_group.script.all()
        tasklogname = "task_"+str(task.task_name)+".log"
        tasklogpath = os.path.join(settings.WEB_ROOT,'..\\','aop','tasklog\\').replace('\\','/') +tasklogname
        try:
            start_task_thread(tasklogpath,host_list,script_list)
            result = "Add Task queue Success!"
        except:
            result = "Add Task queue Faild!"
        return HttpResponse(result,mimetype='application/html')
    
@login_required(login_url='/login/')
def task_status(request,task_id):
    form = taskform()
    task_list = tasks.objects.all()
    task = tasks.objects.get(id=task_id)
    task_log = "task_"+str(task.task_name)+".log"
    tasklogpath = os.path.join(settings.WEB_ROOT,'..\\','aop','tasklog\\').replace('\\','/') +task_log
    try:
        f = open(tasklogpath,'r')
        all_text = f.read()
        result = all_text.replace('\n','<br>')
        return render(request,'task.html',{'form':form,'task_list':task_list,'result':result})
    except:
        result = "read result Faild!"
        return render(request,'task.html',{'form':form,'task_list':task_list,'result':result})

@login_required(login_url='/login/')
def showuser(request):
    users = User.objects.all()
    return render(request,'showuser.html',{'users':users})

@login_required(login_url='/login/')
def adduser(request):
    if request.user.username != "root":
        return HttpResponse("你木有权限添加用户！")
    if request.method == 'POST':
        form = userform(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']
                user = User.objects.create_user(username=username,password=password,email=email)
                user.save()
                name = request.POST['xingming']
                iphone = request.POST['iphone']
                UserProfile(user=user,name=name,iphone=iphone).save()
                return HttpResponseRedirect('/showuser/')
            except Exception as e:
                return HttpResponse(e)
    else:
        form = userform()
        return render(request,'adduser.html',{'form':form})

@login_required(login_url='/login/')
def deluser(request,user_id):
    if request.user.username != "root":
        return HttpResponse("你木有权限删除此用户！")
    User.objects.filter(id=user_id).delete()
    return HttpResponseRedirect('/showuser/')

@login_required(login_url='/login/')
def edituser(request,user_id):
    if request.method == 'POST':
        try:
            password = request.POST['password']
            name = request.POST['xingming']
            iphone = request.POST['iphone']
            email = request.POST['email']
            user = User.objects.get(id=user_id)
            user.email = email
            user.set_password(password)
            user.save()
            userprofile = UserProfile.objects.get(user=user)
            userprofile.name = name 
            userprofile.iphone = iphone
            userprofile.save()
            return HttpResponseRedirect('/showuser/')
        except Exception as e:
            return HttpResponse(e)
        
    else:
        user = User.objects.get(id=user_id)
        return render(request,'edituser.html',{'user':user})



def test(request):
    return render_to_response('showhost_bak.html')




#from django.contrib.auth.models import User;
#user = User.objects.create_user(username='updatesvn',password='updatesvn123',email='a@a.com')
#user.save
#user.set_password("L8ka65##702")
#user.save()