import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PlayerProfile, Job, EquipmentTemplate, PlayerEquipment

@login_required
def home_view(request):
    player = request.user.profile
    context = {
        'player': player,
        'total_attack': player.get_total_attack(),
        'total_defense': player.get_total_defense(),
    }
    return render(request, 'game/home.html', context)

@login_required
def jobs_view(request):
    player = request.user.profile
    available_jobs = Job.objects.filter(level_requirement__lte=player.level)
    context = {'jobs': available_jobs, 'player': player}
    return render(request, 'game/jobs.html', context)

@login_required
def do_job_view(request, job_id):
    player = request.user.profile
    job = get_object_or_404(Job, id=job_id)

    if player.energy < job.energy_cost:
        messages.error(request, "Not enough energy!")
        return redirect('game:jobs')

    # Execute Job
    player.energy -= job.energy_cost
    cash_earned = random.randint(job.min_cash_reward, job.max_cash_reward)
    player.cash += cash_earned
    player.xp += job.xp_reward

    messages.success(request, f"You completed '{job.name}' and earned ${cash_earned} and {job.xp_reward} XP.")
    
    # Check for level up
    if player.xp >= player.xp_to_next_level:
        player.level_up()
        messages.info(request, "LEVEL UP! You are now Level {player.level}. Your stats have been refilled!")

    player.save()
    return redirect('game:jobs')

@login_required
def equipment_view(request):
    player = request.user.profile
    owned_items = player.playerequipment_set.all()
    market_items = EquipmentTemplate.objects.exclude(id__in=owned_items.values_list('template_id', flat=True))
    context = {
        'owned_items': owned_items,
        'market_items': market_items,
        'player': player
    }
    return render(request, 'game/equipment.html', context)

@login_required
def buy_equipment_view(request, item_id):
    player = request.user.profile
    item_to_buy = get_object_or_404(EquipmentTemplate, id=item_id)

    if player.cash < item_to_buy.cost:
        messages.error(request, "You can't afford this item.")
        return redirect('game:equipment')
    
    player.cash -= item_to_buy.cost
    PlayerEquipment.objects.create(player=player, template=item_to_buy)
    player.save()
    
    messages.success(request, f"You purchased {item_to_buy.name}.")
    return redirect('game:equipment')

@login_required
def fight_view(request):
    player = request.user.profile
    # Find targets in a similar level range, excluding self
    targets = PlayerProfile.objects.filter(
        level__gte=player.level - 5, 
        level__lte=player.level + 5
    ).exclude(user=request.user)
    
    context = {'targets': targets}
    return render(request, 'game/fight.html', context)

@login_required
def attack_view(request, target_id):
    attacker = request.user.profile
    defender = get_object_or_404(PlayerProfile, id=target_id)
    
    if attacker.stamina < 10:
        messages.error(request, "Not enough stamina to attack.")
        return redirect('game:fight')
        
    attacker.stamina -= 10
    
    attacker_power = attacker.get_total_attack() * (1 + random.uniform(-0.1, 0.1))
    defender_power = defender.get_total_defense() * (1 + random.uniform(-0.1, 0.1))
    
    if attacker_power > defender_power:
        cash_stolen = int(defender.cash * 0.1)
        xp_gained = defender.level * 5
        
        attacker.cash += cash_stolen
        attacker.xp += xp_gained
        defender.cash -= cash_stolen
        
        messages.success(request, f"You won! You stole ${cash_stolen} and gained {xp_gained} XP.")
        if attacker.xp >= attacker.xp_to_next_level:
            attacker.level_up()
            messages.info(request, "LEVEL UP!")
    else:
        messages.error(request, "You lost the fight!")

    attacker.save()
    defender.save()
    
    return redirect('game:fight')

@login_required
def family_view(request):
    # This is a stub. A real implementation would handle requests.
    player = request.user.profile
    recruitment_link = request.build_absolute_uri('/') # A real link would have a token
    context = {
        'player': player,
        'recruitment_link': recruitment_link,
    }
    return render(request, 'game/family.html', context)