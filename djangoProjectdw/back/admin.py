from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

class EvenAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('station', 'department', 'gpa_number', 'sau_modifications', 'plan', 'complete', 'isnotnecessary', 'text', 'done', 'category', 'user',  'total_complete')
    list_filter = ('category', 'user')

    def totalcomplete(self, obj):
        return obj.category.summa

    totalcomplete.shortdescription = 'Сумма выполненных работ'


class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name',)


class VnedrenieAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('lpu', 'department', 'gpa_number', 'ip', 'type_equipment', 'ip_number', 'done', 'reason', 'user')
    list_filter = ('lpu', 'user')


class ExecutionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('filial', 'station', 'kc', 'gpa_number', 'gpa_modification', 'sau_modification', 'mpn', 'date', 'defects_count', 'fio', 'event', 'position')


class ControlsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('lpu', 'station', 'department', 'gpa_number', 'gpa_typle', 'sau_modifications', 'type_equioment', 'n_ip', 'ip', 'complete', 'text', 'user')


class ReisterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ()

class PredicionsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('type_refuses', 'type_gpa', 'type_say', 'type_equioment', 'element', 'maybe_reasons', 'meropriation',)


class NotEvendmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('station', 'department', 'gpa_number', 'sau_modifications', 'complete', 'cvartal1', 'cvartal2', 'cvartal3',
                    'cvartal4', 'cvartal5', 'cvartal6', 'cvartal7', 'cvartal8', 'cvartal9', 'cvartal10', 'cvartal11', 'cvartal12', 'category', 'user')



admin.site.register(ChatResponse)
# Register your models here.
admin.site.register(Plan)
admin.site.register(Execution, ExecutionAdmin)
admin.site.register(Filial)
admin.site.register(Station)
admin.site.register(KcNumber)
admin.site.register(Event)
admin.site.register(Mpn)
admin.site.register(GpaNumber)
admin.site.register(Plans)
admin.site.register(Kc)
admin.site.register(GpaModification)
admin.site.register(SauModification)
admin.site.register(Position)
admin.site.register(Even, EvenAdmin)
admin.site.register(Notes)
admin.site.register(IsNotNecessary)
admin.site.register(Marks)
admin.site.register(Complete)
admin.site.register(Narabotka)
admin.site.register(Otkaz)
admin.site.register(Vnerdenie, VnedrenieAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Document3)
admin.site.register(Category1)
admin.site.register(Control, ControlsAdmin)
admin.site.register(Document5)
admin.site.register(Document1)
admin.site.register(Predicions, PredicionsAdmin)
admin.site.register(Category5)
admin.site.register(Cvartals)
admin.site.register(Document6)
admin.site.register(NotEven, NotEvendmin)
admin.site.register(Category4)

admin.site.register(DialogueStep)