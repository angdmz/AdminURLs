from django.contrib.auth.models import User

from logic.models import Manager

all_user_queryset = User.objects
all_managers_queryset = Manager.objects
