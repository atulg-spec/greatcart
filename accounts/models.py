from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import transaction as db_transaction
from django.db.models import F
from django.db.models import Sum
import uuid

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.PositiveIntegerField(blank=True, null=True)
    wallet = models.IntegerField(default=0)
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    region_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    timezone = models.CharField(max_length=100, blank=True, null=True)
    isp = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
    
    def get_balance(self):
        """Returns the current wallet balance"""
        return self.wallet
    
    def get_transaction_history(self):
        """Returns all transactions for this user"""
        return self.transactions.all()
    
    def get_total_credited(self):
        """Returns total amount credited to wallet"""
        return self.transactions.filter(
            transaction_type='credit',
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
    
    def get_total_debited(self):
        """Returns total amount debited from wallet"""
        return self.transactions.filter(
            transaction_type='debit',
            status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
    
    @db_transaction.atomic
    def credit_wallet(self, amount, description=None, metadata=None):
        """Credits the user's wallet"""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        reference = f"CR-{uuid.uuid4().hex[:10].upper()}"
        
        # Create transaction record
        transaction = self.transactions.create(
            transaction_type='credit',
            amount=amount,
            balance_after=self.wallet + amount,
            reference=reference,
            status='completed',
            description=description,
            metadata=metadata or {}
        )
        
        # Update wallet balance
        self.wallet = F('wallet') + amount
        self.save(update_fields=['wallet'])
        
        # Refresh from db to get updated wallet value
        self.refresh_from_db()
        
        return transaction
    
    @db_transaction.atomic
    def debit_wallet(self, amount, description=None, metadata=None):
        """Debits the user's wallet if sufficient balance exists"""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        if self.wallet < amount:
            raise ValueError("Insufficient balance")
        
        reference = f"DR-{uuid.uuid4().hex[:10].upper()}"
        
        # Create transaction record
        transaction = self.transactions.create(
            transaction_type='debit',
            amount=amount,
            balance_after=self.wallet - amount,
            reference=reference,
            status='completed',
            description=description,
            metadata=metadata or {}
        )
        
        # Update wallet balance
        self.wallet = F('wallet') - amount
        self.save(update_fields=['wallet'])
        
        # Refresh from db to get updated wallet value
        self.refresh_from_db()
        
        return transaction
    
    def can_debit(self, amount):
        """Check if user has sufficient balance for a debit"""
        return self.wallet >= amount


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('reversed', 'Reversed'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    balance_after = models.IntegerField()
    # The reference field has been removed.
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    description = models.TextField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            # Removed the index on 'reference'
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount}"
    
    def process_transaction(self):
        """
        Processes this transaction:
        
        - For a debit: Checks if the user's wallet has enough funds.
          If not, marks the transaction as failed.
        - For a credit: Adds the amount to the user's wallet.
        
        After processing, updates the transaction status and the user's wallet balance.
        """
        # Assume that the CustomUser model has a 'wallet' attribute representing the current balance.
        wallet = self.user.wallet
        
        if self.transaction_type == 'debit':
            if wallet >= self.amount:
                # Deduct the debit amount from the wallet
                wallet -= self.amount
                self.status = 'completed'
            else:
                # Insufficient funds: mark as failed
                self.status = 'failed'
        elif self.transaction_type == 'credit':
            # Add the credit amount to the wallet
            wallet += self.amount
            self.status = 'completed'
        
        # Update the user's wallet balance and the transaction's balance_after field
        self.user.wallet = wallet
        self.balance_after = wallet
        
        # Save both the user and the transaction
        self.user.save()
        self.save()

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            current_balance = self.user.wallet
            if self.transaction_type == 'credit':
                self.balance_after = current_balance + self.amount
            elif self.transaction_type == 'debit':
                if current_balance >= self.amount:
                    self.balance_after = current_balance - self.amount
                else:
                    self.balance_after = current_balance  # No change, since transaction will be failed
                    self.status = 'failed'
        super().save(*args, **kwargs)

