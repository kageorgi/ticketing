from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from daraja.models import Movie, Show

class Command(BaseCommand):
    help = "Seed sample movies and shows"

    def handle(self, *args, **kwargs):
        Movie.objects.all().delete()
        Show.objects.all().delete()

        m1 = Movie.objects.create(name="The First Adventure", description="An epic adventure.", price_per_seat=250)
        m2 = Movie.objects.create(name="Romance in Nairobi", description="Feelings & sunsets.", price_per_seat=300)

        now = timezone.now()
        Show.objects.create(movie=m1, show_time=now + timedelta(days=1, hours=18), total_seats=50)
        Show.objects.create(movie=m1, show_time=now + timedelta(days=2, hours=18), total_seats=50)
        Show.objects.create(movie=m2, show_time=now + timedelta(days=1, hours=20), total_seats=40)

        self.stdout.write(self.style.SUCCESS("Sample movies & shows created"))
