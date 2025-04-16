from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Transaction
from django.urls import path
from django.shortcuts import redirect
from django.utils.html import format_html
from django.contrib import messages

class CustomUserAdmin(UserAdmin):
    # Define the fields to be displayed in the admin list view
    list_display = ('username', 'first_name' ,'email', 'phone_number', 'is_active', 'is_staff', 'date_joined')
    
    # Define the fields to be used in the admin detail view
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Financial Info', {'fields': ('wallet',)}),
        ('Personal Info', {'fields': ('phone_number', 'first_name', 'last_name','profile_picture', 'address_line_1', 'address_line_2', 'city', 'state', 'country', 'zip_code')}),
        ('Location Info', {'fields': ('region_name', 'lat', 'lon', 'timezone', 'isp')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    
    # Define the fields to be used in the admin add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    
    # Enable search functionality
    search_fields = ('username', 'email', 'phone_number', 'city', 'state', 'country')
    
    # Enable filtering
    list_filter = ('is_active', 'is_staff', 'date_joined', 'country', 'state')
    
    # Set the ordering of the list view
    ordering = ('-date_joined',)

# Register the CustomUser model with the CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'transaction_type', 'amount',
        'balance_after', 'status', 'created_at', 'process_button'
    )
    list_filter = ('transaction_type', 'status', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('balance_after', 'created_at', 'updated_at', 'status')

    fieldsets = (
        (None, {
            'fields': (
                'user', 'transaction_type', 'amount',
                'status', 'balance_after', 'description', 'metadata'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    actions = ['process_selected_transactions']

    @admin.action(description="Process selected transactions")
    def process_selected_transactions(self, request, queryset):
        processed = 0
        for transaction in queryset:
            if transaction.status == 'pending':
                transaction.process_transaction()
                processed += 1
        self.message_user(request, f"{processed} transaction(s) processed.")

    def process_button(self, obj):
        if obj.status == 'pending':
            return format_html(
                '<a class="paper-actions__button btn btn-info ml-1 border-0" href="{}">Process</a>',
                f'process/{obj.pk}'
            )
        return '—'
    process_button.short_description = 'Action'
    process_button.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('process/<int:pk>', self.admin_site.admin_view(self.process_single_transaction), name='process-transaction'),
        ]
        return custom_urls + urls

    def process_single_transaction(self, request, pk):
        transaction = Transaction.objects.get(pk=pk)
        if transaction.status == 'pending':
            transaction.process_transaction()
            self.message_user(request, f"Transaction {pk} processed.")
        else:
            self.message_user(request, f"Transaction {pk} is already {transaction.status}.", level=messages.WARNING)
        return redirect('..')
