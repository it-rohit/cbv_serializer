from rest_framework import serializers
from  . models import Student
from django.core.exceptions import ValidationError 

class StudentSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = Student
        fields=['id','name','score']

    # def validate(self, attrs):
    #     breakpoint()
    #     return super().validate(attrs)
    
    # def validate(self, attrs):
    #     breakpoint()
    #     return super().validate(attrs)
    def validate_score(self,score):
        
        if score >=50:
            raise ValidationError({"error":"score should be below 50"})
        return score