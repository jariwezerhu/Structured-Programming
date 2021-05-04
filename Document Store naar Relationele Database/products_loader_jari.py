from pymongo import MongoClient
import psycopg2

client = MongoClient(port=27017)


def getConnection():  # https://www.postgresqltutorial.com/postgresql-python/connect/
    conn = psycopg2.connect(
        host="localhost",
        database="huwebshop",
        user="postgres",
        password="123")
    return conn


def insert(pr_id, brand, category, sub_category, sub_sub_category, sub_sub_sub_category, price, gender, fast_mover,
           herhaalaankopen, name, discount, doelgroep, conn):
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO products (id, brand, category, sub_category, sub_sub_category, sub_sub_sub_category, 
            price, gender, fast_mover, herhaalaankopen, name, discount, doelgroep) VALUES(%s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s)""", (pr_id, brand, category, sub_category, sub_sub_category, sub_sub_sub_category,
                                         price, gender, fast_mover, herhaalaankopen, name, discount, doelgroep))
        conn.commit()
    print("INSERTED ", pr_id, brand, category, sub_category, sub_sub_category, sub_sub_sub_category, price, gender,
          fast_mover,
          herhaalaankopen, name, discount, doelgroep)


with client:
    db = client.huwebshop

    products = db.products.find({}, {'_id': 1, 'name': 1, 'brand': 1, 'category': 1, 'sub_category': 1,
                                     'sub_sub_category': 1, 'sub_sub_sub_category': 1, 'preferences': 1, 'price': 1,
                                     'gender': 1, 'fast_mover': 1, 'herhaalaankopen': 1, 'properties': 1})

    for product in products:
        product_name = product['name']
        product_price = product['price']
        product_properties = product['properties']
        try:

            """ Alleen als een product een naam heeft, willen we het product inladen """

            if product_name:

                """ Hetzelfde geldt voor de selling_price. (We willen alleen de selling_price weten) """

                for price_type, price in product_price.items():
                    if price_type == 'selling_price':
                        if price:

                            """ Nu hebben we de juiste filters toegepast """
                            """ Uit properties nog de juiste data halen en alle product_data benoemen"""
                            for prop_type, value in product_properties.items():
                                if prop_type == 'discount':
                                    discount = value
                                if prop_type == 'doelgroep':
                                    doelgroep = value
                            pr_id = product['_id']
                            brand = product['brand']
                            category = product['category']
                            sub_category = product['sub_category']
                            sub_sub_category = product['sub_sub_category']
                            sub_sub_sub_category = product['sub_sub_sub_category']
                            gender = product['gender']
                            fast_mover = product['fast_mover']
                            herhaalaankopen = product['herhaalaankopen']

                            if not brand:
                                brand = 'NULL'
                            if not category:
                                category = 'NULL'
                            if not sub_category:
                                sub_category = 'NULL'
                            if not sub_sub_category:
                                sub_sub_category = 'NULL'
                            if not sub_sub_sub_category:
                                sub_sub_sub_category = 'NULL'
                            if not gender:
                                gender = 'NULL'
                            """ Product-data inladen """

                            insert(pr_id, brand, category, sub_category, sub_sub_category, sub_sub_sub_category, price,
                                   gender, fast_mover, herhaalaankopen, product_name, discount, doelgroep,
                                   getConnection())

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
