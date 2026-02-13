"""Populate database with sample raid data for testing."""
from models.database import get_db, RaidBoss, RaidCounter, init_db
from datetime import datetime

# Initialize database
init_db()

db = get_db()

# Sample raid bosses based on current Pokemon GO raids
sample_raids = [
    {
        'name': 'Dialga',
        'tier': '5',
        'types': 'Steel,Dragon',
        'weaknesses': 'Fighting,Ground',
        'cp_min': 2217,
        'cp_max': 2307,
        'cp_boosted_min': 2771,
        'cp_boosted_max': 2884,
        'is_active': True,
        'counters': [
            {'pokemon_name': 'Terrakion', 'rank': 1, 'fast_move': 'Double Kick', 'charge_move': 'Sacred Sword', 'pokemon_types': 'Rock,Fighting', 'dps': 21.5, 'tdo': 650, 'is_shadow': False, 'is_mega': False, 'is_legendary': True},
            {'pokemon_name': 'Groudon', 'rank': 2, 'fast_move': 'Mud Shot', 'charge_move': 'Earthquake', 'pokemon_types': 'Ground', 'dps': 20.8, 'tdo': 620, 'is_shadow': False, 'is_mega': False, 'is_legendary': True},
            {'pokemon_name': 'Garchomp', 'rank': 3, 'fast_move': 'Mud Shot', 'charge_move': 'Earth Power', 'pokemon_types': 'Dragon,Ground', 'dps': 19.9, 'tdo': 595, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
            {'pokemon_name': 'Excadrill', 'rank': 4, 'fast_move': 'Mud-Slap', 'charge_move': 'Drill Run', 'pokemon_types': 'Ground,Steel', 'dps': 19.2, 'tdo': 560, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
            {'pokemon_name': 'Machamp', 'rank': 5, 'fast_move': 'Counter', 'charge_move': 'Dynamic Punch', 'pokemon_types': 'Fighting', 'dps': 18.5, 'tdo': 540, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        ]
    },
    {
        'name': 'Palkia',
        'tier': '5',
        'types': 'Water,Dragon',
        'weaknesses': 'Dragon,Fairy',
        'cp_min': 2190,
        'cp_max': 2280,
        'cp_boosted_min': 2737,
        'cp_boosted_max': 2850,
        'is_active': True,
        'counters': [
            {'pokemon_name': 'Rayquaza', 'rank': 1, 'fast_move': 'Dragon Tail', 'charge_move': 'Outrage', 'pokemon_types': 'Dragon,Flying', 'dps': 23.2, 'tdo': 680, 'is_shadow': False, 'is_mega': False, 'is_legendary': True},
            {'pokemon_name': 'Dialga', 'rank': 2, 'fast_move': 'Dragon Breath', 'charge_move': 'Draco Meteor', 'pokemon_types': 'Steel,Dragon', 'dps': 22.5, 'tdo': 720, 'is_shadow': False, 'is_mega': False, 'is_legendary': True},
            {'pokemon_name': 'Garchomp', 'rank': 3, 'fast_move': 'Dragon Tail', 'charge_move': 'Outrage', 'pokemon_types': 'Dragon,Ground', 'dps': 21.8, 'tdo': 650, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
            {'pokemon_name': 'Dragonite', 'rank': 4, 'fast_move': 'Dragon Tail', 'charge_move': 'Draco Meteor', 'pokemon_types': 'Dragon,Flying', 'dps': 20.5, 'tdo': 620, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
            {'pokemon_name': 'Salamence', 'rank': 5, 'fast_move': 'Dragon Tail', 'charge_move': 'Outrage', 'pokemon_types': 'Dragon,Flying', 'dps': 20.2, 'tdo': 600, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        ]
    },
    {
        'name': 'Mega Sableye',
        'tier': 'Mega',
        'types': 'Dark,Ghost',
        'weaknesses': 'Fairy',
        'cp_min': 1668,
        'cp_max': 1745,
        'is_active': True,
        'counters': [
            {'pokemon_name': 'Togekiss', 'rank': 1, 'fast_move': 'Charm', 'charge_move': 'Dazzling Gleam', 'pokemon_types': 'Fairy,Flying', 'dps': 18.5, 'tdo': 580, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
            {'pokemon_name': 'Gardevoir', 'rank': 2, 'fast_move': 'Charm', 'charge_move': 'Dazzling Gleam', 'pokemon_types': 'Psychic,Fairy', 'dps': 17.8, 'tdo': 550, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
            {'pokemon_name': 'Granbull', 'rank': 3, 'fast_move': 'Charm', 'charge_move': 'Play Rough', 'pokemon_types': 'Fairy', 'dps': 16.5, 'tdo': 520, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        ]
    },
    {
        'name': 'Regigigas',
        'tier': '5',
        'types': 'Normal',
        'weaknesses': 'Fighting',
        'cp_min': 2171,
        'cp_max': 2261,
        'is_active': True,
        'counters': [
            {'pokemon_name': 'Lucario', 'rank': 1, 'fast_move': 'Counter', 'charge_move': 'Aura Sphere', 'pokemon_types': 'Fighting,Steel', 'dps': 22.1, 'tdo': 620, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
            {'pokemon_name': 'Machamp', 'rank': 2, 'fast_move': 'Counter', 'charge_move': 'Dynamic Punch', 'pokemon_types': 'Fighting', 'dps': 21.3, 'tdo': 595, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
            {'pokemon_name': 'Conkeldurr', 'rank': 3, 'fast_move': 'Counter', 'charge_move': 'Dynamic Punch', 'pokemon_types': 'Fighting', 'dps': 20.8, 'tdo': 610, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        ]
    }
]

print("Populating sample raid data...")

for raid in sample_raids:
    # Extract counters
    counters_data = raid.pop('counters')

    # Check if boss exists
    existing = db.query(RaidBoss).filter_by(name=raid['name']).first()

    if existing:
        print(f"  Updating {raid['name']}...")
        for key, value in raid.items():
            setattr(existing, key, value)
        existing.last_updated = datetime.utcnow()
        raid_boss = existing
    else:
        print(f"  Adding {raid['name']}...")
        raid_boss = RaidBoss(**raid)
        db.add(raid_boss)
        db.flush()

    # Delete old counters
    db.query(RaidCounter).filter_by(raid_boss_id=raid_boss.id).delete()

    # Add new counters
    for counter in counters_data:
        counter['raid_boss_id'] = raid_boss.id
        db.add(RaidCounter(**counter))

db.commit()
db.close()

print(f"\n✓ Successfully populated {len(sample_raids)} raid bosses with counters!")
print("You can now view them at http://localhost:3000/raids")
