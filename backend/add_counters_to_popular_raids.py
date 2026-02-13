"""Add counter data to the most popular and meta-relevant raid bosses."""
from models.database import get_db, RaidBoss, RaidCounter, init_db

# Initialize database
init_db()

db = get_db()

# Counter data for popular raid bosses
boss_counters = {
    'Mewtwo': [
        {'pokemon_name': 'Gengar', 'rank': 1, 'fast_move': 'Lick', 'charge_move': 'Shadow Ball', 'pokemon_types': 'Ghost,Poison', 'dps': 25.1, 'tdo': 650, 'is_shadow': True, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Tyranitar', 'rank': 2, 'fast_move': 'Bite', 'charge_move': 'Crunch', 'pokemon_types': 'Rock,Dark', 'dps': 22.8, 'tdo': 720, 'is_shadow': True, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Darkrai', 'rank': 3, 'fast_move': 'Snarl', 'charge_move': 'Shadow Ball', 'pokemon_types': 'Dark', 'dps': 24.2, 'tdo': 680, 'is_shadow': False, 'is_mega': False, 'is_legendary': True},
        {'pokemon_name': 'Chandelure', 'rank': 4, 'fast_move': 'Hex', 'charge_move': 'Shadow Ball', 'pokemon_types': 'Ghost,Fire', 'dps': 23.5, 'tdo': 620, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Weavile', 'rank': 5, 'fast_move': 'Snarl', 'charge_move': 'Avalanche', 'pokemon_types': 'Dark,Ice', 'dps': 22.1, 'tdo': 580, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
    ],
    'Giratina': [
        {'pokemon_name': 'Rayquaza', 'rank': 1, 'fast_move': 'Dragon Tail', 'charge_move': 'Outrage', 'pokemon_types': 'Dragon,Flying', 'dps': 23.5, 'tdo': 680, 'is_shadow': False, 'is_mega': True, 'is_legendary': True},
        {'pokemon_name': 'Garchomp', 'rank': 2, 'fast_move': 'Dragon Tail', 'charge_move': 'Outrage', 'pokemon_types': 'Dragon,Ground', 'dps': 22.2, 'tdo': 650, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Gengar', 'rank': 3, 'fast_move': 'Lick', 'charge_move': 'Shadow Ball', 'pokemon_types': 'Ghost,Poison', 'dps': 21.5, 'tdo': 600, 'is_shadow': True, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Dragonite', 'rank': 4, 'fast_move': 'Dragon Tail', 'charge_move': 'Draco Meteor', 'pokemon_types': 'Dragon,Flying', 'dps': 21.2, 'tdo': 630, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Salamence', 'rank': 5, 'fast_move': 'Dragon Tail', 'charge_move': 'Outrage', 'pokemon_types': 'Dragon,Flying', 'dps': 20.8, 'tdo': 620, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
    ],
    'Groudon': [
        {'pokemon_name': 'Kyogre', 'rank': 1, 'fast_move': 'Waterfall', 'charge_move': 'Surf', 'pokemon_types': 'Water', 'dps': 24.2, 'tdo': 710, 'is_shadow': False, 'is_mega': False, 'is_legendary': True},
        {'pokemon_name': 'Gyarados', 'rank': 2, 'fast_move': 'Waterfall', 'charge_move': 'Hydro Pump', 'pokemon_types': 'Water,Flying', 'dps': 21.5, 'tdo': 640, 'is_shadow': False, 'is_mega': True, 'is_legendary': False},
        {'pokemon_name': 'Swampert', 'rank': 3, 'fast_move': 'Water Gun', 'charge_move': 'Hydro Cannon', 'pokemon_types': 'Water,Ground', 'dps': 20.8, 'tdo': 650, 'is_shadow': True, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Roserade', 'rank': 4, 'fast_move': 'Razor Leaf', 'charge_move': 'Solar Beam', 'pokemon_types': 'Grass,Poison', 'dps': 19.8, 'tdo': 570, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Venusaur', 'rank': 5, 'fast_move': 'Vine Whip', 'charge_move': 'Frenzy Plant', 'pokemon_types': 'Grass,Poison', 'dps': 19.2, 'tdo': 600, 'is_shadow': False, 'is_mega': True, 'is_legendary': False},
    ],
    'Kyogre': [
        {'pokemon_name': 'Zekrom', 'rank': 1, 'fast_move': 'Charge Beam', 'charge_move': 'Wild Charge', 'pokemon_types': 'Dragon,Electric', 'dps': 23.1, 'tdo': 680, 'is_shadow': False, 'is_mega': False, 'is_legendary': True},
        {'pokemon_name': 'Raikou', 'rank': 2, 'fast_move': 'Thunder Shock', 'charge_move': 'Wild Charge', 'pokemon_types': 'Electric', 'dps': 22.5, 'tdo': 650, 'is_shadow': True, 'is_mega': False, 'is_legendary': True},
        {'pokemon_name': 'Magnezone', 'rank': 3, 'fast_move': 'Spark', 'charge_move': 'Wild Charge', 'pokemon_types': 'Electric,Steel', 'dps': 21.8, 'tdo': 630, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Electivire', 'rank': 4, 'fast_move': 'Thunder Shock', 'charge_move': 'Wild Charge', 'pokemon_types': 'Electric', 'dps': 20.5, 'tdo': 590, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Roserade', 'rank': 5, 'fast_move': 'Razor Leaf', 'charge_move': 'Grass Knot', 'pokemon_types': 'Grass,Poison', 'dps': 19.8, 'tdo': 570, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
    ],
    'Rayquaza': [
        {'pokemon_name': 'Mamoswine', 'rank': 1, 'fast_move': 'Powder Snow', 'charge_move': 'Avalanche', 'pokemon_types': 'Ice,Ground', 'dps': 25.5, 'tdo': 700, 'is_shadow': True, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Weavile', 'rank': 2, 'fast_move': 'Ice Shard', 'charge_move': 'Avalanche', 'pokemon_types': 'Dark,Ice', 'dps': 24.2, 'tdo': 640, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Glaceon', 'rank': 3, 'fast_move': 'Frost Breath', 'charge_move': 'Avalanche', 'pokemon_types': 'Ice', 'dps': 22.5, 'tdo': 610, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Galarian Darmanitan', 'rank': 4, 'fast_move': 'Ice Fang', 'charge_move': 'Avalanche', 'pokemon_types': 'Ice', 'dps': 26.8, 'tdo': 550, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Rampardos', 'rank': 5, 'fast_move': 'Smack Down', 'charge_move': 'Rock Slide', 'pokemon_types': 'Rock', 'dps': 21.5, 'tdo': 580, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
    ],
    'Reshiram': [
        {'pokemon_name': 'Rayquaza', 'rank': 1, 'fast_move': 'Dragon Tail', 'charge_move': 'Outrage', 'pokemon_types': 'Dragon,Flying', 'dps': 23.5, 'tdo': 670, 'is_shadow': False, 'is_mega': False, 'is_legendary': True},
        {'pokemon_name': 'Salamence', 'rank': 2, 'fast_move': 'Dragon Tail', 'charge_move': 'Draco Meteor', 'pokemon_types': 'Dragon,Flying', 'dps': 21.8, 'tdo': 640, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Rhyperior', 'rank': 3, 'fast_move': 'Smack Down', 'charge_move': 'Rock Wrecker', 'pokemon_types': 'Ground,Rock', 'dps': 21.5, 'tdo': 690, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Dragonite', 'rank': 4, 'fast_move': 'Dragon Tail', 'charge_move': 'Draco Meteor', 'pokemon_types': 'Dragon,Flying', 'dps': 21.0, 'tdo': 650, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Garchomp', 'rank': 5, 'fast_move': 'Dragon Tail', 'charge_move': 'Outrage', 'pokemon_types': 'Dragon,Ground', 'dps': 20.8, 'tdo': 640, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
    ],
    'Zekrom': [
        {'pokemon_name': 'Garchomp', 'rank': 1, 'fast_move': 'Mud Shot', 'charge_move': 'Earth Power', 'pokemon_types': 'Dragon,Ground', 'dps': 23.5, 'tdo': 670, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Rayquaza', 'rank': 2, 'fast_move': 'Dragon Tail', 'charge_move': 'Outrage', 'pokemon_types': 'Dragon,Flying', 'dps': 23.1, 'tdo': 660, 'is_shadow': False, 'is_mega': False, 'is_legendary': True},
        {'pokemon_name': 'Dragonite', 'rank': 3, 'fast_move': 'Dragon Tail', 'charge_move': 'Draco Meteor', 'pokemon_types': 'Dragon,Flying', 'dps': 21.2, 'tdo': 630, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Rhyperior', 'rank': 4, 'fast_move': 'Mud Slap', 'charge_move': 'Earthquake', 'pokemon_types': 'Ground,Rock', 'dps': 20.8, 'tdo': 680, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Mamoswine', 'rank': 5, 'fast_move': 'Mud Slap', 'charge_move': 'Bulldoze', 'pokemon_types': 'Ice,Ground', 'dps': 19.5, 'tdo': 650, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
    ],
    'Darkrai': [
        {'pokemon_name': 'Machamp', 'rank': 1, 'fast_move': 'Counter', 'charge_move': 'Dynamic Punch', 'pokemon_types': 'Fighting', 'dps': 22.5, 'tdo': 650, 'is_shadow': True, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Lucario', 'rank': 2, 'fast_move': 'Counter', 'charge_move': 'Aura Sphere', 'pokemon_types': 'Fighting,Steel', 'dps': 23.1, 'tdo': 620, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Conkeldurr', 'rank': 3, 'fast_move': 'Counter', 'charge_move': 'Dynamic Punch', 'pokemon_types': 'Fighting', 'dps': 21.8, 'tdo': 680, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Togekiss', 'rank': 4, 'fast_move': 'Charm', 'charge_move': 'Dazzling Gleam', 'pokemon_types': 'Fairy,Flying', 'dps': 19.5, 'tdo': 590, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Gardevoir', 'rank': 5, 'fast_move': 'Charm', 'charge_move': 'Dazzling Gleam', 'pokemon_types': 'Psychic,Fairy', 'dps': 18.8, 'tdo': 570, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
    ],
    'Lugia': [
        {'pokemon_name': 'Rampardos', 'rank': 1, 'fast_move': 'Smack Down', 'charge_move': 'Rock Slide', 'pokemon_types': 'Rock', 'dps': 24.5, 'tdo': 580, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Rhyperior', 'rank': 2, 'fast_move': 'Smack Down', 'charge_move': 'Rock Wrecker', 'pokemon_types': 'Ground,Rock', 'dps': 22.8, 'tdo': 690, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Tyranitar', 'rank': 3, 'fast_move': 'Smack Down', 'charge_move': 'Stone Edge', 'pokemon_types': 'Rock,Dark', 'dps': 22.1, 'tdo': 710, 'is_shadow': True, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Gengar', 'rank': 4, 'fast_move': 'Lick', 'charge_move': 'Shadow Ball', 'pokemon_types': 'Ghost,Poison', 'dps': 21.5, 'tdo': 600, 'is_shadow': True, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Magnezone', 'rank': 5, 'fast_move': 'Spark', 'charge_move': 'Wild Charge', 'pokemon_types': 'Electric,Steel', 'dps': 19.8, 'tdo': 610, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
    ],
    'Ho-Oh': [
        {'pokemon_name': 'Rampardos', 'rank': 1, 'fast_move': 'Smack Down', 'charge_move': 'Rock Slide', 'pokemon_types': 'Rock', 'dps': 26.2, 'tdo': 600, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Rhyperior', 'rank': 2, 'fast_move': 'Smack Down', 'charge_move': 'Rock Wrecker', 'pokemon_types': 'Ground,Rock', 'dps': 23.5, 'tdo': 710, 'is_shadow': True, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Tyranitar', 'rank': 3, 'fast_move': 'Smack Down', 'charge_move': 'Stone Edge', 'pokemon_types': 'Rock,Dark', 'dps': 22.8, 'tdo': 720, 'is_shadow': True, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Terrakion', 'rank': 4, 'fast_move': 'Smack Down', 'charge_move': 'Rock Slide', 'pokemon_types': 'Rock,Fighting', 'dps': 22.1, 'tdo': 680, 'is_shadow': False, 'is_mega': False, 'is_legendary': True},
        {'pokemon_name': 'Gigalith', 'rank': 5, 'fast_move': 'Smack Down', 'charge_move': 'Rock Slide', 'pokemon_types': 'Rock', 'dps': 20.5, 'tdo': 650, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
    ],
    'Landorus': [
        {'pokemon_name': 'Mamoswine', 'rank': 1, 'fast_move': 'Powder Snow', 'charge_move': 'Avalanche', 'pokemon_types': 'Ice,Ground', 'dps': 25.8, 'tdo': 710, 'is_shadow': True, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Weavile', 'rank': 2, 'fast_move': 'Ice Shard', 'charge_move': 'Avalanche', 'pokemon_types': 'Dark,Ice', 'dps': 24.5, 'tdo': 650, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Glaceon', 'rank': 3, 'fast_move': 'Frost Breath', 'charge_move': 'Avalanche', 'pokemon_types': 'Ice', 'dps': 23.2, 'tdo': 620, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Galarian Darmanitan', 'rank': 4, 'fast_move': 'Ice Fang', 'charge_move': 'Avalanche', 'pokemon_types': 'Ice', 'dps': 27.1, 'tdo': 560, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Kyogre', 'rank': 5, 'fast_move': 'Waterfall', 'charge_move': 'Surf', 'pokemon_types': 'Water', 'dps': 21.5, 'tdo': 690, 'is_shadow': False, 'is_mega': False, 'is_legendary': True},
    ],
    'Xerneas': [
        {'pokemon_name': 'Metagross', 'rank': 1, 'fast_move': 'Bullet Punch', 'charge_move': 'Meteor Mash', 'pokemon_types': 'Steel,Psychic', 'dps': 22.8, 'tdo': 710, 'is_shadow': True, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Gengar', 'rank': 2, 'fast_move': 'Lick', 'charge_move': 'Sludge Bomb', 'pokemon_types': 'Ghost,Poison', 'dps': 21.5, 'tdo': 620, 'is_shadow': True, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Roserade', 'rank': 3, 'fast_move': 'Poison Jab', 'charge_move': 'Sludge Bomb', 'pokemon_types': 'Grass,Poison', 'dps': 20.2, 'tdo': 590, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Dialga', 'rank': 4, 'fast_move': 'Metal Claw', 'charge_move': 'Iron Head', 'pokemon_types': 'Steel,Dragon', 'dps': 19.8, 'tdo': 730, 'is_shadow': False, 'is_mega': False, 'is_legendary': True},
        {'pokemon_name': 'Excadrill', 'rank': 5, 'fast_move': 'Metal Claw', 'charge_move': 'Iron Head', 'pokemon_types': 'Ground,Steel', 'dps': 19.2, 'tdo': 650, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
    ],
    'Yveltal': [
        {'pokemon_name': 'Rampardos', 'rank': 1, 'fast_move': 'Smack Down', 'charge_move': 'Rock Slide', 'pokemon_types': 'Rock', 'dps': 25.8, 'tdo': 590, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Rhyperior', 'rank': 2, 'fast_move': 'Smack Down', 'charge_move': 'Rock Wrecker', 'pokemon_types': 'Ground,Rock', 'dps': 23.5, 'tdo': 700, 'is_shadow': True, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Mamoswine', 'rank': 3, 'fast_move': 'Powder Snow', 'charge_move': 'Avalanche', 'pokemon_types': 'Ice,Ground', 'dps': 22.8, 'tdo': 680, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Togekiss', 'rank': 4, 'fast_move': 'Charm', 'charge_move': 'Dazzling Gleam', 'pokemon_types': 'Fairy,Flying', 'dps': 21.2, 'tdo': 620, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Gardevoir', 'rank': 5, 'fast_move': 'Charm', 'charge_move': 'Dazzling Gleam', 'pokemon_types': 'Psychic,Fairy', 'dps': 20.5, 'tdo': 600, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
    ],
    'Terrakion': [
        {'pokemon_name': 'Mewtwo', 'rank': 1, 'fast_move': 'Confusion', 'charge_move': 'Psystrike', 'pokemon_types': 'Psychic', 'dps': 24.5, 'tdo': 700, 'is_shadow': True, 'is_mega': False, 'is_legendary': True},
        {'pokemon_name': 'Kyogre', 'rank': 2, 'fast_move': 'Waterfall', 'charge_move': 'Surf', 'pokemon_types': 'Water', 'dps': 22.8, 'tdo': 720, 'is_shadow': False, 'is_mega': False, 'is_legendary': True},
        {'pokemon_name': 'Swampert', 'rank': 3, 'fast_move': 'Water Gun', 'charge_move': 'Hydro Cannon', 'pokemon_types': 'Water,Ground', 'dps': 21.5, 'tdo': 680, 'is_shadow': True, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Garchomp', 'rank': 4, 'fast_move': 'Mud Shot', 'charge_move': 'Earth Power', 'pokemon_types': 'Dragon,Ground', 'dps': 20.8, 'tdo': 650, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
        {'pokemon_name': 'Togekiss', 'rank': 5, 'fast_move': 'Charm', 'charge_move': 'Ancient Power', 'pokemon_types': 'Fairy,Flying', 'dps': 19.5, 'tdo': 620, 'is_shadow': False, 'is_mega': False, 'is_legendary': False},
    ],
}

print("Adding counter data to popular raid bosses...")
print(f"Processing {len(boss_counters)} raid bosses with counter data\n")

updated_count = 0
not_found = []

for boss_name, counters in boss_counters.items():
    # Find the raid boss
    raid_boss = db.query(RaidBoss).filter_by(name=boss_name).first()

    if not raid_boss:
        not_found.append(boss_name)
        print(f"  ⚠️  {boss_name} - Not found in database, skipping...")
        continue

    print(f"  ✓ {boss_name} - Adding {len(counters)} counters...")

    # Delete existing counters for this boss
    db.query(RaidCounter).filter_by(raid_boss_id=raid_boss.id).delete()

    # Add new counters
    for counter_data in counters:
        counter_data['raid_boss_id'] = raid_boss.id
        counter = RaidCounter(**counter_data)
        db.add(counter)

    updated_count += 1

db.commit()
db.close()

print(f"\n{'='*60}")
print(f"✓ Successfully added counters to {updated_count} raid bosses!")
if not_found:
    print(f"⚠️  Could not find {len(not_found)} bosses: {', '.join(not_found)}")
print(f"{'='*60}")
print("\nBosses with counter data:")
for boss_name in boss_counters.keys():
    if boss_name not in not_found:
        print(f"  • {boss_name}")
print("\nYou can now view counters for these bosses at:")
print("  → http://localhost:3000/raids")
