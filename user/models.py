from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser

from insta.models import BaseTimeModel
from django.db import models


# 사용자 매니저 클래스
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        이메일을 사용하는 기본 사용자 생성.
        """
        if not email:
            raise ValueError('이메일이 없으면 회원가입을 못해요.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # 비밀번호 암호화
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        슈퍼 사용자 생성
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


# Create your models here.
class Users(AbstractBaseUser, BaseTimeModel):
	email = models.EmailField(max_length=255, unique=True)
	name = models.CharField(max_length=255)
	birthday = models.DateField()
	tel = models.CharField(max_length=11, unique=True)

	profile_pic = models.TextField(
		null=True,
		blank=True
		)

	sns = models.JSONField(
		default=dict,
		null=True,
		blank=True
		)

	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name']

	objects = CustomUserManager()

	def __str__(self):
		return self.email