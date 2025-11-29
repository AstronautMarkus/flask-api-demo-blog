from flask import request, jsonify
from app.models import RefreshToken
from . import auth_bp
from app import db

@auth_bp.route('/logout', methods=['POST'])
def logout():
    data = request.json
    refresh_token = data.get('refresh_token')
    if not refresh_token:
        return jsonify({'error': 'Refresh token required.'}), 400

    token_obj = RefreshToken.query.filter_by(token=refresh_token, revoked=False).first()
    if not token_obj:
        return jsonify({'error': 'Invalid or already revoked refresh token.'}), 400

    token_obj.revoked = True
    db.session.commit()
    return jsonify({'message': 'Logout successful. Token revoked.'}), 200
