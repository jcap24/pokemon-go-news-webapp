from flask import Blueprint, jsonify, request
from models.database import get_db, Event
from datetime import datetime, timedelta

events_bp = Blueprint('events', __name__, url_prefix='/api/events')


@events_bp.route('/', methods=['GET'])
def get_all_events():
    """Get all events with optional filtering."""
    try:
        db = get_db()

        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        event_type = request.args.get('type', None)
        source = request.args.get('source', None)
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)

        # Build query
        query = db.query(Event).order_by(Event.start_date.desc(), Event.scraped_date.desc())

        # Filter by event type if provided
        if event_type:
            query = query.filter_by(event_type=event_type)

        # Filter by source if provided
        if source:
            query = query.filter_by(source=source)

        # Filter by date range if provided
        if start_date:
            try:
                start = datetime.fromisoformat(start_date)
                query = query.filter(Event.start_date >= start)
            except ValueError:
                pass

        if end_date:
            try:
                end = datetime.fromisoformat(end_date)
                query = query.filter(Event.end_date <= end)
            except ValueError:
                pass

        # Pagination
        total = query.count()
        offset = (page - 1) * per_page
        events = query.limit(per_page).offset(offset).all()

        db.close()

        return jsonify({
            'success': True,
            'data': [event.to_dict() for event in events],
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


@events_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Get a single event by ID."""
    try:
        db = get_db()
        event = db.query(Event).filter_by(id=event_id).first()
        db.close()

        if not event:
            return jsonify({
                'success': False,
                'error': 'Event not found'
            }), 404

        return jsonify({
            'success': True,
            'data': event.to_dict()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@events_bp.route('/calendar', methods=['GET'])
def get_calendar_events():
    """Get events formatted for calendar view."""
    try:
        db = get_db()

        # Get query parameters for date range (default to current month)
        month = request.args.get('month', datetime.now().month, type=int)
        year = request.args.get('year', datetime.now().year, type=int)

        # Calculate start and end of month
        start_of_month = datetime(year, month, 1)
        if month == 12:
            end_of_month = datetime(year + 1, 1, 1) - timedelta(seconds=1)
        else:
            end_of_month = datetime(year, month + 1, 1) - timedelta(seconds=1)

        # Query events in the month
        events = db.query(Event).filter(
            Event.start_date >= start_of_month,
            Event.start_date <= end_of_month
        ).order_by(Event.start_date).all()

        db.close()

        # Format for calendar
        calendar_events = []
        for event in events:
            calendar_events.append({
                'id': event.id,
                'title': event.title,
                'start': event.start_date.isoformat() if event.start_date else None,
                'end': event.end_date.isoformat() if event.end_date else None,
                'type': event.event_type,
                'summary': event.summary,
                'url': event.url,
                'source': event.source
            })

        return jsonify({
            'success': True,
            'data': calendar_events
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@events_bp.route('/types', methods=['GET'])
def get_event_types():
    """Get list of all event types."""
    try:
        db = get_db()
        types = db.query(Event.event_type).distinct().all()
        db.close()

        return jsonify({
            'success': True,
            'data': [t[0] for t in types if t[0]]
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
