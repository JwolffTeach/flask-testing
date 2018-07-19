from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    current_app
from flask_login import login_required
from app import db
from app.schedule.forms import ZoneScheduleForm, EditZoneScheduleForm, Schedule_Days_Form, Schedule_Valves_Form
from app.models import User, Post, Valve, ZoneSchedule
from app.schedule import bp

@bp.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    page = request.args.get('page', 1, type=int)
    zoneSchedules = ZoneSchedule.query.join(
            Valve, 
            ZoneSchedule.zone == Valve.valve
            ).add_columns(
                Valve.valve, 
                Valve.description, 
                Valve.gpio_pin, 
                ZoneSchedule.runLength, 
                ZoneSchedule.m, 
                ZoneSchedule.t, 
                ZoneSchedule.w, 
                ZoneSchedule.th, 
                ZoneSchedule.f, 
                ZoneSchedule.s, ZoneSchedule.su
            ).order_by(ZoneSchedule.id).paginate(
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
            runLength=form.runLength.data,
            m=form.m.data,
            t=form.t.data,
            w=form.w.data,
            th=form.th.data,
            f=form.f.data,
            s=form.s.data,
            su=form.su.data)
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
    valves = Valve.query.filter_by(valve=schedule).first()
    description = valves.description
    if form.validate_on_submit():
        oldSchedule.id = form.id.data
        oldSchedule.zone = form.zone.data
        oldSchedule.runLength = form.runLength.data
        oldSchedule.m=form.m.data
        oldSchedule.t=form.t.data
        oldSchedule.w=form.w.data
        oldSchedule.th=form.th.data
        oldSchedule.f=form.f.data
        oldSchedule.s=form.s.data
        oldSchedule.su=form.su.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('schedule.schedule'))
    elif request.method == 'GET':
        form.id.data = oldSchedule.id
        form.zone.data = oldSchedule.zone
        form.runLength.data = oldSchedule.runLength
        form.description.data = description
        form.m.data = oldSchedule.m
        form.t.data = oldSchedule.t
        form.w.data = oldSchedule.w
        form.th.data = oldSchedule.th
        form.f.data = oldSchedule.f
        form.s.data = oldSchedule.s
        form.su.data = oldSchedule.su
    return render_template('schedule/edit_schedule.html', title='Edit Schedule',
                           form=form)