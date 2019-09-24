from django.db import models
from django.contrib.auth.models import User

from django.core.validators import RegexValidator
from .validators import FileValidator

class Participant(models.Model):
    name = models.CharField(max_length=1024, verbose_name="participant's name")
    email = models.EmailField(verbose_name="participant's email")
    
    phone_validate = RegexValidator(
        regex=r'^\d{10}$', message='Enter your 10 digit phone number without country codes and symbols')
    phone = models.CharField(
        verbose_name="participant's phone", max_length=10, validators=[phone_validate])

    college = models.CharField(verbose_name="participant's institution",max_length=1024, blank=True)

# Create your models here.
class Team(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    participant1 = models.ForeignKey(
        Participant, on_delete=models.DO_NOTHING, related_name='participant1')
    participant2 = models.ForeignKey(
        Participant, on_delete=models.DO_NOTHING, null=True, related_name='participant2')
    participant3 = models.ForeignKey(
        Participant, on_delete=models.DO_NOTHING, null=True, related_name='participant3')
    participant4 = models.ForeignKey(
        Participant, on_delete=models.DO_NOTHING, null=True, related_name='participant4')
    
    
    PROB_PWC = 'PWC'
    PROB_MICRON = 'MIC'
    PROB_QUALCOMM = 'QUA'
    PROB_EMBIBE = 'EMB'

    PROBLEM_STATEMENTS = [
        (PROB_EMBIBE, 'Embibe'),
        (PROB_MICRON, 'Micron'),
        (PROB_QUALCOMM, 'Qualcomm'),
        (PROB_PWC, 'PWC'),
    ]

    problem = models.CharField(max_length=3, choices=PROBLEM_STATEMENTS)

    file_validate = FileValidator(
        max_size=100*1024*1024, content_types=('application/pdf', 'application/vnd.ms-powerpoint', 'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'application/vnd.openxmlformats-officedocument.presentationml.slideshow'))
    
    presentation = models.FileField(validators=[file_validate,], null=True)

    submission = models.URLField(blank=True)

    
