from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    current_app
from flask_login import login_required
from app import db
from app.main.forms import ValveForm, EditValveForm
from app.models import Valve
from app.main import bp

@bp.route('/valves', methods=['GET', 'POST'])
@login_required
def valves():
    form = ValveForm()
    if form.validate_on_submit():
        valve = Valve(valve=form.valve.data, description=form.description.data, gpio_pin=form.gpio_pin.data)
        db.session.add(valve)
        db.session.commit()
        flash('Your valve has been added!')
        return redirect(url_for('main.valves'))
    page = request.args.get('page', 1, type=int)
    valves = Valve.query.order_by(Valve.id).paginate(
        page, current_app.config['VALVES_PER_PAGE'], False)
    next_url = url_for('valves', page=valves.next_num) \
        if valves.has_next else None
    prev_url = url_for('valves', page=valves.prev_num) \
        if valves.has_prev else None
    return render_template('valves.html', title='Sprinkler Valves', form=form,
                           valves=valves.items, next_url=next_url,
                           prev_url=prev_url)

@bp.route('/edit_valve/<valve>', methods=['GET', 'POST'])
@login_required
def edit_valve(valve):
    form = EditValveForm(valve)
    oldValve = Valve.query.filter_by(id=valve).first()
    if form.validate_on_submit():
        oldValve.id = form.id.data
        oldValve.valve = form.valve.data
        oldValve.description = form.description.data
        oldValve.gpio_pin = form.gpio_pin.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.valves'))
    elif request.method == 'GET':
        form.id.data = oldValve.id
        form.valve.data = oldValve.valve
        form.description.data = oldValve.description
        form.gpio_pin.data = oldValve.gpio_pin
    return render_template('edit_valve.html', title='Edit Valve',
                           form=form)