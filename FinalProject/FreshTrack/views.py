from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime, timedelta, date
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import GroceryItem
from . import db

views = Blueprint('views', __name__)

# landing page route
@views.route('/')
def landing_page():
    return render_template('landingpage.html', user=current_user)

# home page route
@views.route('/home')
@login_required
def home():
    return render_template('home.html', user=current_user, today=date.today())

# add grocery item route
# This route handles the addition of grocery items
# When the user clicks the add grocery button, they are redirected to the add grocery page
@views.route('/add_grocery', methods=['GET', 'POST'])
@login_required
def add_grocery():
    if request.method == 'POST':
        name = request.form.get('name')
        quantity = request.form.get('quantity', 1)
        expiry_date = request.form.get('expiry')
        category = request.form.get('category')

        new_item = GroceryItem(
            name=name,
            quantity=quantity,
            expiry_date=datetime.strptime(expiry_date, '%Y-%m-%d') if expiry_date else None,
            category=category,
            user_id=current_user.id
        )
        db.session.add(new_item)
        db.session.commit()
        flash('Item added!', 'success')
        return redirect(url_for('views.home'))

    return render_template("add_grocery.html", user=current_user)

# edit grocery item route
@views.route('/delete-item/<int:id>', methods=['POST'])
@login_required
def delete_item(id):
    item = GroceryItem.query.get_or_404(id)
    
    # Ensure user owns the item
    if item.user_id != current_user.id:
        flash("Not authorized to delete this item", "error")
        return redirect(url_for('views.home'))
    
    db.session.delete(item)
    db.session.commit()
    flash("Item deleted", "success")
    return redirect(url_for('views.home'))