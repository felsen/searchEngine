from django.contrib import admin
from aue.models import Enquiry

class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('goal','url','ip_address','created_date')
    search_fields = ['ip_address','url','goal']
    list_filter = ('ip_address','url','goal')
admin.site.register(Enquiry,EnquiryAdmin)

