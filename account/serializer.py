from rest_framework import serializers
from account.models import Account, upload_path


class AccountSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    gender = serializers.CharField(max_length=10)
    age = serializers.IntegerField(default=0)
    email = serializers.EmailField(default=None)
    create_date = serializers.DateTimeField(read_only=True)
    icon = serializers.ImageField(default=None)
    user = serializers.PrimaryKeyRelatedField(many=False, required=False,read_only=True)
    result = serializers.CharField(max_length=200)
    url = serializers.URLField()

    def create(self, validated_data):
        return Account.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.gender = validated_data.get('gender',instance.gender)
        instance.age = validated_data.get('age',instance.age)
        instance.email = validated_data.get('email',instance.email)
        instance.icon = validated_data.get('icon',instance.icon)
        instance.result = validated_data.get('result',instance.result)
        instance.url = validated_data.get('url',instance.url)
        instance.save()
        return instance
# class AccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Account
#         fields = ('username','gender','age','email','create_date','icon','user')
#
#     def create(self, validated_data):
#         return Account.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.username = validated_data.get('username', instance.username)
#         instance.gender = validated_data.get('gender',instance.gender)
#         instance.age = validated_data.get('age',instance.age)
#         instance.email = validated_data.get('email',instance.email)
#         instance.icon = validated_data.get('icon',instance.icon)
#         instance.save()
#         return instance