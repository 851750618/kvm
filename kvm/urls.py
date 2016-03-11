"""kvm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','murano.views.test',),
    url(r'^login/$','murano.views.login_show',),
    url(r'^login_auth/$','murano.views.login_auth',),
    url(r'^logout/$','murano.views.logout_exit',),
    url(r'^murano/index/$','murano.views.murano_environments',),
    url(r'^murano/envaction/$','murano.views.murano_environment_action',),
    url(r'^murano/managecomponents','murano.views.murano_environment_manage_components',),
    url(r'^murano/instances/$','murano.views.murano_instances',),
    url(r'^murano/packages/$','murano.views.murano_packages',),
    url(r'^murano/upload_package','murano.views.upload_package',),
    url(r'^murano/package_review','murano.views.admin_review_action',),
    url(r'^murano/publisher_package','murano.views.publisher_package_action',),
    url(r'^switch_role','murano.views.switch_current_userrole',),
    url(r'murano/quick_deploy','murano.views.quick_deploy'),

    url(r'^wso2/index','wso2.views.get_webapp_list',),
    url(r'^wso2/add_new_web_app/$','wso2.views.create_web_app_old',),
    url(r'^wso2/my_subscriptions/$','wso2.views.get_my_subs',),
    url(r'wso2/change_life_cycle','wso2.views.change_life_cycle'),
    url(r'wso2/webapp','wso2.views.get_all_published'),
    url(r'wso2/sub_app','wso2.views.sub_one_webapp'),

    url(r'^usermanage','murano.views.user_manage',),
]
