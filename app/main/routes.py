from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, PostForm, ValveForm, EditValveForm, \
    ZoneScheduleForm, EditZoneScheduleForm
from app.models import User, Post, Valve, ZoneSchedule
from app.main import bp


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Explore',
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username,
                       page=posts.next_num) if posts.has_next else None
    prev_url = url_for('main.user', username=user.username,
                       page=posts.prev_num) if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %(username)s not found.', username=username)
        return redirect(url_for('main.index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %(username)s not found.', username=username)
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following %(username)s.', username=username)
    return redirect(url_for('main.user', username=username))

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

@bp.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    page = request.args.get('page', 1, type=int)
    zoneSchedules = ZoneSchedule.query.order_by(ZoneSchedule.id).paginate(
        page, current_app.config['VALVES_PER_PAGE'], False)
    next_url = url_for('schedule', page=zoneSchedules.next_num) \
        if zoneSchedules.has_next else None
    prev_url = url_for('schedule', page=zoneSchedules.prev_num) \
        if zoneSchedules.has_prev else None
    return render_template('schedule.html', title='Sprinkler Zone Schedule',
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
        return redirect(url_for('main.schedule'))
    return render_template('add_schedule.html', title='Schedule a Zone', form=form)

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
        return redirect(url_for('main.schedule'))
    elif request.method == 'GET':
        form.id.data = oldSchedule.id
        form.zone.data = oldSchedule.zone
        form.runLength.data = oldSchedule.runLength
    return render_template('edit_schedule.html', title='Edit Schedule',
                           form=form)