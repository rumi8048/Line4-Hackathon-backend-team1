from rest_framework import serializers

from accounts.models import Account
from ptn_project.models import CollaboratorMiddleTable, Project
from search.models import GenreTag, Platform, StackTag, UniversityTag
from .models import *

