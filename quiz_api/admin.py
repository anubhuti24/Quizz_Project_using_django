from django.contrib import admin

from quiz_api.models import Quiz


# Register your models here.
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['question', 'start_date', 'end_date']
    list_filter = ['start_date', 'end_date']
    search_fields = ['question']

    # Customize the form fieldsets if needed
    fieldsets = (
        (None, {'fields': ('question', 'options', 'right_answer')}),
        ('Date and Time', {'fields': ('start_date', 'end_date')}),
    )
