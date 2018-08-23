import uuid
from flask import jsonify, session
import re
import psycopg2
from datetime import date, datetime
from connect import conn
from passlib.hash import sha256_crypt
cur = conn.cursor()

class User(object):

    def __init__(self,username=None, email=None, password=None):
        super(User, self).__init__()
        self.username = username
        self.email = email
        self.password = password

    def save(self):
        conn.commit()

    def create(self):
        """Create users"""
        if self.username_exist(self.username) is False
            """hash the password"""
            hash_pass = self.hash_password(self.password)
            """call cursor to read INSERT query"""
            cur.execute(
                """
                INSERT INTO users (username, email, password)
                VALUES (%s, %s, %s) RETURNING id;
                """,
                (self.username, self.email, hash_pass))
            """fetch the new user, pick the id, and assign to userid"""
            userid = cur.fetchone()[0]
            """save user"""
            self.save()
             return jsonify({"message": "Successful", "user": self.user_by_id(userid)}), 201
        return jsonify({"message": "Username is taken."}), 400

    def get_all_users(self):
        """retrieve all users"""
        cur.execute("SELECT * FROM users")
        """fetch all users using cursor and assign results to users_tuple"""
        users_tuple = cur.fetchall()
        users = []

        for user in users_tuple:
            """append user after serializing to the list"""
            users.append(self.serializer(user))
        return jsonify({"Users": users})


    def get_user_by_username(self, username):
        """retrieve a specific user"""
        cur.execute(
            "SELECT * FROM users where username=%s", (username))
        user = cur.fetchone()
        if user:
            return self.serializer(user)
        return False

    def serializer(self, user):
        return dict(
            id=user[0],
            username=user[1],
            email=user[2],
            password=user[3]
        )

    def username_exist(self, username):
        """ check if user with the same username already exist """
        cur.execute("SELECT * FROM users WHERE username = %s;", (username,))
        user = cur.fetchone()
        if user:
            return True
        else:
            return False

    def hash_password(self, password):
        """Hash Password """
        h_pass = sha256_crypt.encrypt(password)
        return h_pass

    def verify_password(self, password, h_pass):
        """ Verify Password"""
        h_pass = sha256_crypt.verify(password, h_pass)
        return h_pass

    def serialiser_user(self, user):
        """ Serialize tuple into dictionary """
        print()
        user_details = dict(
            id=user[0],
            username=user[1],
            email=user[2],
            password=user[4]
        )
        return user_details

    def user_by_id(self, id):
        """ Serialize tuple into dictionary """
        cur.execute("SELECT * FROM users WHERE id = %s;", (id,))
        user = cur.fetchone()

    return self.serialiser_user(user)

    