"""

Assumptions (not necessarily realistic):

- a school does not need to have classrooms 
- a school can have multiple classrooms
- if a school is removed, its classrooms are too

- a classroom must have an associated school 
- a classroom can only belong to a single school
- a classroom can have multiple students
- if a classroom is removed, its students remain 

- a student does not need to have a classroom 
- a student can only belong to a single classroom

"""
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.forms import ModelForm, ModelChoiceField
from django.db import models
from django.utils.translation import ugettext as _

@python_2_unicode_compatible
class School(models.Model):
    name = models.CharField(verbose_name="School name",
        max_length=255,
    )

    # could be split into address1, address2, city, region/state, country, etc.
    address = models.CharField(_('address'), max_length=254, blank=True)
    
    phone = models.CharField(_('phone'), max_length=30, blank=True)
    
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Classroom(models.Model):
    # just a name for now 
    name = models.CharField(verbose_name="Classroom name",
        max_length=255,
    )

    # assumes that classrooms seize to exist if their school seizes to exist
    school = models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        related_name="children",
    ) 

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Student(models.Model):

    """
    Name validation is a lost cause. 
    The only non-discrimnatory scheme seems to be a single field allowing all characters.
    See: https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/
    """
    name = models.CharField(_('name'), max_length=254, blank=True)

    # could be split into address1, address2, city, region/state, country, etc.
    address = models.CharField(_('address'), max_length=254, blank=True)

    phone = models.CharField(_('phone'), max_length=30, blank=True)

    date_of_birth = models.DateField()

    # email max_length=254 (RFC 5321)
    email = models.EmailField(_('email address'), max_length=254, blank=True)

    classroom = models.ForeignKey(
        'Classroom',
        # allow students without classrooms in DB and admin panel
        null=True,
        blank=True,
        # don't cascade - leave affected students intact if classroom is deleted
        on_delete=models.SET_NULL,
        related_name="children"
    )  

    def __str__(self):
        return self.name


# Used by the Vis.js network graph view
class SchoolSelect(ModelForm):
    schools = ModelChoiceField(queryset=School.objects.all(),
    
        )
    class Meta:
        model = School
        exclude = ["name"]

