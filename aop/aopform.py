# -*- coding: UTF-8 -*- 
from django.forms import ModelForm
from aop.models import *
from django import forms
from django.contrib.auth.models import User 


class hostform(ModelForm):
    host_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Host Name"}))
    host_user = forms.CharField(widget=forms.TextInput(attrs={"class":"input-medium","placeholder":"login user"}))
    host_w_ip = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Inter ip"}))
    host_w_port = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Inter port","class":"input-mini"}))
    host_n_ip = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"local ip"}))
    host_n_port = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"local port","class":"input-mini"}))
    script_dir = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Example:  /bin/aop/"}))
    host_description = forms.CharField(widget=forms.Textarea(attrs={"class":"input-xlarge","placeholder":"Server Description","rows":3}))
    host_pass = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"login pass","class":"input-medium"}))
    host_root_pwd = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"root pass","class":"input-medium"}))
    class Meta:
        model = hosts
        fields = ('host_name','host_user','host_pass','host_w_ip','host_w_port','host_n_ip','host_n_port','host_root_pwd','script_dir','host_description')


class svnform(ModelForm):
    svn_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Svn Name"}))
    svn_user = forms.CharField(widget=forms.TextInput(attrs={"class":"input-medium","placeholder":"Svn user"}))
    svn_pass = forms.CharField(widget=forms.PasswordInput(attrs={"class":"input-medium","placeholder":"Svn pass"}))
    svn_local = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Example:  /var/www/html"}))
    svn_path = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Example:  svn://xx.xx.com/svnproject"}))
    class Meta:
        model = svns
        fields = ('svn_name','svn_user','svn_pass','svn_local','svn_path','host')
        


class scriptform(ModelForm):
    script_description = forms.CharField(widget=forms.Textarea(attrs={"class":"input-xlarge","placeholder":"Script Description","rows":3}))
    class Meta:
        model = scripts
        fields = ('script_name','script_file','script_description')



class hostgroupform(ModelForm):
    class Meta:
        model = hostgroup
        fields = ('host_groupname','host')

class scriptgroupform(ModelForm):
    class Meta:
        model = scriptgroup
        fields = ('script_groupname','script')

class taskform(ModelForm):
    class Meta:
        model = tasks
        fields = ('task_name','script_group','host_group')

class userform(ModelForm):
    class Meta:
        model = User
        fields = ('username','password','email')
if __name__ == "__main__":
    pass
