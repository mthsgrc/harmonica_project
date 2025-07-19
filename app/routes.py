# import logging

from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .decorators import admin_required, editor_required, roles_required
from .forms import EditTabForm, AddTabForm
from .models import Tab, User, db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


main = Blueprint('main', __name__)

# Set up logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    tabs = Tab.query.paginate(page=page, per_page=24)
    return render_template('index.html', tabs=tabs)


@main.route('/tab/<int:tab_id>')
def view_tab(tab_id):
    tab = Tab.query.get_or_404(tab_id)
    return render_template('tab.html', tab=tab)


@main.route('/search')
def search():
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 24
    
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


@main.route('/toggle_favorite/<int:tab_id>', methods=['POST'])
@login_required
def toggle_favorite(tab_id):
    tab = Tab.query.get_or_404(tab_id)
    if tab in current_user.favorites:
        current_user.favorites.remove(tab)
        action = 'removed'
        flash(f'Removed {tab.song} from favorites', 'info')
    else:
        current_user.favorites.append(tab)
        action = 'added'
        flash(f'Removed {tab.song} from favorites', 'info')
    db.session.commit()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'status': 'success', 'action': action})
    return redirect(request.referrer or url_for('main.index'))


@main.route('/favorites')
@login_required
def favorites():
    sort_by = request.args.get('sort', 'recent')  # Get sort parameter or default to 'recent'
    
    # Get favorites with eager loading to prevent N+1 query problem
    user = User.query.options(db.joinedload(User.favorites)).get(current_user.id)
    
    if sort_by == 'artist':
        favorites = sorted(user.favorites, key=lambda x: (x.artist.lower(), x.song.lower()))
    else:  # recent
        favorites = sorted(user.favorites, key=lambda x: x.id, reverse=True)
    
    return render_template('favorites.html', 
                         favorites=favorites,
                         sort_by=sort_by,
                         user=user,
                         )


@main.route('/profile')
@login_required
def profile():
    sort_by = request.args.get('sort', 'recent')  # Get sort parameter or default to 'recent'
    
    # Get favorites with eager loading to prevent N+1 query problem
    user = User.query.options(db.joinedload(User.favorites)).get(current_user.id)
    
    if sort_by == 'artist':
        favorites = sorted(user.favorites, key=lambda x: (x.artist.lower(), x.song.lower()))
    else:  # recent
        favorites = sorted(user.favorites, key=lambda x: x.id, reverse=True)
    
    return render_template('profile.html', 
                         favorites=favorites,
                         sort_by=sort_by,
                         user=user,
                         )


@main.route('/change_password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    # Validation
    if not all([current_password, new_password, confirm_password]):
        flash('All fields are required')
        return redirect(url_for('main.profile'))
    
    if new_password != confirm_password:
        flash('New passwords must match')
        return redirect(url_for('main.profile'))
    
    if len(new_password) < 4:
        flash('Password must be at least 4 characters')
        return redirect(url_for('main.profile'))
    
    # Verify current password
    if not check_password_hash(current_user.password_hash, current_password):
        flash('Current password is incorrect')
        return redirect(url_for('main.profile'))
    
    # Update password
    current_user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    
    flash('Password updated successfully!')
    return redirect(url_for('main.profile'))


@main.route('/profile/bulk_favorites', methods=['POST'])
@login_required
def bulk_favorite_action():
    tab_ids = request.form.getlist('tab_ids')
    action = request.form.get('action')
    
    if not tab_ids:
        flash('No tabs selected', 'warning')
        return redirect(url_for('main.profile'))
    
    tabs = Tab.query.filter(Tab.id.in_(tab_ids)).all()
    
    if action == 'remove':
        for tab in tabs:
            if tab in current_user.favorites:
                current_user.favorites.remove(tab)
        db.session.commit()
        flash(f'Removed {len(tabs)} tabs from favorites', 'success')
    elif action == 'download':
        # Implement download logic here
        flash('Download feature coming soon!', 'info')
    
    return redirect(url_for('main.profile'))

from app.forms import EditTabForm
from app.decorators import editor_required


@main.route('/edit-tab/<int:tab_id>', methods=['GET', 'POST'])
@roles_required('admin', 'editor')
def edit_tab(tab_id):
    tab = Tab.query.get_or_404(tab_id)
    form = EditTabForm(obj=tab)
    
    if form.validate_on_submit():
        form.populate_obj(tab)
        db.session.commit()
        flash('Tab updated successfully!', 'success')
        return redirect(url_for('main.view_tab', tab_id=tab.id))
    
    return render_template('edit_tab.html', form=form, tab=tab)


@main.route('/delete-tab/<int:tab_id>', methods=['POST'])
@roles_required('admin')
def delete_tab(tab_id):
    tab = Tab.query.get_or_404(tab_id)
    db.session.delete(tab)
    db.session.commit()
    flash(f'Tab "{tab.song}" by {tab.artist} has been deleted', 'success')
    return redirect(url_for('main.index'))


@main.route('/all-tabs')
@roles_required('admin', 'editor')
def all_tabs():
    page = request.args.get('page', 1, type=int)
    per_page = 50
    tabs = Tab.query.order_by(Tab.artist, Tab.song).paginate(page=page, per_page=per_page)
    return render_template('all_tabs.html', tabs=tabs)


@main.route('/search-tabs')
@roles_required('admin', 'editor')
def search_tabs():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    if query:
        tabs = Tab.query.filter(
            Tab.artist.ilike(f'%{query}%') | 
            Tab.song.ilike(f'%{query}%') |
            Tab.content.ilike(f'%{query}%')
        ).paginate(page=page, per_page=per_page)
    else:
        tabs = Tab.query.paginate(page=page, per_page=per_page)
        
    return render_template('all_tabs.html', tabs=tabs, query=query)


@main.route('/add-tab', methods=['GET', 'POST'])
@roles_required('admin', 'editor')
def add_tab():
    form = AddTabForm()
    
    if form.validate_on_submit():
        new_tab = Tab(
            artist=form.artist.data,
            song=form.song.data,
            difficulty=form.difficulty.data,
            genre=form.genre.data,
            harp_type=form.harp_type.data,
            harp_key=form.harp_key.data,
            content=form.content.data,
            youtube_link=form.youtube_link.data,
            created_at=datetime.utcnow()
        )
        db.session.add(new_tab)
        db.session.commit()
        flash(f'Tab "{form.song.data}" by {form.artist.data} added successfully!', 'success')
        return redirect(url_for('main.view_tab', tab_id=new_tab.id))
    
    return render_template('add_tab.html', form=form)

