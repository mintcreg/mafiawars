from celery import shared_task
from django.utils import timezone
from django.db.models import F
from .models import PlayerProfile

ENERGY_REGEN_RATE = 1 / 300  # 1 energy every 5 minutes (300 seconds)
STAMINA_REGEN_RATE = 1 / 180 # 1 stamina every 3 minutes (180 seconds)

@shared_task
def regenerate_all_player_stats():
    now = timezone.now()
    profiles = PlayerProfile.objects.all()
    for profile in profiles:
        seconds_passed = (now - profile.last_stat_update).total_seconds()
        
        # Regenerate Energy
        energy_to_add = int(seconds_passed * ENERGY_REGEN_RATE)
        if energy_to_add > 0:
            profile.energy = min(profile.max_energy, profile.energy + energy_to_add)

        # Regenerate Stamina
        stamina_to_add = int(seconds_passed * STAMINA_REGEN_RATE)
        if stamina_to_add > 0:
            profile.stamina = min(profile.max_stamina, profile.stamina + stamina_to_add)
            
        profile.last_stat_update = now
        profile.save()

    return f"Updated stats for {profiles.count()} players."