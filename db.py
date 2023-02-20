import os
from hashlib import sha3_512

def hash_password(password):
    return sha3_512(password.encode("utf-8")).hexdigest()

def populate_test_database():
    from models import User ,Product, products_db

    products_db.create_tables([Product, User])
    Product.create(name="Aero Bubbly", description="Some description", pack=["PP","foil"])
    Product.create(name="Cadbury Mini Eggs", description="Some description", pack=["soft plastic packaging"])
    Product.create(name="Coffee Cup", description="Some description", pack=["paper"])
    Product.create(name="Tissue", description="Some description", pack=["paper"])
    Product.create(name="Propercorn", description="Some description", pack=["matte foil"])
    Product.create(name="Kettel Vegetable Chips", description="Some description", pack=["foil and LDPE"])
    Product.create(name="Oreo Cookies", description="Some description", pack=["plastic GRADE 7"])
    Product.create(name="Mars Duo", description="Some description", pack=["PP","foil"])

    hashed_password = hash_password("SamIsthebestBrotherEver")

    User.create(name="ana@anasemail.com", password=hashed_password)





if not os.path.isfile(os.path.join(os.getcwd(), os.path.basename("Products.db"))):
    populate_test_database()
