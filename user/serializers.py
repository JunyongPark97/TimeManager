from rest_framework import serializers

from user.models import EnterTimelog, OutTimelog, OutAtHomeTimelog, EnterAtHomeTimelog, User, UpdateRequest, UserTime


class CurrentOriginDefault(object):
    def set_context(self, serializer_field):
        self.origin = serializer_field.context['origin']

    def __call__(self):
        return EnterTimelog.objects.get(pk=self.origin)

class ObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the `tagged_object` generic relationship.
    """

    def to_representation(self, value):
        """
        Serialize tagged objects to a simple textual representation.
        """
        if isinstance(value, EnterTimelog):
            return value.pk
        elif isinstance(value, OutTimelog):
            return value.pk
        raise Exception('Unexpected type of tagged object')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'grade']


class TimelogSerializer(serializers.ModelSerializer):
    default_user = serializers.HiddenField(source='user', default=serializers.CurrentUserDefault())
    created_at = serializers.DateTimeField()
    text = serializers.CharField(max_length=10)
    user = UserSerializer(read_only=True)


class EnterTimelogSerializer(TimelogSerializer):
    class Meta:
        model = EnterTimelog
        fields = '__all__'
        read_only_field=('keyword')


class OutTimelogSerializer(TimelogSerializer):
    half_day_off = serializers.CharField(required=False)
    breaktime = serializers.IntegerField(required=False)

    class Meta:
        model = OutTimelog
        fields = '__all__'
        read_only_field=('keyword')


class EnterAtHomeTimelogSerializer(TimelogSerializer):

    class Meta:
        model = EnterAtHomeTimelog
        fields = '__all__'
        read_only_field=('keyword')


class OutAtHomeTimelogSerializer(TimelogSerializer):
    breaktime = serializers.IntegerField(required=False)

    class Meta:
        model = OutAtHomeTimelog
        fields = '__all__'
        read_only_field=('keyword')



class CurrentUserDefault(object):
    def set_context(self, serializer_field):
        self.user = serializer_field.context['request'].user

    def __call__(self):
        return self.user



class EnterUpdateRequestSerializer(serializers.ModelSerializer):
    origin = serializers.HiddenField(default=CurrentOriginDefault())
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UpdateRequest
        fields = ('receiver','update','reason','breaktime', 'origin', 'sender')

class EnterUpdateRequestEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = UpdateRequest
        fields = ('status',)
        read_only_fields = ('update',)

class UserTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTime
        fields='__all__'