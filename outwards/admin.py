from django.contrib import admin
from .forms import OutwardModelForm
from .models import Outward


class OutwardModelAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Date Range', {
            'fields': ('employee', 'reference', 'subject', 'instrument', 'query', 'query_type', 'tax_type',
                       'if_other_tax_type', 'country', 'document', 'tax_period',
                       ),
            'classes': ('predefined',)
        }),
        (None, {
            'fields': (('start_tax_period', 'end_tax_period'),),
            'classes': ('board',)
        })
    )

    form = OutwardModelForm

    class Media:
        js = ('static/js/base.js',)


admin.site.register(Outward, OutwardModelAdmin)


