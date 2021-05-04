import psycopg2

connection = psycopg2.connect("dbname=huwebshop user=postgres password=123")

cursor = connection.cursor()

# Als de tabel al bestaat wordt deze verwijderd

cursor.execute("DROP TABLE IF EXISTS products CASCADE")
cursor.execute("DROP TABLE IF EXISTS viewed_before CASCADE")
cursor.execute("DROP TABLE IF EXISTS orders CASCADE")
cursor.execute("DROP TABLE IF EXISTS buids CASCADE")
cursor.execute("DROP TABLE IF EXISTS profiles CASCADE")
cursor.execute("DROP TABLE IF EXISTS sessions CASCADE")

# Nu worden de tabellen aangemaakt met hun kolommen

# Products

cursor.execute("""CREATE TABLE products
                (id VARCHAR PRIMARY KEY,
                 brand VARCHAR,
                 category VARCHAR,
                 subcategory VARCHAR,
                 sub_subcategory VARCHAR,
                 gender VARCHAR,
                 price INTEGER,
                 fast_mover BOOLEAN,
                 repeat_purchase BOOLEAN,
                 name VARCHAR,
                 discount VARCHAR,
                 targeted VARCHAR
                 );""")

# Buids

cursor.execute("""CREATE TABLE buids
                (buid VARCHAR PRIMARY KEY
                 );""")

# Profiles

cursor.execute("""CREATE TABLE profiles
                (id VARCHAR PRIMARY KEY,
                 buid VARCHAR,
                 segment VARCHAR,
                 FOREIGN KEY (buid) REFERENCES buids (buid)
                 );""")

# Sessions

cursor.execute("""CREATE TABLE sessions
                (id VARCHAR PRIMARY KEY,
                 buid VARCHAR,
                 segment VARCHAR,
                 FOREIGN KEY (buid) REFERENCES buids (buid)
                 );""")

# Orders

cursor.execute("""CREATE TABLE orders
                (buid VARCHAR,
                 product_id VARCHAR,
                 FOREIGN KEY (buid) REFERENCES buids (buid),
                 FOREIGN KEY (product_id) REFERENCES products (id)
                 );""")

# Viewed_before

cursor.execute("""CREATE TABLE viewed_before
                (product_id VARCHAR,
                 profile_id VARCHAR,
                 FOREIGN KEY (product_id) REFERENCES products (id),
                 FOREIGN KEY (profile_id) REFERENCES profiles (id)
                 );""")

connection.commit()
cursor.close()
connection.close()
