"""Add more raid bosses to the database."""
from models.database import get_db, RaidBoss, RaidCounter, init_db
from datetime import datetime

# Initialize database
init_db()

db = get_db()

# Additional raid bosses
additional_raids = [
    {
        'name': 'Giratina',
        'tier': '5',
        'types': 'Ghost,Dragon',
        'weaknesses': 'Ice,Ghost,Dragon,Dark,Fairy',
        'cp_min': 2018,
        'cp_max': 2105,
        'cp_boosted_min': 2523,
        'cp_boosted_max': 2631,
        'is_active': True,
        'counters': [
            {'pokemon_name': 'Rayquaza', 'rank': 1, 'fast_move': 'Dragon Tail', 'charge_move': 'Outrage', 'pokemon_types': 'Dragon,Flying', 'dps': 22.5, 'tdo': 660, 'is_shadow': False, 'is_mega': False, 'is_legendary': True},
            {'pokemon_name': 'Garchomp', 'rank': 2, 'fast_move': 'Dragon Tail', 'charge_move': 'Outrage', 'pokemon_types': 'Dragon,Ground', 'dps': 21.2, 'tdo': 630, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
            {'pokemon_name': 'Gengar', 'rank': 3, 'fast_move': 'Lick', 'charge_move': 'Shadow Ball', 'pokemon_types': 'Ghost,Poison', 'dps': 20.5, 'tdo': 580, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        ]
    },
    {
        'name': 'Groudon',
        'tier': '5',
        'types': 'Ground',
        'weaknesses': 'Water,Grass,Ice',
        'cp_min': 2260,
        'cp_max': 2351,
        'is_active': True,
        'counters': [
            {'pokemon_name': 'Kyogre', 'rank': 1, 'fast_move': 'Waterfall', 'charge_move': 'Surf', 'pokemon_types': 'Water', 'dps': 24.2, 'tdo': 710, 'is_shadow': False, 'is_mega': False, 'is_legendary': True},
            {'pokemon_name': 'Gyarados', 'rank': 2, 'fast_move': 'Waterfall', 'charge_move': 'Hydro Pump', 'pokemon_types': 'Water,Flying', 'dps': 20.5, 'tdo': 620, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
            {'pokemon_name': 'Roserade', 'rank': 3, 'fast_move': 'Razor Leaf', 'charge_move': 'Solar Beam', 'pokemon_types': 'Grass,Poison', 'dps': 19.8, 'tdo': 570, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        ]
    },
    {
        'name': 'Kyogre',
        'tier': '5',
        'types': 'Water',
        'weaknesses': 'Grass,Electric',
        'cp_min': 2260,
        'cp_max': 2351,
        'is_active': True,
        'counters': [
            {'pokemon_name': 'Zekrom', 'rank': 1, 'fast_move': 'Charge Beam', 'charge_move': 'Wild Charge', 'pokemon_types': 'Dragon,Electric', 'dps': 23.1, 'tdo': 680, 'is_shadow': False, 'is_mega': False, 'is_legendary': True},
            {'pokemon_name': 'Raikou', 'rank': 2, 'fast_move': 'Thunder Shock', 'charge_move': 'Wild Charge', 'pokemon_types': 'Electric', 'dps': 22.5, 'tdo': 650, 'is_shadow': False, 'is_mega': False, 'is_legendary': True},
            {'pokemon_name': 'Magnezone', 'rank': 3, 'fast_move': 'Spark', 'charge_move': 'Wild Charge', 'pokemon_types': 'Electric,Steel', 'dps': 20.8, 'tdo': 610, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        ]
    },
    {
        'name': 'Rayquaza',
        'tier': '5',
        'types': 'Dragon,Flying',
        'weaknesses': 'Ice,Rock,Dragon,Fairy',
        'cp_min': 2191,
        'cp_max': 2283,
        'is_active': True,
        'counters': [
            {'pokemon_name': 'Mamoswine', 'rank': 1, 'fast_move': 'Powder Snow', 'charge_move': 'Avalanche', 'pokemon_types': 'Ice,Ground', 'dps': 24.5, 'tdo': 680, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
            {'pokemon_name': 'Weavile', 'rank': 2, 'fast_move': 'Ice Shard', 'charge_move': 'Avalanche', 'pokemon_types': 'Dark,Ice', 'dps': 23.2, 'tdo': 620, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
            {'pokemon_name': 'Glaceon', 'rank': 3, 'fast_move': 'Frost Breath', 'charge_move': 'Avalanche', 'pokemon_types': 'Ice', 'dps': 21.5, 'tdo': 590, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        ]
    },
    {
        'name': 'Mewtwo',
        'tier': '5',
        'types': 'Psychic',
        'weaknesses': 'Bug,Ghost,Dark',
        'cp_min': 2294,
        'cp_max': 2387,
        'is_active': True,
        'counters': [
            {'pokemon_name': 'Gengar', 'rank': 1, 'fast_move': 'Lick', 'charge_move': 'Shadow Ball', 'pokemon_types': 'Ghost,Poison', 'dps': 25.1, 'tdo': 650, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
            {'pokemon_name': 'Tyranitar', 'rank': 2, 'fast_move': 'Bite', 'charge_move': 'Crunch', 'pokemon_types': 'Rock,Dark', 'dps': 22.8, 'tdo': 720, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
            {'pokemon_name': 'Darkrai', 'rank': 3, 'fast_move': 'Snarl', 'charge_move': 'Shadow Ball', 'pokemon_types': 'Dark', 'dps': 24.2, 'tdo': 680, 'is_shadow': False, 'is_mega': False, 'is_legendary': True},
        ]
    },
    {
        'name': 'Reshiram',
        'tier': '5',
        'types': 'Dragon,Fire',
        'weaknesses': 'Ground,Rock,Dragon',
        'cp_min': 2217,
        'cp_max': 2307,
        'is_active': True,
        'counters': [
            {'pokemon_name': 'Rayquaza', 'rank': 1, 'fast_move': 'Dragon Tail', 'charge_move': 'Outrage', 'pokemon_types': 'Dragon,Flying', 'dps': 23.5, 'tdo': 670, 'is_shadow': False, 'is_mega': False, 'is_legendary': True},
            {'pokemon_name': 'Salamence', 'rank': 2, 'fast_move': 'Dragon Tail', 'charge_move': 'Draco Meteor', 'pokemon_types': 'Dragon,Flying', 'dps': 21.8, 'tdo': 640, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
            {'pokemon_name': 'Rhyperior', 'rank': 3, 'fast_move': 'Smack Down', 'charge_move': 'Rock Wrecker', 'pokemon_types': 'Ground,Rock', 'dps': 20.5, 'tdo': 680, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        ]
    },
    {
        'name': 'Zekrom',
        'tier': '5',
        'types': 'Dragon,Electric',
        'weaknesses': 'Ice,Ground,Dragon,Fairy',
        'cp_min': 2217,
        'cp_max': 2307,
        'is_active': True,
        'counters': [
            {'pokemon_name': 'Garchomp', 'rank': 1, 'fast_move': 'Mud Shot', 'charge_move': 'Earth Power', 'pokemon_types': 'Dragon,Ground', 'dps': 22.5, 'tdo': 650, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
            {'pokemon_name': 'Rayquaza', 'rank': 2, 'fast_move': 'Dragon Tail', 'charge_move': 'Outrage', 'pokemon_types': 'Dragon,Flying', 'dps': 23.1, 'tdo': 660, 'is_shadow': False, 'is_mega': False, 'is_legendary': True},
            {'pokemon_name': 'Dragonite', 'rank': 3, 'fast_move': 'Dragon Tail', 'charge_move': 'Draco Meteor', 'pokemon_types': 'Dragon,Flying', 'dps': 21.2, 'tdo': 630, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        ]
    },
    {
        'name': 'Articuno',
        'tier': '5',
        'types': 'Ice,Flying',
        'weaknesses': 'Rock,Steel,Fire,Electric',
        'cp_min': 1743,
        'cp_max': 1823,
        'is_active': False,
        'counters': [
            {'pokemon_name': 'Rampardos', 'rank': 1, 'fast_move': 'Smack Down', 'charge_move': 'Rock Slide', 'pokemon_types': 'Rock', 'dps': 24.8, 'tdo': 580, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
            {'pokemon_name': 'Rhyperior', 'rank': 2, 'fast_move': 'Smack Down', 'charge_move': 'Rock Wrecker', 'pokemon_types': 'Ground,Rock', 'dps': 22.5, 'tdo': 670, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
            {'pokemon_name': 'Tyranitar', 'rank': 3, 'fast_move': 'Smack Down', 'charge_move': 'Stone Edge', 'pokemon_types': 'Rock,Dark', 'dps': 21.8, 'tdo': 690, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        ]
    },
]

print("Adding more raid bosses to the database...")

for raid in additional_raids:
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

print(f"\n✓ Successfully added {len(additional_raids)} more raid bosses!")
print("Total raid bosses in database now:")
print("  - Dialga, Palkia, Regigigas, Mega Sableye (original)")
print("  - Giratina, Groudon, Kyogre, Rayquaza, Mewtwo, Reshiram, Zekrom, Articuno (new)")
print("\nYou can now search for any of these raid bosses at http://localhost:3000/raids")
