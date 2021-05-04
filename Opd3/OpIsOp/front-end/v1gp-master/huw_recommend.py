from flask import Flask
from flask_restful import Api, Resource
from pymongo import MongoClient
from dotenv import load_dotenv
import random
import psycopg2

app = Flask(__name__)
api = Api(app)

# Establishing connections to MongoDB and Postgresql

load_dotenv()

# MongoDB connection (edit address/port if necessary)
client = MongoClient(port=27017)
mongoDatabase = client.huwebshop

# PostgreSQL connection (edit variables if necessary)
postgresDatabase = psycopg2.connect("dbname=postgres user=postgres password=123")
cursor = postgresDatabase.cursor()

# Fetches the subsubcategory from a certain product
subsubcategory_query = """
        SELECT id
        FROM products
        WHERE subsubcategory = %s
        """

# Fetches the subcategory from a certain product
subcategory_query = """
        SELECT id
        FROM products
        WHERE subcategory = %s
        """

# Fetches the category from a certain product
category_query = """
        SELECT id
        FROM products
        WHERE category = %s
        """


def category_fetch(product_id):
    """ This function takes the product_id from the current page, and finds its subsubcategory, subcategory and
    category """

    # Finds out which subsubcategory, subcategory and category the product belongs to and adds them to cat_list
    query = """
    SELECT category, subcategory, subsubcategory
    FROM products
    WHERE id = %s;
    """
    cursor.execute(query, (product_id,))
    cat_list = cursor.fetchall()

    # It's a nested list

    cat_list = cat_list[0]

    return cat_list


def content_recommendation(lst):
    """ This is the content-filtering recommendation engine. This recommendation engine will look up the lowest possible
 category of a clicked product, and recommend products from its corresponding sub_sub_category, sub_category,
 and category, IF available """

    recommendations = []

    while len(recommendations) < 4:

        # If there are subsubcategory, subcategory and category
        if lst[2] and lst[1] and lst[0]:
            # Adds 2 random products from subsub
            cursor.execute(subsubcategory_query, (lst[2],))
            product_list = cursor.fetchall()
            product_list = random.sample(product_list, 2)
            for i in product_list:
                recommendations.append(i[0])
            # Adds a random products from sub
            cursor.execute(subcategory_query, (lst[1],))
            product_list = cursor.fetchall()
            product_list = random.sample(product_list, 1)
            for i in product_list:
                recommendations.append(i[0])
            # Adds a random product from category
            cursor.execute(category_query, (lst[0],))
            product_list = cursor.fetchall()
            product_list = random.sample(product_list, 1)
            for i in product_list:
                recommendations.append(i[0])

        # If there are only subcategory and category
        elif lst[1] and lst[0]:
            # Adds 3 random products from sub
            cursor.execute(subcategory_query, (lst[1],))
            product_list = cursor.fetchall()
            product_list = random.sample(product_list, 3)
            for i in product_list:
                recommendations.append(i[0])
            # Adds a random product from category
            cursor.execute(category_query, (lst[0],))
            product_list = cursor.fetchall()
            product_list = random.sample(product_list, 1)
            for i in product_list:
                recommendations.append(i[0])

        # If there is only category
        elif lst[0]:
            # Adds 4 random product from category
            cursor.execute(category_query, (lst[0],))
            product_list = cursor.fetchall()
            product_list = random.sample(product_list, 4)
            for i in product_list:
                recommendations.append(i[0])

        # Else we break and return nothing
        else:
            break

    return recommendations


def collaborative_recommendation(product_id):
    """ This is the collaborative-filtering recommendation engine. This recommendation engine will fetch every
    profile that viewed a certain product before in the WHERE line, and uses that information to get every product
    those profiles clicked on before """

    recommendations = []

    query = """
    SELECT prodid, count(prodid)
    FROM profiles_previously_viewed
    WHERE profid IN(SELECT profid FROM profiles_previously_viewed WHERE profiles_previously_viewed.prodid = %s)
    GROUP BY prodid
    ORDER BY count DESC LIMIT 11
    """

    cursor.execute(query, (product_id,))
    prod_list = cursor.fetchall()

    # Create the list of products most viewed by other profiles that also clicked current product
    for i in prod_list:
        recommendations.append((i[0]))

    # Select 4 random products from the top 10 list, but first remove the clicked product
    if recommendations:
        recommendations.remove(product_id)
        recommendations = random.sample(recommendations, 4)

    return recommendations


class Recom(Resource):

    def get(self, profile_id, count, product_id, page):
        """ This function represents the handler for GET requests coming in through the API. It gets the product_id
        and profile_id from the currently displayed product and user respectively, which is required for searching
        our postgreSQL database. It also gets a page parameter, which we need to figure out on what page we are,
        thus what type of recommendation we want to call """

        if page == 'product_details':

            # First we try getting product recommendations with our Collaborative-Filter
            recommendations = collaborative_recommendation(product_id)
            if recommendations:
                print("Collaborative-Filter successfully applied")

            # If we have NO Collaborative-Filter recommendations to offer, because no one has previously viewed the
            # product, we try the Content-Filter
            if not recommendations:
                recommendations = content_recommendation(category_fetch(product_id))
                if recommendations:
                    print("Content-Filter successfully applied")

            mongo_cursor = mongoDatabase.products.find({'_id': {'$in': recommendations}})
            prodids = list(map(lambda x: x['_id'], list(mongo_cursor)))

        else:

            randcursor = mongoDatabase.products.aggregate([{'$sample': {'size': count}}])
            prodids = list(map(lambda x: x['_id'], list(randcursor)))

        return prodids


# This method binds the Recom class to the REST API, to parse specifically
# requests in the format described below
api.add_resource(Recom, "/<string:profile_id>/<int:count>/<string:product_id>/<string:page>")
