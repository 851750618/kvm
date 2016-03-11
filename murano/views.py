#coding=utf8
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout

from models import User_role,Package_review
from django.contrib import messages
import re
import urllib2
import json

domain = 'http://127.0.0.1:8000/'
murano_server = '10.109.253.112'


def login_show(request):
        return render(request, 'login.html')

def login_auth(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            request.session['username'] = username
            if len(User_role.objects.filter(name=username).all()) >= 1:
                request.session['userrole'] = User_role.objects.filter(name=username).all()[0].role
                userrole_str = request.session.get('userrole')
                for i in str(userrole_str).split('_'):
                    if int(i) >= 4:
                        request.session['current_role'] = 'Admin'
                    elif int(i) >= 3:
                        request.session['current_role'] = 'Publisher'
                    elif int(i) >= 2:
                        request.session['current_role'] = 'Creator'
                    elif int(i) >= 1:
                        request.session['current_role'] = 'User'
            else:
                request.session['current_role'] = 'User'
            return HttpResponseRedirect(domain)
        else:
            messages.info(request,"用户没有被激活")
            return HttpResponseRedirect(domain + "login")
    else:
        messages.info(request,"用户不存在或者密码错误")
        return HttpResponseRedirect(domain + "login")

def logout_exit(request):
    logout(request)
    return HttpResponseRedirect(domain + "login")

def get_loginuser_role(request):
    userrole_str = request.session.get('userrole')
    roles = []
    for i in str(userrole_str).split('_'):
        if i == '1':
            roles.append('User')
        elif i == '2':
            roles.append('Creator')
        elif i == '3':
            roles.append('Publisher')
        elif i == '4':
            roles.append('Admin')
    return roles

def switch_current_userrole(request):
    role = request.GET['role']
    if role in get_loginuser_role(request):
        request.session['current_role'] = role
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

def test(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(domain + "login")
    username = request.session.get('username')
    current_role = request.session.get('current_role')
    return render(request,"base.html",{'login_user':username,'roles':get_loginuser_role(request),'current_role':current_role})

def send_post(request,url,parm,is_or_not_gettoken):
    postData = json.dumps(parm)
    req = urllib2.Request(url, postData)
    if is_or_not_gettoken == 1:
        req.add_header("Content-Type","application/json")
    else:
        req.add_header("Content-Type","application/json")
        req.add_header("X-Auth-Token",getToken(request))
    resp = urllib2.urlopen(req)
    json_data = json.loads(resp.read())
    return json_data

def send_get(request,url):
    print url
    req = urllib2.Request(url)
    req.add_header("Content-Type","application/json")
    req.add_header("X-Auth-Token",getToken(request))
    resp = urllib2.urlopen(req)
    json_data = json.loads(resp.read())
    return json_data

def send_put(request,url,parm):
    postData = json.dumps(parm)
    req = urllib2.Request(url,data=postData)
    req.get_method = lambda: 'PUT'
    req.add_header("Content-Type","application/json")
    req.add_header("X-Auth-Token",getToken(request))
    resp = urllib2.urlopen(req)
    json_data = json.loads(resp.read())
    return json_data
def send_delete(request,url):
    req = urllib2.Request(url)
    req.get_method = lambda: 'DELETE'
    req.add_header("Content-Type","application/json")
    req.add_header("X-Auth-Token",getToken(request))
    resp = urllib2.urlopen(req)
def getToken(request):
    if not request.session.has_key('murano_token'):
        values = {"auth": {"tenantName": "admin", "passwordCredentials": {"username": "admin", "password": "123456"}}}
        murano_toekn = send_post(request,"http://" + murano_server + ":5000/v2.0/tokens",values,1)['access']['token']['id']
        request.session['murano_token'] = murano_toekn
    else:
        murano_toekn = request.session.get('murano_token')
    return murano_toekn


def murano_environments(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(domain + "login")
    username = request.session.get('username')
    current_role = request.session.get('current_role')
    json_data = send_get(request,'http://' + murano_server + ':8082/v1/environments')
    environments_info = []
    id = 0
    for i in json_data['environments']:
        id = id + 1
        environment_info = {}
        environment_info['name'] = i['name']
        environment_info['status'] = i['status']
        environment_info['rid'] = i['id']
        environment_info['tenant_id'] = i['tenant_id']
        environment_info['id'] = id
        environments_info.append(environment_info)
    return render(request,'murano_environments.html',{'login_user':username,'roles':get_loginuser_role(request),'current_role':current_role,'environments_info':environments_info})

def murano_instances(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(domain + "login")
    username = request.session.get('username')
    current_role = request.session.get('current_role')
    json_data = send_get(request,'http://' + murano_server + ':8774/v2.1/24bc63132b534052a86a592560c472e5/servers/detail')
    print json_data
    instance_type = {
        '1':'m1.tiny',
        '2':'m1.small',
        '3':'m1.medium',
        '4':'m1.large',
        '42':'m1.nano',
        '451':'m1.heat',
        '5':'m1.xlarge',
        '84':'m1.micro'
    }
    instances_info = []
    id = 0
    for i in json_data['servers']:
        instance_info = {}
        id = id + 1
        instance_info['id'] = id
        instance_info['name'] = i['name']
        instance_info['type'] = instance_type[i['flavor']['id']]
        instance_info['status'] = i['status']
        add_str = str(i['addresses'])
        m = re.match(r".*u'(\d+\.\d+\.\d+\.\d+)'.*u'fixed'.*",add_str)
        if m:
            instance_info['fixed_ip'] = m.group(1)
        n = re.match(r".*u'(\d+\.\d+\.\d+\.\d+)'.*u'floating'.*",add_str)
        if n:
            instance_info['floating_ip'] = n.group(1)
        instances_info.append(instance_info)
    return render(request,'murano_instances.html',{'login_user':username,'roles':get_loginuser_role(request),'current_role':current_role,'instances_info':instances_info})

def murano_packages(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(domain + "login")
    username = request.session.get('username')
    current_role = request.session.get('current_role')
    json_data = send_get(request,'http://' + murano_server + ':8082/v1/catalog/packages')
    packages_info = []
    id = 0
    for i in json_data['packages']:
        pending_info = Package_review.objects.filter(name=i['name'])
        if len(pending_info) < 1:
            continue
        id = id + 1
        package_info = {}
        package_info['name'] = i['name']
        package_info['rid'] = i['id']
        package_info['description'] = i['description']
        package_info['id'] = id
        packages_info.append(package_info)
    return render(request,'murano_packages.html',{'login_user':username,'roles':get_loginuser_role(request),'current_role':current_role,'packages_info':packages_info,'show':1})

def quick_deploy(request):
    import time
    if request.GET['service'] == 'apache':
        time.sleep(10)
        messages.info(request,'Apache HTTP Server 已经开始部署，请稍后到我的环境中查看！')
        return HttpResponseRedirect(domain + 'murano/index/' )


def upload_package(request):
    import random,os,zipfile
    UPLOAD_ROOT = 'D:/Python_file/kvm_upload_package/'
    file_obj = request.FILES.get('package',None)
    if file_obj == None:
        return HttpResponse('file not existing in the request')
    file_name = 'temp_file-%d.zip' % random.randint(0,100000)
    file_full_path = os.path.join(UPLOAD_ROOT, file_name)
    dest = open(file_full_path,'wb+')
    dest.write(file_obj.read())
    dest.close()
    f = zipfile.ZipFile(file_full_path,'r')
    for filename in f.namelist():
        if filename == 'manifest.yaml':
            data = f.read(filename)
            import  yaml
            s = yaml.load(data)
            description = s['Description']
            name = s['Name']
            author = s['Author']
    Package_review.objects.create(user=request.session.get('username'),name=name,desc=description,author=author,status='created',path=file_full_path)
    messages.info(request,name + ' 导入成功')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def admin_review_action(request):
    username = request.session.get('username')
    current_role = request.session.get('current_role')
    if request.GET['action'] == 'get_pengding_list':
        pending_info = Package_review.objects.filter(status='in-review')
        return render(request,'package_review.html',{'login_user':username,'roles':get_loginuser_role(request),'current_role':current_role,'pending_info':pending_info,'pending_len':len(pending_info)})
    if request.GET['action'] == 'get_all_package_list':
        all_info = Package_review.objects.filter()
        return render(request,'all_packages_manage.html',{'login_user':username,'roles':get_loginuser_role(request),'current_role':current_role,'all_info':all_info})
    if request.GET['action'] == 'accept':
        id = request.GET['id']
        accept_package_info = Package_review.objects.filter(id=id)
        accept_package_info.update(status='approved')
        return HttpResponseRedirect(domain + 'murano/package_review?action=get_pengding_list')
    if request.GET['action'] == 'reject':
        id = request.GET['id']
        accept_package_info = Package_review.objects.filter(id=id)
        accept_package_info.update(status='reject')
        return HttpResponseRedirect(domain + 'murano/package_review?action=get_pengding_list')
    if request.GET['action'] == 'in-review':
        id = request.GET['id']
        accept_package_info = Package_review.objects.filter(id=id)
        accept_package_info.update(status='in-review')
        messages.info(request,'提交成功，等待审核！')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    if request.GET['action'] == 'delete':
        id = request.GET['id']
        accept_package_info = Package_review.objects.filter(id=id)
        accept_package_info.delete()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    if request.GET['action'] == 'published':
        id = request.GET['id']
        accept_package_info = Package_review.objects.filter(id=id)
        accept_package_info.update(status='published')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    if request.GET['action'] == 'unpublished':
        id = request.GET['id']
        accept_package_info = Package_review.objects.filter(id=id)
        accept_package_info.update(status='unpublished')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

def publisher_package_action(request):
    username = request.session.get('username')
    current_role = request.session.get('current_role')
    if request.GET['action'] == 'get_packages_list':
        packages_info = Package_review.objects.filter(user=username)
        return render(request, 'creator_packages.html',{'login_user':username,'roles':get_loginuser_role(request),'current_role':current_role,'packages_info':packages_info})


def murano_environment_action(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(domain + "login")
    if request.method == 'POST':
        if request.POST['action'] == 'create':
            env_name = request.POST['env_name']
            values = {"name": env_name}
            send_post(request,'http://' + murano_server + ':8082/v1/environments',values,0)
        elif request.POST['action']  == 'update':
            env_new_name = request.POST['new_name']
            env_rid = request.POST['env_rid']
            values = {"name": env_new_name}
            send_put(request,"http://" + murano_server + ":8082/v1/environments/" + env_rid,values)
    else:
        if request.GET['action']  == 'delete':
            env_rid = request.GET['env_rid']
            send_delete(request,"http://" + murano_server + ":8082/v1/environments/" + env_rid)
        elif request.GET['action'] == 'deploy':
            env_rid = request.GET['env_rid']
            print send_get(request,"http://" + murano_server + ":8082/v1/environments/%s/deployments"%env_rid,)
    return HttpResponseRedirect(domain + "murano/index")

def murano_environment_manage_components(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(domain + "login")
    username = request.session.get('username')
    current_role = request.session.get('current_role')
    env_rid = request.GET['env_rid']
    json_data = send_get(request,"http://" + murano_server + ":8082/v1/environments/" + env_rid)
    env_has_packages = []
    for i in json_data['services']:
        m = re.match(r".*u'name': u'(.*?)'",str(i))
        if m:
            env_has_packages.append(m.group(1))

    json_data = send_get(request,'http://' + murano_server + ':8082/v1/catalog/packages')
    packages_info = []
    id = 0
    for i in json_data['packages']:
        id = id + 1
        package_info = {}
        package_info['name'] = i['name']
        package_info['rid'] = i['id']
        package_info['description'] = i['description']
        package_info['id'] = id
        packages_info.append(package_info)
    return render(request,'murano_packages.html',{'login_user':username,'roles':get_loginuser_role(request),'current_role':current_role,'packages_info':packages_info,'env_has_packages':env_has_packages,'show':2})

def user_manage(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(domain + "login")
    from django.contrib.auth.models import User
    from models import User_role
    username = request.session.get('username')
    current_role = request.session.get('current_role')
    if request.method == 'POST':
        if request.POST['action'] == 'add_user':
            username = request.POST['name']
            password = request.POST['pass']
            roles_array = []
            if request.POST.has_key('1'):
                roles_array.append('1')
            if request.POST.has_key('2'):
                roles_array.append('2')
            if request.POST.has_key('3'):
                roles_array.append('3')
            string = '_'
            roles = string.join(roles_array)
            User.objects.create_user(username,password=password)
            User_role.objects.create(name=username,role=roles)
            messages.info(request,"Add user " + username + " success")
            return HttpResponseRedirect(domain + 'usermanage?action=get_users')
        elif request.POST['action'] == 'update_role':
            roles_array = []
            if request.POST.has_key('1'):
                roles_array.append('1')
            if request.POST.has_key('2'):
                roles_array.append('2')
            if request.POST.has_key('3'):
                roles_array.append('3')
            string = '_'
            update_user = request.POST['user_name']
            roles = string.join(roles_array)
            update_user_info = User_role.objects.filter(name=update_user)
            update_user_info.update(role=roles)
            messages.info(request,"Update %s roles success" % update_user)
            return HttpResponseRedirect(domain + 'usermanage?action=get_users')
    if request.method == 'GET':
        if request.GET['action'] == 'get_users':
            user_roles_tmp = User_role.objects.all()
            users_roles = []
            for i in user_roles_tmp:
                user_roles = {}
                roles_initializing = i.role
                roles_des = roles_initializing.replace('_',',').replace('1','User').replace('2','Creator').replace('3','Publisher').replace('4','Admin')
                user_roles['name'] = i.name
                user_roles['role'] = roles_des
                user_roles['role_array'] = roles_initializing.split('_')
                users_roles.append(user_roles)
            return render(request,'user_list.html',{'login_user':username,'roles':get_loginuser_role(request),'current_role':current_role,'users_roles':users_roles})
        elif request.GET['action'] == 'del_user':
            del_user_name = request.GET['user_name']
            del_user_info = User.objects.filter(username=del_user_name)
            del_user_info.delete()
            del_user_info = User_role.objects.filter(name=del_user_name)
            del_user_info.delete()
            return HttpResponseRedirect(domain + 'usermanage?action=get_users')

