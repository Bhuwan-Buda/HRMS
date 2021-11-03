from django.contrib import admin
from .models import User, Education, Skill, Experience

# Register your models here.

admin.site.register([User, Education, Skill, Experience])



