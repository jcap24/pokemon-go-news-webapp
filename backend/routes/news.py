from flask import Blueprint, jsonify, request
from models.database import get_db, NewsItem
from datetime import datetime

news_bp = Blueprint('news', __name__, url_prefix='/api/news')


@news_bp.route('/', methods=['GET'])
def get_all_news():
    """Get all news items with optional pagination."""
    try:
        db = get_db()

        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        source = request.args.get('source', None)

        # Build query
        query = db.query(NewsItem).order_by(NewsItem.published_date.desc(), NewsItem.scraped_date.desc())

        # Filter by source if provided
        if source:
            query = query.filter_by(source=source)

        # Pagination
        total = query.count()
        offset = (page - 1) * per_page
        news_items = query.limit(per_page).offset(offset).all()

        db.close()

        return jsonify({
            'success': True,
            'data': [item.to_dict() for item in news_items],
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


@news_bp.route('/<int:news_id>', methods=['GET'])
def get_news_item(news_id):
    """Get a single news item by ID."""
    try:
        db = get_db()
        news_item = db.query(NewsItem).filter_by(id=news_id).first()
        db.close()

        if not news_item:
            return jsonify({
                'success': False,
                'error': 'News item not found'
            }), 404

        return jsonify({
            'success': True,
            'data': news_item.to_dict()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@news_bp.route('/sources', methods=['GET'])
def get_sources():
    """Get list of all news sources."""
    try:
        db = get_db()
        sources = db.query(NewsItem.source).distinct().all()
        db.close()

        return jsonify({
            'success': True,
            'data': [source[0] for source in sources]
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
