from django.contrib import admin
from .models import Branch, BDM, Broker

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email', 'created_at')
    search_fields = ('name', 'address', 'email')
    list_filter = ('created_at',)

@admin.register(BDM)
class BDMAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'branch', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('branch', 'created_at')
    raw_id_fields = ('user', 'created_by')

@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'email', 'phone', 'branch', 'created_at')
    search_fields = ('name', 'company', 'email', 'phone')
    list_filter = ('branch', 'created_at')
    raw_id_fields = ('user', 'created_by')
    filter_horizontal = ('bdms',)
