from flask import redirect, url_for, current_app, abort, request, flash, \
    session, Blueprint
from flask_login import current_user, login_user, logout_user
import secrets
from urllib.parse import urlencode
import requests
from cookbook.models import User
from cookbook.extensions import db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', "message")
    return redirect(url_for('main.index'))


@bp.route("/<provider>")
def oauth2_authorize(provider):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    session['oauth2_state'] = secrets.token_urlsafe(16)

    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('auth.oauth2_callback', provider=provider,
                                _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })

    session["next_url"] = request.referrer
    return redirect(provider_data['authorize_url'] + '?' + qs)


@bp.route('/callback/<provider>')
def oauth2_callback(provider):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}', "error")
        return redirect(url_for('main.index'))

    if request.args['state'] != session.get('oauth2_state'):
        abort(401)

    if 'code' not in request.args:
        abort(401)

    response = requests.post(
        provider_data['token_url'],
        data={'client_id': provider_data['client_id'],
              'client_secret': provider_data['client_secret'],
              'code': request.args['code'],
              'grant_type': 'authorization_code',
              'redirect_uri':
              url_for(
            'auth.oauth2_callback', provider=provider, _external=True), },
        headers={'Accept': 'application/json'})
    if response.status_code != 200:
        abort(401)
    oauth2_token = response.json().get('access_token')
    if not oauth2_token:
        abort(401)

    response = requests.get(
        provider_data['userinfo']['url'],
        headers={'Authorization': 'Bearer ' + oauth2_token,
                 'Accept': 'application/json', })
    if response.status_code != 200:
        abort(401)
    email = provider_data['userinfo']['email'](response.json())

    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(email=email)
        db.session.add(user)
        db.session.commit()

    login_user(user)
    flash(f"Logged in as {user.email}", "message")
    if session.get("next_url"):
        return redirect(session.get("next_url"))
    else:
        return redirect(url_for('main.index'))
