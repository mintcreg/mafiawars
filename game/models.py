from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum

class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    
    # Core Stats
    level = models.PositiveIntegerField(default=1)
    xp = models.BigIntegerField(default=0)
    xp_to_next_level = models.BigIntegerField(default=100)
    cash = models.BigIntegerField(default=1000)
    
    # Resource Pools
    health = models.PositiveIntegerField(default=100)
    max_health = models.PositiveIntegerField(default=100)
    energy = models.PositiveIntegerField(default=50)
    max_energy = models.PositiveIntegerField(default=50)
    stamina = models.PositiveIntegerField(default=20)
    max_stamina = models.PositiveIntegerField(default=20)
    
    # Skill Points
    skill_points = models.PositiveIntegerField(default=0)
    
    # Combat Stats (Base)
    base_attack = models.PositiveIntegerField(default=5)
    base_defense = models.PositiveIntegerField(default=5)
    
    # Family (Mafia)
    family = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='family_members')
    
    # Timestamps for regeneration
    last_stat_update = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

    def level_up(self):
        self.level += 1
        self.xp = 0
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5) # Increase XP requirement
        self.skill_points += 5
        self.health = self.max_health # Full heal on level up
        self.energy = self.max_energy
        self.stamina = self.max_stamina
        self.save()

    def get_total_attack(self):
        # Base + Equipment + Top Family Bonus
        equipment_attack = self.playerequipment_set.aggregate(Sum('template__attack_boost'))['template__attack_boost__sum'] or 0
        
        # This is a simplified family bonus for demonstration. A real one would be more complex.
        family_bonus = 0
        if self.family.exists():
            # For simplicity, we'll just add a flat bonus per family member
            family_bonus = self.family.count() * 2 
            
        return self.base_attack + equipment_attack + family_bonus

    def get_total_defense(self):
        equipment_defense = self.playerequipment_set.aggregate(Sum('template__defense_boost'))['template__defense_boost__sum'] or 0
        family_bonus = self.family.count() * 2
        return self.base_defense + equipment_defense + family_bonus

# Signal to create a PlayerProfile whenever a new User is created
@receiver(post_save, sender=User)
def create_player_profile(sender, instance, created, **kwargs):
    if created:
        PlayerProfile.objects.create(user=instance)

class EquipmentTemplate(models.Model):
    name = models.CharField(max_length=100)
    attack_boost = models.IntegerField(default=0)
    defense_boost = models.IntegerField(default=0)
    cost = models.BigIntegerField()
    
    def __str__(self):
        return self.name

class PlayerEquipment(models.Model):
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE)
    template = models.ForeignKey(EquipmentTemplate, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('player', 'template')

class Job(models.Model):
    name = models.CharField(max_length=100)
    energy_cost = models.IntegerField()
    min_cash_reward = models.IntegerField()
    max_cash_reward = models.IntegerField()
    xp_reward = models.IntegerField()
    level_requirement = models.IntegerField(default=1)

    def __str__(self):
        return self.name