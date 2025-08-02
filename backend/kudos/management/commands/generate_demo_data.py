# kudos/management/commands/generate_demo_data.py
import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from kudos.models import Organization, UserProfile, Kudo

class Command(BaseCommand):
    help = 'Generate demo data for the kudos application'
    
    def handle(self, *args, **options):
        # Clear existing data
        Kudo.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()
        Organization.objects.all().delete()
        
        # Sample organizations
        org_names = [
            'Mitratech Solutions',
            'Tech Innovators Inc',
            'Digital Excellence Corp'
        ]
        
        organizations = []
        for name in org_names:
            org = Organization.objects.create(name=name)
            organizations.append(org)
        
        # Sample user data
        user_data = [
            ('alice_johnson', 'Alice', 'Johnson', 'alice@company.com'),
            ('bob_smith', 'Bob', 'Smith', 'bob@company.com'),
            ('carol_davis', 'Carol', 'Davis', 'carol@company.com'),
            ('david_wilson', 'David', 'Wilson', 'david@company.com'),
            ('eve_brown', 'Eve', 'Brown', 'eve@company.com'),
            ('frank_miller', 'Frank', 'Miller', 'frank@company.com'),
            ('grace_taylor', 'Grace', 'Taylor', 'grace@company.com'),
            ('henry_clark', 'Henry', 'Clark', 'henry@company.com'),
            ('iris_white', 'Iris', 'White', 'iris@company.com'),
            ('jack_harris', 'Jack', 'Harris', 'jack@company.com'),
        ]
        
        users = []
        for username, first_name, last_name, email in user_data:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password='demo123'  # Simple password for demo
            )
            
            # Assign users to organizations (mostly to first org)
            if len(users) < 7:
                org = organizations[0]  # Most users in first org
            else:
                org = random.choice(organizations[1:])  # Some in other orgs
            
            UserProfile.objects.create(user=user, organization=org)
            users.append(user)
        
        # Generate sample kudos messages
        kudo_messages = [
            "Great job on the presentation! Really well organized and clear.",
            "Thanks for helping me debug that tricky issue yesterday.",
            "Your code review comments were super helpful and detailed.",
            "Appreciate you staying late to help meet the deadline.",
            "Love your positive attitude and energy in team meetings!",
            "Your solution to the performance problem was brilliant.",
            "Thanks for mentoring the new team member so patiently.",
            "Your documentation is always so thorough and helpful.",
            "Great idea in today's brainstorming session!",
            "Thanks for covering for me while I was out sick.",
            "Your attention to detail caught that critical bug!",
            "Really appreciate your collaboration on this project.",
            "Your presentation skills have improved so much!",
            "Thanks for sharing that useful tool with the team.",
            "Your quick response helped us avoid a major issue.",
            "Love how you always think about the user experience.",
            "Your testing was incredibly thorough on this release.",
            "Thanks for organizing the team lunch - it was fun!",
            "Your calm demeanor during the crisis was reassuring.",
            "Great job facilitating that difficult conversation.",
        ]
        
        # Generate kudos for the past few weeks
        main_org_users = [u for u in users if UserProfile.objects.get(user=u).organization == organizations[0]]
        
        # Generate kudos for current week (some users have given kudos, some haven't)
        current_week_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        current_week_start = current_week_start - timedelta(days=current_week_start.weekday())
        
        # Some users give kudos this week
        for giver in random.sample(main_org_users, k=random.randint(3, 5)):
            kudos_to_give = random.randint(1, 3)  # Some don't use all their kudos
            receivers = random.sample([u for u in main_org_users if u != giver], k=kudos_to_give)
            
            for i, receiver in enumerate(receivers):
                kudo_time = current_week_start + timedelta(
                    days=random.randint(0, 6),
                    hours=random.randint(9, 17),
                    minutes=random.randint(0, 59)
                )
                
                Kudo.objects.create(
                    giver=giver,
                    receiver=receiver,
                    message=random.choice(kudo_messages),
                    created_at=kudo_time
                )
        
        # Generate kudos for previous weeks (more history)
        for week_offset in range(1, 4):  # Past 3 weeks
            week_start = current_week_start - timedelta(weeks=week_offset)
            
            # More users gave kudos in previous weeks
            for giver in random.sample(main_org_users, k=random.randint(4, 7)):
                kudos_to_give = random.randint(1, 3)
                receivers = random.sample([u for u in main_org_users if u != giver], k=kudos_to_give)
                
                for receiver in receivers:
                    kudo_time = week_start + timedelta(
                        days=random.randint(0, 6),
                        hours=random.randint(9, 17),
                        minutes=random.randint(0, 59)
                    )
                    
                    Kudo.objects.create(
                        giver=giver,
                        receiver=receiver,
                        message=random.choice(kudo_messages),
                        created_at=kudo_time
                    )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created:\n'
                f'- {len(organizations)} organizations\n'
                f'- {len(users)} users\n'
                f'- {Kudo.objects.count()} kudos\n\n'
                f'Sample login credentials:\n'
                f'Username: alice_johnson, Password: demo123\n'
                f'Username: bob_smith, Password: demo123\n'
                f'Username: carol_davis, Password: demo123\n'
                f'(All users have password: demo123)'
            )
        )