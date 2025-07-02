import os
from flask import Blueprint, jsonify, request
from helper.db_helper import get_connection
from helper.form_validation import get_form_data
from datetime import datetime
from db import get_db_connection
from flask_jwt_extended import jwt_required, get_jwt_identity

vehicles_endpoints = Blueprint('vehicles', __name__)
UPLOAD_FOLDER = "img"

def default_datetime_handler(obj):
    """Convert datetime objects to ISO format strings."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

# GET all vehicles
@vehicles_endpoints.route('/', methods=['GET'])
def get_all_vehicles():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, name, description, price, brand, type, image, created_at, updated_at FROM vehicles")
        vehicles = cursor.fetchall()

        cursor.close()
        conn.close()
        return jsonify(vehicles), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET vehicle by ID
@vehicles_endpoints.route('/read/<vehicle_id>', methods=['GET'])
def read_by_id(vehicle_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM vehicles WHERE id = %s", (vehicle_id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return jsonify({"message": "OK", "data": result}), 200
    return jsonify({"message": "Vehicle not found"}), 404

# CREATE new vehicle
@vehicles_endpoints.route('/create', methods=['POST'])
@jwt_required()
def create():
    required = get_form_data(["name", "price", "brand", "type"])
    name = required["name"]
    description = request.form.get('description')
    price = required["price"]
    brand = required["brand"]
    vtype = required["type"]  # 'new' / 'used'
    image = request.form.get('image', None)

    user_id = get_jwt_identity()  # owner from JWT

    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if vtype not in ['new', 'used']:
                cursor.close()
                conn.close()
                return jsonify({
                    "message": "Bad Request",
                    "description": "Invalid user type"
                }), 400
        
        insert_query = """
            INSERT INTO vehicles (user_id, name, description, price, brand, type, image)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (user_id, name, description, price, brand, vtype, image))
        conn.commit()
        vehicle_id = cursor.lastrowid

        if vtype == 'new':
            required = get_form_data(["transmission", "seats", "color", "year", "location", "fuel_type", "stock"])
            transmission = request.form.get('transmission')
            seats = request.form.get('seats')
            color = request.form.get('color')
            year = request.form.get('year')
            location = request.form.get('location')
            fuel_type = request.form.get('fuel_type')
            stock = request.form.get('stock')

            cursor.execute("""
                INSERT INTO new_vehicles (vehicle_id, transmission, seats, color, year, location, fuel_type, stock)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (vehicle_id, transmission, seats, color, year, location, fuel_type, stock))

        elif vtype == 'used':
            required = get_form_data(["transmission", "seats", "color", "year", "location", "fuel_type", "mileage"])
            transmission = request.form.get('transmission')
            seats = request.form.get('seats')
            color = request.form.get('color')
            year = request.form.get('year')
            location = request.form.get('location')
            fuel_type = request.form.get('fuel_type')
            mileage = request.form.get('mileage')

            cursor.execute("""
                INSERT INTO used_vehicles (vehicle_id, transmission, seats, color, year, location, fuel_type, mileage)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (vehicle_id, transmission, seats, color, year, location, fuel_type, mileage))

        conn.commit()
        cursor.close()
        conn.close()

        if vehicle_id:
            return jsonify({"message": "Vehicle added", "vehicle_id": vehicle_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@vehicles_endpoints.route('/update/<vehicle_id>', methods=['PUT'])
@jwt_required()
def update(vehicle_id):
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    brand = request.form.get('brand')
    vtype = request.form.get('type')
    image = request.form.get('image')

    connection = get_connection()
    cursor = connection.cursor()

    # Update table vehicles
    update_query = """
        UPDATE vehicles SET name=%s, description=%s, price=%s, brand=%s, type=%s, image=%s
        WHERE id = %s
    """
    cursor.execute(update_query, (name, description, price, brand, vtype, image, vehicle_id))

    # Update table new_vehicles if type is 'new'
    if vtype == 'new':
        required = get_form_data(["transmission", "seats", "color", "year", "location", "fuel_type", "stock"])
        transmission = required["transmission"]
        seats = required["seats"]
        color = required["color"]
        year = required["year"]
        location = required["location"]
        fuel_type = required["fuel_type"]
        stock = required["stock"]

        # Check if entry exists
        cursor.execute("SELECT vehicle_id FROM new_vehicles WHERE vehicle_id = %s", (vehicle_id,))
        if cursor.fetchone():
            # Update existing
            cursor.execute("""
                UPDATE new_vehicles
                SET transmission=%s, seats=%s, color=%s, year=%s, location=%s, fuel_type=%s, stock=%s
                WHERE vehicle_id=%s
            """, (transmission, seats, color, year, location, fuel_type, stock, vehicle_id))
        else:
            # Insert if not exists
            cursor.execute("""
                INSERT INTO new_vehicles (vehicle_id, transmission, seats, color, year, location, fuel_type, stock)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (vehicle_id, transmission, seats, color, year, location, fuel_type, stock))

    # Update table used_vehicles if type is 'used'
    elif vtype == 'used':
        required = get_form_data(["transmission", "seats", "color", "year", "location", "fuel_type", "mileage"])
        transmission = required["transmission"]
        seats = required["seats"]
        color = required["color"]
        year = required["year"]
        location = required["location"]
        fuel_type = required["fuel_type"]
        mileage = required["mileage"]

        # Check if entry exists
        cursor.execute("SELECT vehicle_id FROM used_vehicles WHERE vehicle_id = %s", (vehicle_id,))
        if cursor.fetchone():
            # Update existing
            cursor.execute("""
                UPDATE used_vehicles
                SET transmission=%s, seats=%s, color=%s, year=%s, location=%s, fuel_type=%s, mileage=%s
                WHERE vehicle_id=%s
            """, (transmission, seats, color, year, location, fuel_type, mileage, vehicle_id))
        else:
            # Insert if not exists
            cursor.execute("""
                INSERT INTO used_vehicles (vehicle_id, transmission, seats, color, year, location, fuel_type, mileage)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (vehicle_id, transmission, seats, color, year, location, fuel_type, mileage))

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Vehicle updated", "vehicle_id": vehicle_id}), 200


# DELETE vehicle
@vehicles_endpoints.route('/delete/<vehicle_id>', methods=['DELETE'])
@jwt_required()
def delete(vehicle_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM vehicles WHERE id = %s", (vehicle_id,))
    connection.commit()
    cursor.close()
    return jsonify({"message": "Vehicle deleted", "vehicle_id": vehicle_id}), 200

