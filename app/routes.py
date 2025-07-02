# from flask import Blueprint, render_template, request
# from app.models import Tab
# import logging
# from flask import current_app

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .decorators import admin_required, editor_required
from .models import Tab, User, db

main = Blueprint('main', __name__)

# Set up logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    tabs = Tab.query.paginate(page=page, per_page=25)
    return render_template('index.html', tabs=tabs)

@main.route('/tab/<int:tab_id>')
def view_tab(tab_id):
    tab = Tab.query.get_or_404(tab_id)
    return render_template('tab.html', tab=tab)

@main.route('/search')
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

@main.route('/favorite/<int:tab_id>', methods=['POST'])
@login_required
def favorite_tab(tab_id):
    tab = Tab.query.get_or_404(tab_id)
    if tab in current_user.favorites:
        current_user.favorites.remove(tab)
    else:
        current_user.favorites.append(tab)
    db.session.commit()
    return redirect(request.referrer or url_for('main.index'))

@main.route('/edit/<int:tab_id>', methods=['GET', 'POST'])
@editor_required
def edit_tab(tab_id):
    tab = Tab.query.get_or_404(tab_id)
    if request.method == 'POST':
        # Update tab logic
        pass
    return render_template('edit_tab.html', tab=tab)

@main.route('/favorites')
@login_required
def favorites():
    fav_tabs = current_user.favorites
    return render_template('favorites.html', tabs=fav_tabs)    