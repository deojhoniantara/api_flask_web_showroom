from flask import Blueprint, request, jsonify
from helper.db_helper import get_connection
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

articles_endpoints = Blueprint('articles_endpoints', __name__)


# GET all articles
@articles_endpoints.route('/read', methods=['GET'])
def read_articles():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM articles ORDER BY published_date DESC")
    articles = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"message": "OK", "data": articles}), 200


# GET article by ID
@articles_endpoints.route('/read/<int:article_id>', methods=['GET'])
def read_article_by_id(article_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM articles WHERE id = %s", (article_id,))
    article = cursor.fetchone()
    cursor.close()
    conn.close()
    if article:
        return jsonify({"message": "OK", "data": article}), 200
    return jsonify({"message": "Article not found"}), 404


# CREATE new article
@articles_endpoints.route('/create', methods=['POST'])
@jwt_required()
def create_article():
    claims = get_jwt_identity()
    if claims.get('role') != 'admin':
        return jsonify({"msg": "Admin only"}), 403

    title = request.form.get('title')
    content = request.form.get('content')

    if not all([title, content]):
        return jsonify({"msg": "title, and content are required"}), 400
    
    published_date = datetime.now().strftime("%Y-%m-%d")  # atau gunakan datetime.now() jika kolom bertipe DATETIME

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO articles (title, published_date, content) VALUES (%s, %s, %s)",
            (title, published_date, content)
        )
        conn.commit()
        article_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({
            "msg": "Article created", 
            "article_id": article_id,
            "title": title}), 201
    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({"msg": str(e)}), 500
    

# UPDATE article
@articles_endpoints.route('/update/<int:article_id>', methods=['PUT'])
@jwt_required()
def update_article(article_id):
    claims = get_jwt_identity()
    if claims.get('role') != 'admin':
        return jsonify({"msg": "Admin only"}), 403
    
    title = request.form.get('title')
    content = request.form.get('content')

    if not all([title, content]):
        return jsonify({"msg": "title, and content are required"}), 400
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE articles SET title = %s, content = %s WHERE id = %s",
        (title, content, article_id)
    )
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"msg": "Article not found"}), 404
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"msg": "Article updated", "article_id": article_id, "title": title}), 200


# DELETE article
@articles_endpoints.route('/delete/<int:article_id>', methods=['DELETE'])
@jwt_required()
def delete_article(article_id):
    claims = get_jwt_identity()
    if claims.get('role') != 'admin':   
        return jsonify({"msg": "Admin only"}), 403
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles WHERE id = %s", (article_id,))
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"msg": "Article not found"}), 404  
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"msg": "Article deleted", "article_id": article_id}), 200
