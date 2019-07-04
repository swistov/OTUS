import sqlite3

from orm.db.check import full_path, db, control_foreign_keys


class Field:
    def __init__(self,
                 field_type=None,
                 is_null=False,
                 pk=False,
                 auto_increment=False,
                 foreign_key=None):

        if not field_type and not foreign_key:
            return TypeError('Add <field_type>. Not created.')

        self.type = field_type

        if not is_null:
            self.is_null = 'NOT NULL'
        if pk:
            self.pk = 'PRIMARY KEY'
        if auto_increment:
            self.auto_increment = 'AUTOINCREMENT'
        if foreign_key:
            self.foreign_key = foreign_key


def db_conn():
    connection = sqlite3.dbapi2.connect(full_path)
    if control_foreign_keys:
        connection.cursor().execute('PRAGMA foreign_keys = ON;')
    return connection
