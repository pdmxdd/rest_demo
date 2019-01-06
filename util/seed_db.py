from application_configuration.app_config import db
from models.dog import Dog


def create():
    db.create_all()
    print("Tables created")
    db.session.add(Dog(name="Bernie", age="3"))
    db.session.add(Dog(name="Simon", age="4"))
    db.session.add(Dog(name="Lily", age="10"))

    db.session.commit()
    print("3 dogs added to table dog")


def drop_create():
    db.drop_all()
    print("Tables dropped")
    create()

if __name__ == "__main__":
    drop_create()
