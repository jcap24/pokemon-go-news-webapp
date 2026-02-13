from flask import Blueprint, jsonify, request
from models.database import get_db, RaidBoss, RaidCounter
from scrapers.pokebattler import PokebattlerScraper
from datetime import datetime

raids_bp = Blueprint('raids', __name__, url_prefix='/api/raids')


@raids_bp.route('/', methods=['GET'])
def get_all_raids():
    """Get all raid bosses with optional filtering and pagination."""
    try:
        db = get_db()

        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        tier = request.args.get('tier', None)
        active = request.args.get('active', None)

        # Build query
        query = db.query(RaidBoss).order_by(RaidBoss.tier, RaidBoss.name)

        # Filter by tier if provided
        if tier:
            query = query.filter_by(tier=tier)

        # Filter by active status if provided
        if active is not None:
            is_active = active.lower() == 'true'
            query = query.filter_by(is_active=is_active)

        # Pagination
        total = query.count()
        offset = (page - 1) * per_page
        raid_bosses = query.limit(per_page).offset(offset).all()

        db.close()

        return jsonify({
            'success': True,
            'data': [boss.to_dict() for boss in raid_bosses],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@raids_bp.route('/<string:boss_name>/counters', methods=['GET'])
def get_boss_counters(boss_name):
    """Get counters for a specific raid boss."""
    try:
        db = get_db()

        # Get query parameters
        limit = request.args.get('limit', 20, type=int)
        include_shadow = request.args.get('include_shadow', 'true').lower() == 'true'
        include_mega = request.args.get('include_mega', 'true').lower() == 'true'
        include_legendary = request.args.get('include_legendary', 'true').lower() == 'true'

        # Find the raid boss (case-insensitive search)
        raid_boss = db.query(RaidBoss).filter(
            RaidBoss.name.ilike(boss_name)
        ).first()

        if not raid_boss:
            db.close()
            return jsonify({
                'success': False,
                'error': f'Raid boss "{boss_name}" not found'
            }), 404

        # Build counters query
        counters_query = db.query(RaidCounter).filter_by(
            raid_boss_id=raid_boss.id
        ).order_by(RaidCounter.rank)

        # Apply filters
        if not include_shadow:
            counters_query = counters_query.filter_by(is_shadow=False)
        if not include_mega:
            counters_query = counters_query.filter_by(is_mega=False)
        if not include_legendary:
            counters_query = counters_query.filter_by(is_legendary=False)

        # Limit results
        counters = counters_query.limit(limit).all()

        db.close()

        return jsonify({
            'success': True,
            'data': {
                'boss': raid_boss.to_dict(),
                'counters': [counter.to_dict() for counter in counters]
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@raids_bp.route('/search', methods=['GET'])
def search_raid_bosses():
    """Search for raid bosses by name (autocomplete)."""
    try:
        db = get_db()

        # Get query parameter
        query_str = request.args.get('q', '').strip()

        if not query_str:
            db.close()
            return jsonify({
                'success': True,
                'data': []
            })

        # Search for matching raid bosses (case-insensitive)
        raid_bosses = db.query(RaidBoss).filter(
            RaidBoss.name.ilike(f'%{query_str}%')
        ).order_by(RaidBoss.is_active.desc(), RaidBoss.name).limit(10).all()

        db.close()

        # Return simplified data for autocomplete
        results = [{
            'id': boss.id,
            'name': boss.name,
            'tier': boss.tier,
            'is_active': boss.is_active,
            'types': boss.types.split(',') if boss.types else []
        } for boss in raid_bosses]

        return jsonify({
            'success': True,
            'data': results
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@raids_bp.route('/refresh', methods=['POST'])
def refresh_raid_data():
    """Manually trigger a refresh of raid data from Pokebattler."""
    try:
        db = get_db()

        # Initialize scraper
        scraper = PokebattlerScraper()

        # Scrape all raids and counters
        print("Starting manual raid data refresh...")
        raid_data = scraper.scrape_all_raids_and_counters()

        updated_count = 0
        added_count = 0

        # Process each raid boss and its counters
        for raid_entry in raid_data:
            boss_data = raid_entry.get('boss_data', {})
            counters_data = raid_entry.get('counters', [])

            if not boss_data.get('name'):
                continue

            # Check if raid boss already exists
            existing_boss = db.query(RaidBoss).filter_by(name=boss_data['name']).first()

            if existing_boss:
                # Update existing boss
                for key, value in boss_data.items():
                    if hasattr(existing_boss, key) and key != 'id':
                        setattr(existing_boss, key, value)
                existing_boss.last_updated = datetime.utcnow()
                raid_boss = existing_boss
                updated_count += 1
            else:
                # Create new boss
                raid_boss = RaidBoss(**boss_data)
                db.add(raid_boss)
                db.flush()  # Get the ID
                added_count += 1

            # Delete old counters for this boss
            db.query(RaidCounter).filter_by(raid_boss_id=raid_boss.id).delete()

            # Add new counters
            for counter_data in counters_data:
                counter_data['raid_boss_id'] = raid_boss.id
                counter = RaidCounter(**counter_data)
                db.add(counter)

        db.commit()
        db.close()

        print(f"Raid data refresh complete: {added_count} added, {updated_count} updated")

        return jsonify({
            'success': True,
            'data': {
                'added': added_count,
                'updated': updated_count,
                'total_processed': len(raid_data)
            }
        })

    except Exception as e:
        db.rollback()
        db.close()
        print(f"Error refreshing raid data: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@raids_bp.route('/tiers', methods=['GET'])
def get_raid_tiers():
    """Get list of all raid tiers."""
    try:
        db = get_db()
        tiers = db.query(RaidBoss.tier).distinct().all()
        db.close()

        return jsonify({
            'success': True,
            'data': [tier[0] for tier in tiers if tier[0]]
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
