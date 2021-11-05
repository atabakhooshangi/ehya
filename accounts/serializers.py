from django.utils.translation import ugettext as _
from rest_framework import serializers
from django.contrib.auth.views import get_user_model
from rest_framework.generics import get_object_or_404

from accounts.models import Role

User = get_user_model()


class RegisterLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=225)

    def is_user(self):
        phone_number = self.data.get('phone_number')
        user = User.objects.filter(phone_number=phone_number)
        if user.exists():
            return user.first()
        return False
    # def validate(self, attrs):
    #     phone_number = attrs.get('phone_number')
    #     user = User.objects.filter(phone_number=phone_number)
    #     if user.exists() and user.is_active:
    #         raise serializers.ValidationError(_('این شماره قبلا ثبت نام انجام داده است.'))
    #
    #     return attrs
    #
    # def save(self, **kwargs):
    #     user = User.objects.create(phone_number=self.validated_data['phone_number'])
    #     return user


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


class VerificationCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    code = serializers.IntegerField(max_value=9999)

    def validate(self, attrs):
        user = get_object_or_404(User, phone_number=attrs.get('phone_number'))
        if user.verify_code == attrs.get('code'):
            if not user.is_active: user.is_active = True
            # user.verify_code = None
            user.save()
            return user.tokens
        raise serializers.ValidationError({'code': _('کد وارد شده اشتباه است.')})


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    profile_done = serializers.SerializerMethodField(read_only=True)
    has_points = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['phone_number', 'role', 'first_name', 'last_name', 'province', 'city', 'birthday', 'gender', 'degree',
                  'field_of_study', 'job', 'points', 'profile_done', 'has_points']

    def get_role(self, obj):
        return obj.role.name

    def get_profile_done(self, obj):
        return obj.profile_done

    def get_has_points(self, obj):
        return obj.check_point_status_for_ticket


class ReferralSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13)

    def validate(self, attrs):
        try:
            user = User.objects.get(phone_number=attrs.get('phone_number'), is_active=True)

        except:
            raise serializers.ValidationError({'user': _('شماره تلفن وارد شده اشتباه است.')})

        else:
            return user
