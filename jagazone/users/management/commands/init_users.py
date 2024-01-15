from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
import random

from jagazone.users.models import Gender, UsersProfile


User = get_user_model()


class Command(BaseCommand):
    help = "Initial users"

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        now = timezone.now()
        created_users = []
        created_users_profiles = []
        
        for index in range(30):
            user = User(
                name=f"user_{index}",
                email=f"user_{index}@gmail.com",
                username=f"user_{index} user_{index}",
            )
            created_users.append(user)
            user_profile = UsersProfile(
                user=user,
                birthdate=now - relativedelta(year=18+index),
                role=random.choice((
                    UsersProfile.GUEST,
                    UsersProfile.ADMIN,
                    UsersProfile.N_CONFIRMED,
                    UsersProfile.CONFIRMED,
                )),
                gender=random.choice(Gender.names),
                phone_number=f'+38000000000{index}',
            )
            created_users_profiles.append(user_profile)
            
        User.objects.bulk_create(created_users)
        UsersProfile.objects.bulk_create(created_users_profiles)
          
        self.stdout.write(
            self.style.SUCCESS('Successfully')
        )