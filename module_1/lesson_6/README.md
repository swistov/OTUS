#### Create Table 
    from orm.db import BaseTable
    
    class Curse(BaseTable):
        curse_name = Field(field_type='VARCHAR', is_null=True)

#### Init DB
    curse = Curse()

#### Create DB
    curse.create()

#### Drop DB
    curse.drop()

#### Add new line
    curse.add(curse_name='Python Django2')

#### Get line
    curse.get(curse_name='Python Django')
