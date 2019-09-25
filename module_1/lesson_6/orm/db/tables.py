import sqlite3
from collections import OrderedDict, defaultdict
from loguru import logger
from orm.db import Field, db_conn, sql_select_as


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
    def __get_object_from_sql(cls, attrs: dict):
        obj_dict = defaultdict(dict)

        for table__field, value in attrs.items():
            table_name, field_name = table__field.split('__')

            if table_name == cls.__get_table_name():
                obj_dict[field_name] = value
            else:
                model_name = table_name.replace('_tbl', '')
                model_to_model = '__'.join((cls.__name__.lower(), model_name))
                obj_dict[model_to_model].update({field_name: value})

        return cls(**obj_dict)

    @classmethod
    def __get_table_name(cls):
        return '_'.join((cls.__name__.lower(), 'tbl'))

    @classmethod
    def __get_relations(cls):
        """
        :return: [(field_name, model),(field_name, model)]
        """
        connections = []
        for name, field in cls.__get_fields().items():
            if 'foreign_key' in field.__dict__.keys():
                connections.append((name, field.__dict__['foreign_key']))
        return connections

    @classmethod
    def __db_getter(cls, connection=CONNECTION, **kwargs):

        only_fields_list = kwargs.get('only', None)
        kwargs.pop('only', None)

        request_type = kwargs.get('request_type')
        kwargs.pop('request_type', None)

        from_table = cls.__get_table_name()

        connection.row_factory = Row

        connected_models = cls.__get_relations()

        if only_fields_list:
            fields = sql_select_as(from_table, only_fields_list)
        else:
            if connected_models:
                to_tables = [model.__get_table_name() for _, model in connected_models]

                from_fields = [name for name, _ in connected_models]
                joined_from = ['.'.join(i) for i in list(zip([from_table] * len(from_fields), from_fields))]

                to_fields = ['id'] * len(connected_models)
                joined_to = ['.'.join(i) for i in list(zip(to_tables, to_fields))]

                joins = f'{from_table}'

                for x in range(len(to_tables)):
                    joins += f' LEFT JOIN {to_tables[x]} ON {joined_from[x]}={joined_to[x]}'

                self_fields = list(cls.__get_fields().keys())
                fields = [sql_select_as(from_table, self_fields)]

                for _, model in cls.__get_relations():
                    foreign_table_name = model.__get_table_name()
                    foreign_table_fields = list(model.__get_fields().keys())
                    fields += [sql_select_as(foreign_table_name, foreign_table_fields)]

                fields = ' ,'.join(fields)

            else:
                self_fields = list(cls.__get_fields().keys())
                fields = sql_select_as(from_table, self_fields)

        if request_type == 'all':
            if connected_models and not only_fields_list:
                request = f'SELECT {fields} FROM {joins};'
            else:
                request = f'SELECT {fields} FROM {from_table};'

        else:
            conditions = ' AND '.join(
                ['='.join(('.'.join((from_table, str(k))), repr(v) if isinstance(v, str) else str(v)))
                 for k, v in kwargs.items()]
            )

            if connected_models and not only_fields_list:
                request = f'SELECT {fields} FROM {joins} WHERE {conditions};'
            else:
                request = f'SELECT {fields} FROM {from_table} WHERE {conditions};'

        if request_type == 'one':
            try:
                all_records = connection.cursor().execute(request).fetchall()
            except OperationalError as e:
                logger.error('Unable to get: {}', str(e))
                return None

            if len(all_records) > 1:
                logger.error('Unable to get record: more than one found')
                return None
            elif not all_records:
                logger.warning('DB clean. Raw not found')
                return None

            attrs = dict(connection.cursor().execute(request).fetchone())

            return cls.__get_object_from_sql(attrs)

        try:
            rows = connection.cursor().execute(request).fetchall()
        except OperationalError as e:
            logger.error('Unable to get: {}', str(e))
            return None

        if rows:
            return [cls.__get_object_from_sql(dict(row)) for row in rows]

        return None

    @classmethod
    def add(cls, conn=db_conn(), **kwargs):
        fields = ', '.join(kwargs.keys())
        values = ', '.join([value_formatter(value) for value in kwargs.values()])
        table_name = cls.__get_table_name()

        request = f'INSERT INTO {table_name}({fields}) VALUES({values});'

        try:
            conn.cursor().execute(request)
            conn.commit()
            logger.debug('New record "{}"', request)
        except sqlite3.IntegrityError as e:
            logger.error('Error: Unable to create record: {}', str(e))

    @classmethod
    def drop(cls, conn=db_conn()):
        table_name = cls.__get_table_name()

        request = f'DROP TABLE {table_name};'

        try:
            conn.cursor().execute(request)
            logger.debug('Drop table. Request: "{}"', request)
        except sqlite3.OperationalError as e:
            logger.error('Error: Unable to drop table {}: {}', table_name, str(e))

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

        try:
            conn.cursor().execute(request)
            logger.info('Add new table. Request: "{}"', request)
        except sqlite3.OperationalError as e:
            logger.error('Error: Unable to create table {}: {}', table_name, str(e))

    @classmethod
    def get(cls, **kwargs):

        kwargs.update(request_type='one')
        return cls.__db_getter(**kwargs)
