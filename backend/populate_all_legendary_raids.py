"""Populate database with comprehensive legendary raid bosses from Pokebattler."""
from models.database import get_db, RaidBoss, RaidCounter, init_db
from datetime import datetime

# Initialize database
init_db()

db = get_db()

# Comprehensive list of Tier 5 legendary raid bosses
legendary_raids = [
    # Current/Recent Legendaries
    {'name': 'Dialga', 'tier': '5', 'types': 'Steel,Dragon', 'weaknesses': 'Fighting,Ground', 'is_active': True},
    {'name': 'Palkia', 'tier': '5', 'types': 'Water,Dragon', 'weaknesses': 'Dragon,Fairy', 'is_active': True},
    {'name': 'Dialga Origin', 'tier': '5', 'types': 'Steel,Dragon', 'weaknesses': 'Fighting,Ground', 'is_active': False},
    {'name': 'Palkia Origin', 'tier': '5', 'types': 'Water,Dragon', 'weaknesses': 'Dragon,Fairy', 'is_active': False},

    # Legendary Birds
    {'name': 'Articuno', 'tier': '5', 'types': 'Ice,Flying', 'weaknesses': 'Rock,Steel,Fire,Electric', 'is_active': False},
    {'name': 'Zapdos', 'tier': '5', 'types': 'Electric,Flying', 'weaknesses': 'Ice,Rock', 'is_active': False},
    {'name': 'Moltres', 'tier': '5', 'types': 'Fire,Flying', 'weaknesses': 'Rock,Water,Electric', 'is_active': False},

    # Legendary Beasts
    {'name': 'Raikou', 'tier': '5', 'types': 'Electric', 'weaknesses': 'Ground', 'is_active': False},
    {'name': 'Entei', 'tier': '5', 'types': 'Fire', 'weaknesses': 'Water,Ground,Rock', 'is_active': False},
    {'name': 'Suicune', 'tier': '5', 'types': 'Water', 'weaknesses': 'Grass,Electric', 'is_active': False},

    # Weather Trio
    {'name': 'Groudon', 'tier': '5', 'types': 'Ground', 'weaknesses': 'Water,Grass,Ice', 'is_active': False},
    {'name': 'Kyogre', 'tier': '5', 'types': 'Water', 'weaknesses': 'Grass,Electric', 'is_active': False},
    {'name': 'Rayquaza', 'tier': '5', 'types': 'Dragon,Flying', 'weaknesses': 'Ice,Rock,Dragon,Fairy', 'is_active': False},
    {'name': 'Primal Groudon', 'tier': '5', 'types': 'Ground,Fire', 'weaknesses': 'Water,Ground', 'is_active': False},
    {'name': 'Primal Kyogre', 'tier': '5', 'types': 'Water', 'weaknesses': 'Grass,Electric', 'is_active': False},

    # Tower Duo
    {'name': 'Lugia', 'tier': '5', 'types': 'Psychic,Flying', 'weaknesses': 'Rock,Ghost,Electric,Ice,Dark', 'is_active': False},
    {'name': 'Ho-Oh', 'tier': '5', 'types': 'Fire,Flying', 'weaknesses': 'Rock,Water,Electric', 'is_active': False},
    {'name': 'Shadow Lugia', 'tier': '5', 'types': 'Psychic,Flying', 'weaknesses': 'Rock,Ghost,Electric,Ice,Dark', 'is_active': False},
    {'name': 'Shadow Ho-Oh', 'tier': '5', 'types': 'Fire,Flying', 'weaknesses': 'Rock,Water,Electric', 'is_active': False},

    # Eon Duo
    {'name': 'Latios', 'tier': '5', 'types': 'Dragon,Psychic', 'weaknesses': 'Ice,Bug,Ghost,Dragon,Dark,Fairy', 'is_active': False},
    {'name': 'Latias', 'tier': '5', 'types': 'Dragon,Psychic', 'weaknesses': 'Ice,Bug,Ghost,Dragon,Dark,Fairy', 'is_active': False},

    # Regi Trio
    {'name': 'Regirock', 'tier': '5', 'types': 'Rock', 'weaknesses': 'Water,Grass,Fighting,Ground,Steel', 'is_active': False},
    {'name': 'Regice', 'tier': '5', 'types': 'Ice', 'weaknesses': 'Fire,Fighting,Rock,Steel', 'is_active': False},
    {'name': 'Registeel', 'tier': '5', 'types': 'Steel', 'weaknesses': 'Fire,Fighting,Ground', 'is_active': False},
    {'name': 'Regigigas', 'tier': '5', 'types': 'Normal', 'weaknesses': 'Fighting', 'is_active': True},

    # Lake Trio
    {'name': 'Uxie', 'tier': '5', 'types': 'Psychic', 'weaknesses': 'Bug,Ghost,Dark', 'is_active': False},
    {'name': 'Mesprit', 'tier': '5', 'types': 'Psychic', 'weaknesses': 'Bug,Ghost,Dark', 'is_active': False},
    {'name': 'Azelf', 'tier': '5', 'types': 'Psychic', 'weaknesses': 'Bug,Ghost,Dark', 'is_active': False},

    # Creation Trio
    {'name': 'Giratina', 'tier': '5', 'types': 'Ghost,Dragon', 'weaknesses': 'Ice,Ghost,Dragon,Dark,Fairy', 'is_active': False},
    {'name': 'Giratina Origin', 'tier': '5', 'types': 'Ghost,Dragon', 'weaknesses': 'Ice,Ghost,Dragon,Dark,Fairy', 'is_active': False},

    # Legendary Dragons
    {'name': 'Reshiram', 'tier': '5', 'types': 'Dragon,Fire', 'weaknesses': 'Ground,Rock,Dragon', 'is_active': False},
    {'name': 'Zekrom', 'tier': '5', 'types': 'Dragon,Electric', 'weaknesses': 'Ice,Ground,Dragon,Fairy', 'is_active': False},
    {'name': 'Kyurem', 'tier': '5', 'types': 'Dragon,Ice', 'weaknesses': 'Fighting,Rock,Dragon,Steel,Fairy', 'is_active': False},
    {'name': 'Black Kyurem', 'tier': '5', 'types': 'Dragon,Ice', 'weaknesses': 'Fighting,Rock,Dragon,Steel,Fairy', 'is_active': False},
    {'name': 'White Kyurem', 'tier': '5', 'types': 'Dragon,Ice', 'weaknesses': 'Fighting,Rock,Dragon,Steel,Fairy', 'is_active': False},

    # Swords of Justice
    {'name': 'Cobalion', 'tier': '5', 'types': 'Steel,Fighting', 'weaknesses': 'Fire,Fighting,Ground', 'is_active': False},
    {'name': 'Terrakion', 'tier': '5', 'types': 'Rock,Fighting', 'weaknesses': 'Water,Grass,Fighting,Ground,Psychic,Steel,Fairy', 'is_active': False},
    {'name': 'Virizion', 'tier': '5', 'types': 'Grass,Fighting', 'weaknesses': 'Fire,Ice,Poison,Flying,Psychic,Fairy', 'is_active': False},
    {'name': 'Keldeo', 'tier': '5', 'types': 'Water,Fighting', 'weaknesses': 'Grass,Electric,Flying,Psychic,Fairy', 'is_active': False},

    # Forces of Nature
    {'name': 'Tornadus', 'tier': '5', 'types': 'Flying', 'weaknesses': 'Rock,Electric,Ice', 'is_active': False},
    {'name': 'Thundurus', 'tier': '5', 'types': 'Electric,Flying', 'weaknesses': 'Ice,Rock', 'is_active': False},
    {'name': 'Landorus', 'tier': '5', 'types': 'Ground,Flying', 'weaknesses': 'Ice,Water', 'is_active': False},
    {'name': 'Enamorus', 'tier': '5', 'types': 'Fairy,Flying', 'weaknesses': 'Rock,Steel,Electric,Ice,Poison', 'is_active': False},

    # Kalos Legendaries
    {'name': 'Xerneas', 'tier': '5', 'types': 'Fairy', 'weaknesses': 'Poison,Steel', 'is_active': False},
    {'name': 'Yveltal', 'tier': '5', 'types': 'Dark,Flying', 'weaknesses': 'Rock,Electric,Ice,Fairy', 'is_active': False},
    {'name': 'Zygarde', 'tier': '5', 'types': 'Dragon,Ground', 'weaknesses': 'Ice,Dragon,Fairy', 'is_active': False},

    # Mythicals (Special Research/Raids)
    {'name': 'Mewtwo', 'tier': '5', 'types': 'Psychic', 'weaknesses': 'Bug,Ghost,Dark', 'is_active': False},
    {'name': 'Mew', 'tier': '5', 'types': 'Psychic', 'weaknesses': 'Bug,Ghost,Dark', 'is_active': False},
    {'name': 'Celebi', 'tier': '5', 'types': 'Psychic,Grass', 'weaknesses': 'Fire,Ice,Poison,Flying,Bug,Ghost,Dark', 'is_active': False},
    {'name': 'Jirachi', 'tier': '5', 'types': 'Steel,Psychic', 'weaknesses': 'Fire,Ground,Ghost,Dark', 'is_active': False},
    {'name': 'Deoxys', 'tier': '5', 'types': 'Psychic', 'weaknesses': 'Bug,Ghost,Dark', 'is_active': False},
    {'name': 'Darkrai', 'tier': '5', 'types': 'Dark', 'weaknesses': 'Fighting,Bug,Fairy', 'is_active': False},
    {'name': 'Genesect', 'tier': '5', 'types': 'Bug,Steel', 'weaknesses': 'Fire', 'is_active': False},

    # Alola Legendaries
    {'name': 'Tapu Koko', 'tier': '5', 'types': 'Electric,Fairy', 'weaknesses': 'Ground,Poison', 'is_active': False},
    {'name': 'Tapu Lele', 'tier': '5', 'types': 'Psychic,Fairy', 'weaknesses': 'Poison,Ghost,Steel', 'is_active': False},
    {'name': 'Tapu Bulu', 'tier': '5', 'types': 'Grass,Fairy', 'weaknesses': 'Fire,Ice,Poison,Flying,Steel', 'is_active': False},
    {'name': 'Tapu Fini', 'tier': '5', 'types': 'Water,Fairy', 'weaknesses': 'Grass,Electric,Poison', 'is_active': False},
    {'name': 'Solgaleo', 'tier': '5', 'types': 'Psychic,Steel', 'weaknesses': 'Fire,Ground,Ghost,Dark', 'is_active': False},
    {'name': 'Lunala', 'tier': '5', 'types': 'Psychic,Ghost', 'weaknesses': 'Ghost,Dark', 'is_active': False},
    {'name': 'Necrozma', 'tier': '5', 'types': 'Psychic', 'weaknesses': 'Bug,Ghost,Dark', 'is_active': False},

    # Ultra Beasts
    {'name': 'Nihilego', 'tier': '5', 'types': 'Rock,Poison', 'weaknesses': 'Water,Ground,Psychic,Steel', 'is_active': False},
    {'name': 'Buzzwole', 'tier': '5', 'types': 'Bug,Fighting', 'weaknesses': 'Fire,Flying,Psychic,Fairy', 'is_active': False},
    {'name': 'Pheromosa', 'tier': '5', 'types': 'Bug,Fighting', 'weaknesses': 'Fire,Flying,Psychic,Fairy', 'is_active': False},
    {'name': 'Xurkitree', 'tier': '5', 'types': 'Electric', 'weaknesses': 'Ground', 'is_active': False},
    {'name': 'Celesteela', 'tier': '5', 'types': 'Steel,Flying', 'weaknesses': 'Fire,Electric', 'is_active': False},
    {'name': 'Kartana', 'tier': '5', 'types': 'Grass,Steel', 'weaknesses': 'Fire,Fighting', 'is_active': False},
    {'name': 'Guzzlord', 'tier': '5', 'types': 'Dark,Dragon', 'weaknesses': 'Fighting,Bug,Ice,Dragon,Fairy', 'is_active': False},
]

print(f"Populating database with {len(legendary_raids)} legendary raid bosses...")

added_count = 0
updated_count = 0

for raid in legendary_raids:
    # Check if boss exists
    existing = db.query(RaidBoss).filter_by(name=raid['name']).first()

    if existing:
        print(f"  ↻ Updating {raid['name']}...")
        for key, value in raid.items():
            setattr(existing, key, value)
        existing.last_updated = datetime.utcnow()
        updated_count += 1
    else:
        print(f"  + Adding {raid['name']}...")
        raid_boss = RaidBoss(**raid)
        db.add(raid_boss)
        added_count += 1

db.commit()
db.close()

print(f"\n{'='*60}")
print(f"✓ Successfully processed {len(legendary_raids)} legendary raid bosses!")
print(f"  - Added: {added_count}")
print(f"  - Updated: {updated_count}")
print(f"{'='*60}")
print("\nYou can now search for ANY legendary raid boss at:")
print("  → http://localhost:3000/raids")
print("\nTry searching for: Mewtwo, Giratina, Rayquaza, Groudon, etc.")
