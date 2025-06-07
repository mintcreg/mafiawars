from django.contrib import admin
from .models import PlayerProfile, EquipmentTemplate, PlayerEquipment, Job

@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'cash', 'energy', 'stamina')

@admin.register(EquipmentTemplate)
class EquipmentTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'attack_boost', 'defense_boost', 'cost')

@admin.register(PlayerEquipment)
class PlayerEquipmentAdmin(admin.ModelAdmin):
    list_display = ('player', 'template')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('name', 'energy_cost', 'xp_reward', 'level_requirement')