from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, phone_num, email, full_name, password):
        if not phone_num or not email or not full_name:
            raise ValueError("This field can not be empty!")
        user = self.model(phone_num=phone_num, email=self.normalize_email(email), full_name=full_name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_num, email, full_name, password):
        user = self.create_user(phone_num, email, full_name, password)
        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user