import os
import sys

# Make it run more easily outside PyCharm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import kringlecraft.data.db_session as db_session
from kringlecraft.data.users import User
from kringlecraft.utils.misc_tools import hash_text
from kringlecraft.utils.constants import Role, State  # Import the constants


def main():
    """Performs the initial user setup.
    """
    init_db()
    insert_admin_user()


def insert_admin_user():
    """Adds an administrator to the database. The data is queried via the command line interface.
    """
    u = User()
    u.name = input('Name: ').strip()
    u.email = input('Email: ').strip()
    u.hashed_password = hash_text(input('Password: ').strip())
    u.active = State.ON.value  # default setting for active user
    u.role = Role.ADMIN.value  # default setting for full permissions
    u.notification = State.OFF.value  # default setting for e-mail notifications disabled

    session = db_session.create_session()
    session.add(u)
    session.commit()
    session.close()


def init_db():
    """Initializes the database using the factory pattern.
    """
    top_folder = os.path.dirname(__file__)
    rel_file = os.path.join('..', 'db', 'kringlecraft.sqlite')  # build relative path to DB file
    db_file = os.path.abspath(os.path.join(top_folder, rel_file))  # build full absolute path
    db_session.global_init(db_file)


if __name__ == '__main__':
    main()
