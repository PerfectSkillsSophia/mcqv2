from django.db import models

class allAssessment(models.Model):
    assId = models.AutoField(primary_key=True)
    assessmentName = models.CharField(max_length=255,null=True)
    assessmentDes = models.CharField(max_length=1000,null=True)
    def __str__(self):
        return self.assessmentName

class Question(models.Model):
    quostion= models.CharField(max_length=255,null=True)
    ops1=models.CharField(max_length=255,null=True)
    ops2=models.CharField(max_length=255,null=True)
    ops3=models.CharField(max_length=255,null=True)
    ops4=models.CharField(max_length=255,null=True)
    assessment = models.ForeignKey(allAssessment, on_delete=models.CASCADE)
    def __str__(self):
        return self.quostion
    
