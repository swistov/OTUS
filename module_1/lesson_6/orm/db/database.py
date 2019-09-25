import sqlite3
from loguru import logger

from orm.db.check import full_path, db, control_foreign_keys


class Field:
    def __init__(self,
                 field_type=None,
                 is_null=False,
                 pk=False,
                 auto_increment=False,
                 foreign_key=None):

        if not field_type and not foreign_key:
            logger.error('Add <field_type>. Not created.')
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


def sql_select_as(from_table: str, fields_list: list):
    table_dot_only = ['.'.join(i) for i in
                      list(zip([from_table] * len(fields_list), fields_list))]
    fields_as = ['__'.join(i) for i in
                 list(zip([from_table] * len(fields_list), fields_list))]
    table_dot_only_fields_as = [' as '.join(i) for i in
                                list(zip(table_dot_only, fields_as))]

    return ', '.join(table_dot_only_fields_as)


def db_conn():
    try:
        connection = sqlite3.dbapi2.connect(full_path)
    except:
        logger.error('Problem with connect to DB')
    if control_foreign_keys:
        connection.cursor().execute('PRAGMA foreign_keys = ON;')
    return connection
