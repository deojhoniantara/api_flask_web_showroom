from flask import Blueprint, request, jsonify
from db import get_db_connection
from helper.form_validation import get_form_data

users_endpoints = Blueprint('users_endpoints', __name__)

# GET all users
@users_endpoints.route('/', methods=['GET'])
def get_all_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, name, email, type, created_at, updated_at FROM users")
        users = cursor.fetchall()

        cursor.close()
        conn.close()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET user by ID
@users_endpoints.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, name, email, type, created_at, updated_at FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()
        if user:
            return jsonify(user), 200
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET all dealers
@users_endpoints.route('/dealers', methods=['GET'])
def get_all_dealers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT users.id, users.name, users.email, users.type,
           dealers.dealer_name, dealers.address, dealers.phone
        FROM users
        JOIN dealers ON users.id = dealers.user_id
        WHERE users.type = 'dealer'
    """)
    dealers = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"message": "OK", "data": dealers}), 200

# GET all individuals
@users_endpoints.route('/individuals', methods=['GET'])
def get_all_individuals():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT users.id, users.name, users.email, users.type,
           individuals.address, individuals.phone
        FROM users
        JOIN individuals ON users.id = individuals.user_id
        WHERE users.type = 'individual'
    """)
    individuals = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"message": "OK", "data": individuals}), 200

# POST create user
@users_endpoints.route('/register', methods=['POST'])
def create_user():
    required = get_form_data(["name", "email", "password", "type"])
    name = required["name"]
    email = required["email"]
    password = required["password"]
    user_type = required["type"]  # 'dealer' or 'individual'

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.close()
            conn.close()
            return jsonify({
                "message": "Conflict",
                "description": "User with this email already exists"
            }), 409
        if user_type not in ['dealer', 'individual']:
            cursor.close()
            conn.close()
            return jsonify({
                "message": "Bad Request",
                "description": "Invalid user type"
            }), 400
        # Insert new user
        cursor.execute("""
            INSERT INTO users (name, email, password, type)
            VALUES (%s, %s, %s, %s)
        """, (name, email, password, user_type))
        conn.commit()
        new_id = cursor.lastrowid

        if user_type == 'dealer':
            required = get_form_data(["dealer_name", "address", "phone"])
            dealer_name = required["dealer_name"]
            address = required["address"]
            phone = required["phone"]

            cursor.execute("""
                INSERT INTO dealers (user_id, dealer_name, address, phone)
                VALUES (%s, %s, %s, %s)
            """, (new_id, dealer_name, address, phone))
            conn.commit()
        
        if user_type == 'individual':
            required = get_form_data(["address", "phone"])
            address = required["address"]
            phone = required["phone"]

            cursor.execute("""
                INSERT INTO individuals (user_id, address, phone)
                VALUES (%s, %s, %s)
            """, (new_id, address, phone))
            conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
                    "message": "OK",
                    "description": "User created successfully",
                    "user_id": new_id,
                    "name": name,
                    "email": email,
                    "type": user_type
                }), 201
    except Exception as e:
            return jsonify({"error": str(e)}), 500

# PUT update user
@users_endpoints.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    required = get_form_data(["name", "email", "type"])
    name = required["name"]
    email = required["email"]
    user_type = required["type"]  # 'dealer' or 'individual'
    password = request.form.get('password')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            cursor.close()
            conn.close()
            return jsonify({
                "message": "Not Found",
                "description": "User not found"
            }), 404

        if user_type not in ['dealer', 'individual']:
            cursor.close()
            conn.close()
            return jsonify({
                "message": "Bad Request",
                "description": "Invalid user type"
            }), 400

        # Update users table
        cursor.execute("""
            UPDATE users SET name = %s, email = %s, password = %s, type = %s
            WHERE id = %s
        """, (name, email, password, user_type, user_id))
        conn.commit()

        # Update dealer or individual data
        if user_type == 'dealer':
            required = get_form_data(["dealer_name", "address", "phone"])
            dealer_name = required["dealer_name"]
            address = required["address"]
            phone = required["phone"]

            # Check if dealer entry exists
            cursor.execute("SELECT user_id FROM dealers WHERE user_id = %s", (user_id,))
            if cursor.fetchone():
                # Update dealer
                cursor.execute("""
                    UPDATE dealers
                    SET dealer_name = %s, address = %s, phone = %s
                    WHERE user_id = %s
                """, (dealer_name, address, phone, user_id))
            else:
                # Insert dealer
                cursor.execute("""
                    INSERT INTO dealers (user_id, dealer_name, address, phone)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, dealer_name, address, phone))
            conn.commit()

        if user_type == 'individual':
            required = get_form_data(["address", "phone"])
            address = required["address"]
            phone = required["phone"]

            # Check if individual entry exists
            cursor.execute("SELECT user_id FROM individuals WHERE user_id = %s", (user_id,))
            if cursor.fetchone():
                # Update individual
                cursor.execute("""
                    UPDATE individuals
                    SET address = %s, phone = %s
                    WHERE user_id = %s
                """, (address, phone, user_id))
            else:
                # Insert individual
                cursor.execute("""
                    INSERT INTO individuals (user_id, address, phone)
                    VALUES (%s, %s, %s)
                """, (user_id, address, phone))
            conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "message": "OK",
            "description": "User updated successfully",
            "user_id": user_id,
            "name": name,
            "email": email,
            "type": user_type
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# DELETE user
@users_endpoints.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500