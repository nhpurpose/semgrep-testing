from flask import Flask, request, jsonify, render_template_string
import sqlite3
import subprocess
import hashlib
import logging
import os

app = Flask(__name__)

# Insecure logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Insecure database connection
def get_db():
    return sqlite3.connect('users.db')

@app.route('/users', methods=['GET'])
def get_user():
    # SQL Injection vulnerability
    username = request.args.get('username')
    conn = get_db()
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"  # Vulnerable!
    cursor.execute(query)
    return jsonify(cursor.fetchall())

@app.route('/execute', methods=['POST'])
def execute_command():
    # Command injection vulnerability
    cmd = request.json.get('command')
    output = subprocess.check_output(cmd, shell=True)  # Vulnerable!
    return output.decode()

@app.route('/template', methods=['POST'])
def render_template():
    # Template injection vulnerability
    template = request.json.get('template')
    return render_template_string(template)  # Vulnerable!

@app.route('/hash', methods=['POST'])
def hash_password():
    # Weak cryptographic hashing
    password = request.json.get('password')
    hashed = hashlib.md5(password.encode()).hexdigest()  # Vulnerable!
    return jsonify({"hashed": hashed})

# Hardcoded credentials
DATABASE_USER = "admin"
DATABASE_PASSWORD = "super_secret_password123"  # Vulnerable!

# Insecure file operations
@app.route('/files/<path:filename>')
def get_file(filename):
    # Path traversal vulnerability
    with open(filename, 'r') as f:  # Vulnerable!
        return f.read()

if __name__ == '__main__':
    # Insecure configuration
    app.run(debug=True, host='0.0.0.0')  # Vulnerable!