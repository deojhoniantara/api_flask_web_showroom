from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from flask_jwt_extended import jwt_required, get_jwt_identity

notifications_endpoints = Blueprint('notifications_endpoints', __name__)

# GET notifications for logged in user
@notifications_endpoints.route('/my', methods=['GET'])
@jwt_required()
def get_my_notifications():
    user_id = get_jwt_identity()
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT n.id, n.message, n.is_read, n.created_at, b.booking_date, b.method, v.name as vehicle_name
        FROM notifications n
        LEFT JOIN bookings b ON n.booking_id = b.id
        LEFT JOIN vehicles v ON b.vehicle_id = v.id
        WHERE n.receiver_id = %s
        ORDER BY n.created_at DESC
    """
    cursor.execute(query, (user_id,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify({"message": "OK", "data": data}), 200


# MARK notification as read
@notifications_endpoints.route('/read/<int:notif_id>', methods=['PUT'])
@jwt_required()
def mark_as_read(notif_id):
    user_id = get_jwt_identity()
    conn = get_connection()
    cursor = conn.cursor()

    # Ensure the notification belongs to this user
    cursor.execute("SELECT id FROM notifications WHERE id = %s AND receiver_id = %s", (notif_id, user_id))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"message": "Notification not found"}), 404

    cursor.execute("UPDATE notifications SET is_read = 1 WHERE id = %s", (notif_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Notification marked as read", "notification_id": notif_id}), 200


# CREATE notification (optional, for admin or system to send)
@notifications_endpoints.route('/create', methods=['POST'])
@jwt_required()
def create_notification():
    receiver_id = request.form.get('receiver_id')
    booking_id = request.form.get('booking_id')
    message = request.form.get('message')

    if not all([receiver_id, message]):
        return jsonify({"msg": "receiver_id and message are required"}), 400

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notifications (receiver_id, booking_id, message)
        VALUES (%s, %s, %s)
    """, (receiver_id, booking_id, message))
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return jsonify({
        "message": "Notification sent",
        "notification_id": new_id
    }), 201
