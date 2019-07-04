import sqlite3
from collections import OrderedDict

from orm.db import Field, db_conn


def value_formatter(value):
    if not value:
        return 'null'
    if isinstance(value, str):
        return repr(value)
    if isinstance(value, int):
        return str(value)


class BaseTable:
    __table_name__ = None
    id = Field(field_type='INTEGER', is_null=False, pk=True, auto_increment=True)

    @classmethod
    def __get_fields(cls) -> dict:
        fields = {field_name: value for field_name, value in cls.__dict__.items() if
                  not field_name.startswith('__')}
        fields['id'] = cls.id

        return fields

    @classmethod
    def __get_table_name(cls):
        # print('_'.join((cls.__name__.lower(), 'tbl')))
        return '_'.join((cls.__name__.lower(), 'tbl'))

    @classmethod
    def add(cls, conn=db_conn(), **kwargs):
        fields = ', '.join(kwargs.keys())
        values = ', '.join([value_formatter(value) for value in kwargs.values()])
        table_name = cls.__get_table_name()

        request = f'INSERT INTO {table_name}({fields}) VALUES({values});'
        print(request)

        try:
            conn.cursor().execute(request)
            conn.commit()
        except sqlite3.IntegrityError as e:
            print(f'Error: Unable to create record: {str(e)}')

    @classmethod
    def drop(cls, conn=db_conn()):
        table_name = cls.__get_table_name()

        request = f'DROP TABLE {table_name};'
        print(request)

        try:
            conn.cursor().execute(request)
        except sqlite3.OperationalError as e:
            print(f'Error: Unable to drop table {table_name}: {str(e)}')

    @classmethod
    def create(cls, conn=db_conn()):

        fields = []
        foreign_keys = []
        table_name = cls.__get_table_name()

        for field_name, field_params in cls.__get_fields().items():
            field_params_dict = OrderedDict(field_params.__dict__)

            field_params_dict['name'] = field_name
            field_params_dict.move_to_end('name', last=False)

            if 'foreign_key' in field_params_dict.keys():
                fk_class = field_params_dict.pop('foreign_key')
                fk_table = fk_class.__get_fk()
                field = [value for value in field_params_dict.values() if value]
                foreign_keys.append(f'FOREIGN KEY({field_params_dict["name"]}) REFERENCES {fk_table}')

            else:
                field = [value for value in field_params_dict.values() if value]
            fields.append(' '.join(field))

        fields += foreign_keys

        request = f'CREATE TABLE {table_name} ({", ".join(fields)});'
        print(request)

        try:
            conn.cursor().execute(request)
        except sqlite3.OperationalError as e:
            print(f'Error: Unable to create table {table_name}: {str(e)}')

    @classmethod
    def get(cls, **kwargs):
        pass
