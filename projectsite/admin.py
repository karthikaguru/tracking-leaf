from django.contrib import admin
from .models import  Project, Stage, Expense



class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'client',
        'budget',
        'status'
    )
    search_fields = (
        'name',
        'client__name',
      
    )
    list_filter = (
        'client',
        'status'
    )


class StageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'project',
        'due_date',
        'start_date',
        'end_date',
        'progress',
        'stage_type',
        'status'
    )
    search_fields = (
        'name',
        'project__name',
        'stage_type'
    )
    list_filter = (
        'project',
        'stage_type',
        'status'
    )


class ExpenseAdmin(admin.ModelAdmin):
    list_display = (
    
        'project',
        'amount_spent',
        'date'
    )
    search_fields = (
    
        'project__name',
    )
    list_filter = (
        'project',
        'date',
    )


admin.site.register(Project, ProjectAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Expense, ExpenseAdmin)