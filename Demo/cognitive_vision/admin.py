from django.contrib import admin
from .models import Results


class ResultsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Results, ResultsAdmin)
