from django.core.management.base import BaseCommand
import schedule
import time
from django.utils import timezone
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Runs continuous discount validity checker'

    def handle(self, *args, **options):
        def update_discounts():
            current_time = timezone.now()
            self.stdout.write(f"\n⌚ Checking discounts at {current_time}...")
            try:
                call_command('deactivate_expired_discounts')
                self.stdout.write("✅ Update completed successfully")
            except Exception as e:
                self.stdout.write(f"❌ Error: {str(e)}", style='ERROR')
        
        schedule.every().day.at("01:55").do(update_discounts)
        
        # # For testing, run every 60 seconds instead:
        # schedule.every(60).seconds.do(update_discounts)
        
        self.stdout.write("🔄 Discount scheduler started (Press Ctrl+C to stop)")
        update_discounts() 

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            self.stdout.write("🛑 Scheduler stopped by user")