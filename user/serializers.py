from rest_framework import serializers

from user.models import EnterTimelog, OutTimelog, OutAtHomeTimelog, EnterAtHomeTimelog, User, UpdateRequest


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


class OutTimelogSerializer(TimelogSerializer):
    half_day_off = serializers.CharField(required=False)
    breaktime = serializers.IntegerField(required=False)

    class Meta:
        model = OutTimelog
        fields = '__all__'


class EnterAtHomeTimelogSerializer(TimelogSerializer):

    class Meta:
        model = EnterAtHomeTimelog
        fields = '__all__'


class OutAtHomeTimelogSerializer(TimelogSerializer):
    breaktime = serializers.IntegerField(required=False)

    class Meta:
        model = OutAtHomeTimelog
        fields = '__all__'


class UpdateRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = UpdateRequest
        fields = ('receiver','update','reason','breaktime')

