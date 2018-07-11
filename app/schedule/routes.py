from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    current_app
from flask_login import login_required
from app import db
from app.schedule.forms import ZoneScheduleForm, EditZoneScheduleForm
from app.models import User, Post, Valve, ZoneSchedule
from app.schedule import bp

@bp.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    page = request.args.get('page', 1, type=int)
    zoneSchedules = ZoneSchedule.query.order_by(ZoneSchedule.id).paginate(
        page, current_app.config['VALVES_PER_PAGE'], False)
    next_url = url_for('schedule.schedule', page=zoneSchedules.next_num) \
        if zoneSchedules.has_next else None
    prev_url = url_for('schedule.schedule', page=zoneSchedules.prev_num) \
        if zoneSchedules.has_prev else None
    return render_template('schedule/schedule.html', title='Sprinkler Zone Schedule',
                           zoneSchedules=zoneSchedules.items, next_url=next_url,
                           prev_url=prev_url)

@bp.route('/add_schedule', methods=['GET', 'POST'])
@login_required
def add_schedule():
    form = ZoneScheduleForm()
    if form.validate_on_submit():
        zoneSchedule = ZoneSchedule(
            zone=form.zone.data, 
            runLength=form.runLength.data)
        db.session.add(zoneSchedule)
        db.session.commit()
        flash('Your valve schedule has been added!')
        return redirect(url_for('schedule.schedule'))
    return render_template('schedule/add_schedule.html', title='Schedule a Zone', form=form)

@bp.route('/edit_schedule/<schedule>', methods=['GET', 'POST'])
@login_required
def edit_schedule(schedule):
    form = EditZoneScheduleForm(schedule)
    oldSchedule = ZoneSchedule.query.filter_by(id=schedule).first()
    if form.validate_on_submit():
        oldSchedule.id = form.id.data
        oldSchedule.zone = form.zone.data
        oldSchedule.runLength = form.runLength.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('schedule.schedule'))
    elif request.method == 'GET':
        form.id.data = oldSchedule.id
        form.zone.data = oldSchedule.zone
        form.runLength.data = oldSchedule.runLength
    return render_template('schedule/edit_schedule.html', title='Edit Schedule',
                           form=form)