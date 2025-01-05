from rest_framework import serializers
from .models import Teacher, School, Course


class TeacherSerializer(serializers.ModelSerializer):
    schools = serializers.StringRelatedField(many=True)

    class Meta:
        model = Teacher
        fields = ['name', 'last_name', 'schools', 'disciplines',
                  'mailaddress', 'phone_number']


class CourseSerializer(serializers.ModelSerializer):
    place = serializers.StringRelatedField(many=False)
    teacher = serializers.StringRelatedField(many=False)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'schedule', 'target_audience',
                  'place', 'teacher', 'discipline', 'online']


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = ['name', 'location', 'contact', 'website']


# Additional improvements
# from rest_framework import serializers
# from .models import School

# class SchoolSerializer(serializers.ModelSerializer):
#     distance = serializers.SerializerMethodField()

#     class Meta:
#         model = School
#         fields = ['id', 'name', 'location', 'distance']

#     def get_distance(self, obj):
#         return round(obj.distance.km, 2)