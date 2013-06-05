#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from aop.models import *

admin.site.register(hosts)
admin.site.register(svns)
admin.site.register(hostgroup)

admin.site.register(scripts)
admin.site.register(scriptgroup)
admin.site.register(tasks)
admin.site.register(users)