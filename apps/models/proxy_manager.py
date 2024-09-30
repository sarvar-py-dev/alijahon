from django.contrib.auth.models import UserManager

from apps.models import User


class DriverUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=User.Type.DRIVER)


class OperatorUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=User.Type.OPERATOR)


class ManagerUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=User.Type.MANAGER)


class AdminUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=User.Type.ADMIN)


class UserUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=User.Type.USER)
