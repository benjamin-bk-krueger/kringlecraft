import os
import sys

import kringlecraft.data.db_session as db_session
from kringlecraft.data.users import User
from kringlecraft.utils.misc_tools import hash_text
from kringlecraft.utils.constants import Roles  # Import the constants

# Make it run more easily outside PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


def main():
    init_db()
    insert_admin_user()


def insert_admin_user():
    u = User()
    u.name = input('Name: ').strip()
    u.email = input('Email: ').strip()
    u.hashed_password = hash_text(input('Password: ').strip())
    u.active = 1
    u.role = Roles.ADMIN
    u.notification = 0

    session = db_session.create_session()
    session.add(u)
    session.commit()
    session.close()


def init_db():
    top_folder = os.path.dirname(__file__)
    rel_file = os.path.join('..', 'db', 'kringlecraft.sqlite')
    db_file = os.path.abspath(os.path.join(top_folder, rel_file))
    db_session.global_init(db_file)


if __name__ == '__main__':
    main()
