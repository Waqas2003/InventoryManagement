from django.core.management.base import BaseCommand
from myapp.models import Discounts  
from django.utils import timezone

class Command(BaseCommand):
    help = "Update discount status based on expiry date"

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        
        # Deactivate expired discounts
        expired_discounts = Discounts.objects.filter(
            valid_until__lt=today,
            is_active=True
        )
        expired_count = expired_discounts.update(is_active=False)
        
        # Activate valid discounts (if they were manually deactivated earlier)
        valid_discounts = Discounts.objects.filter(
            valid_until__gte=today,
            is_active=False
        )
        valid_count = valid_discounts.update(is_active=True)
        
        self.stdout.write(
            f"Updated {expired_count} expired Discounts and {valid_count} valid discounts."
        )
        
        
    