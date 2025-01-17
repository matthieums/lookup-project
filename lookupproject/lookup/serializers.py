from rest_framework import serializers
from .models import CustomUser, School, Course


class UserSerializer(serializers.ModelSerializer):
    schools = serializers.StringRelatedField(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name',
                  'mailaddress']


class CourseSerializer(serializers.ModelSerializer):
    place = serializers.StringRelatedField(many=False)
    teacher = serializers.StringRelatedField(many=False)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'schedule', 'target_audience',
                  'place', 'teacher', 'discipline', 'online']


class SchoolSerializer(serializers.ModelSerializer):

    distance = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = ['name', 'location', 'coordinates', 'contact', 'website', 'distance']

    def get_distance(self, obj):
        return obj.distance.km