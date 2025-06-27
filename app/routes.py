from flask import Blueprint, render_template, request
from app.models import Tab
import logging
from flask import current_app

bp = Blueprint('routes', __name__)

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    tabs = Tab.query.paginate(page=page, per_page=25)
    return render_template('index.html', tabs=tabs)

@bp.route('/tab/<int:tab_id>')
def view_tab(tab_id):
    tab = Tab.query.get_or_404(tab_id)
    return render_template('tab.html', tab=tab)

@bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 25
    
    if query:
        # Use case-insensitive search with proper wildcards
        search_term = f"%{query}%"
        results = Tab.query.filter(
            Tab.artist.ilike(search_term) | 
            Tab.song.ilike(search_term) |
            Tab.genre.ilike(search_term)
        ).paginate(page=page, per_page=per_page)
    else:
        results = Tab.query.paginate(page=page, per_page=per_page)
    
    return render_template('index.html', tabs=results, query=query)