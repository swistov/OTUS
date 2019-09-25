from loguru import logger
from orm.db.database import Field
from orm.db.tables import BaseTable


class Curse(BaseTable):

    curse_name = Field(field_type='VARCHAR', is_null=True)


if __name__ == '__main__':
    logger.add('db.log',
               colorize=True,
               format="<green>{time}</green> <level>{message}</level>",
               rotation="5 MB",
               compression="zip",
               enqueue=True)
    # Init
    curse = Curse()

    # Create DB
    curse.create()

    # Drop DB
    curse.drop()

    # Add new line
    curse.add(curse_name='Python Django2')

    # Get line
    curse.get(curse_name='Python Django')
