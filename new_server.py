#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
import datetime

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of:
#
#     postgresql://USER:PASSWORD@w4111a.eastus.cloudapp.azure.com/proj1part2
#

# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@w4111a.eastus.cloudapp.azure.com/proj1part2"



#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

buyer_id = 0
seller_id = 0
property_id = 0
#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
engine.execute("""CREATE TABLE IF NOT EXISTS test2 (
  id serial,
  name text
);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
#
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args


  # example of a database query
  #

  #important code
  cursor = g.conn.execute("SELECT name FROM buyer_copy")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #
  #     # creates a <div> tag for each element in data
  #     # will print:
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
#
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/another')
def another():
  return render_template("another.html")


@app.route('/buyer')
def buyer():
  #print "Here"
  return render_template("buyer.html")

@app.route('/property')
def property():
  #print "Here"
  cursor = g.conn.execute(" SELECT PROP.property_left_id, PROP.type, PROP.location, PROP.price, S1.name, S1.email,S1.seller_rating FROM (SELECT * FROM property_left_copy PL3 WHERE PL3.property_left_id IN (SELECT PL2.property_left_id FROM (SELECT PL.location, avg(PL.price) AS avg_price FROM property_left_copy PL WHERE washing_machine = 'yes' AND heating = 'yes' GROUP BY PL.location) AS Average JOIN property_left_copy PL2 ON Average.location = PL2.location WHERE PL2.price < Average.avg_price)) AS PROP, property_owned_copy O1, seller_copy S1 WHERE PROP.property_left_id = O1.property_id AND O1.seller_id = S1.seller_id")
  cursor2 = g.conn.execute("SELECT * FROM property_left_copy")
  cursor3 = g.conn.execute("SELECT * from seller_copy S2 where S2.seller_id IN (SELECT S1.seller_id FROM seller_copy S1 JOIN transaction_copy T1 ON S1.seller_id = T1.seller_id GROUP BY S1.seller_id HAVING count(*) > (SELECT avg(cnt) FROM (SELECT S.seller_id, S.name, count(*) AS cnt FROM seller_copy S JOIN transaction_copy T ON S.seller_id = T.seller_id GROUP BY S.seller_id, S.name) ONE))")
  print "Hello"
  tuples = []
  tuples2 = []
  tuples3 = []
  for result in cursor:
      tuples.append(result)
      #tuples_id.append(result['property_left_id'])

  for result in cursor2:
      tuples2.append(result)
  for result in cursor3:
      tuples3.append(result)
  cursor.close()
  cursor2.close()
  cursor3.close()
  context = dict(data = tuples, data2 = tuples2, data3 = tuples3)
  return render_template("property.html", **context)


@app.route('/filterproperty', methods=['POST'])
def filterproperty():
  #print "Here"
  location = request.form['location']
  propertytype = request.form['propertytype']
  washing = request.form['washing']
  pets = request.form['pets']
  heating = request.form['heating']
  water = request.form['water']

  cursor = g.conn.execute(" SELECT PROP.property_left_id, PROP.type, PROP.location, PROP.price, S1.name, S1.email,S1.seller_rating FROM (SELECT * FROM property_left_copy PL3 WHERE PL3.property_left_id IN (SELECT PL2.property_left_id FROM (SELECT PL.location, avg(PL.price) AS avg_price FROM property_left_copy PL WHERE washing_machine = 'yes' AND heating = 'yes' GROUP BY PL.location) AS Average JOIN property_left_copy PL2 ON Average.location = PL2.location WHERE PL2.price < Average.avg_price)) AS PROP, property_owned_copy O1, seller_copy S1 WHERE PROP.property_left_id = O1.property_id AND O1.seller_id = S1.seller_id")
  cursor2 = g.conn.execute("SELECT * FROM property_left_copy WHERE location = '"+ location +"' and type='"+ propertytype +"' and washing_machine = '"+ washing +"' and pets_allowed = '"+ pets +"' and heating = '"+ heating +"' and hot_water = '"+ water +"' ")
  cursor3 = g.conn.execute("SELECT * from seller_copy S2 where S2.seller_id IN (SELECT S1.seller_id FROM seller_copy S1 JOIN transaction_copy T1 ON S1.seller_id = T1.seller_id GROUP BY S1.seller_id HAVING count(*) > (SELECT avg(cnt) FROM (SELECT S.seller_id, S.name, count(*) AS cnt FROM seller_copy S JOIN transaction_copy T ON S.seller_id = T.seller_id GROUP BY S.seller_id, S.name) ONE))")
  tuples = []
  tuples2 = []
  tuples3 = []
  for result in cursor:
      tuples.append(result)

  for result in cursor2:
      tuples2.append(result)

  for result in cursor3:
      tuples3.append(result)
  cursor.close()
  cursor2.close()
  cursor3.close()
  context = dict(data = tuples, data2 = tuples2, data3 = tuples3)
  return render_template("property.html", **context)

@app.route('/listproperty')
def listproperty():
  global seller_id;
  seller_id = unicode(str(seller_id), "utf-8")
  cursor = g.conn.execute("Select type,price,location,washing_machine,pets_allowed,heating,hot_water from property_left_copy p JOIN property_owned_copy o ON p.property_left_id = o.property_id where o.seller_id = "+seller_id)
  cursor2 = g.conn.execute("Select  ONE.date, ONE.type, ONE.price, ONE.location, P.type AS payment_type, P.currency from (select * from transaction_copy T join property_sold_copy S ON T.property_sold_id = S.property_sold_id where T.seller_id = "+ seller_id +") AS ONE JOIN payment_copy P ON ONE.payment_id = P.payment_id;")
  tuples = []
  tuples2 = []
  for result in cursor:
      tuples.append(result)
  for result in cursor2:
      tuples2.append(result)
  cursor.close()
  cursor2.close()
  context = dict(data = tuples, data2=tuples2)

  return render_template("addproperty.html", **context)




@app.route('/addproperty', methods=['POST'])
def addproperty():
  location = request.form['location']
  price = request.form['price']
  propertytype = request.form['propertytype']
  washing = request.form['washing']
  pets = request.form['pets']
  heating = request.form['heating']
  water = request.form['water']
  print location,price,propertytype,water
  #print email,address,creditscore,income
  #g.conn.execute("INSERT INTO buyer_copy VALUES (, '" + name + "')")
  cursor = g.conn.execute("SELECT count(*) from property_copy")
  for result in cursor:
      pkey = result['count']
  cursor.close()
  pkey = pkey + 1
  global seller_id
  pkey = unicode(str(pkey), "utf-8")
  price = unicode(str(price), "utf-8")
  seller_id = unicode(str(seller_id), "utf-8")
  g.conn.execute("INSERT INTO property_copy VALUES (" + pkey + ", '" + propertytype + "', " + price + ", '" + location + "','" + washing + "', '" + pets + "', '" + heating + "','" + water + "')")
  g.conn.execute("INSERT INTO property_left_copy VALUES (" + pkey + ", '" + propertytype + "', " + price + ", '" + location + "','" + washing + "', '" + pets + "', '" + heating + "','" + water + "')")
  g.conn.execute("INSERT INTO property_owned_copy VALUES (" + seller_id + "," + pkey + ")")
  return redirect('/listproperty')


@app.route('/seller')
def seller():
  return render_template("seller.html")

# Example of adding new data to the database
@app.route('/newbuyer', methods=['POST'])
def newbuyer():
  name = request.form['name']
  email = request.form['email']
  address = request.form['address']
  creditscore = request.form['creditscore']
  income = request.form['income']
  print type(income)
  #print email,address,creditscore,income
  #g.conn.execute("INSERT INTO buyer_copy VALUES (, '" + name + "')")
  cursor = g.conn.execute("SELECT count(*) from buyer_copy")
  for result in cursor:
      pkey = result['count']
  cursor.close()
  pkey = pkey + 1
  global buyer_id
  # print pkey
  # print type(pkey)
  pkey = unicode(str(pkey), "utf-8")
  g.conn.execute("INSERT INTO buyer_copy VALUES (" + pkey + ", '" + name + "', '" + email + "', '" + address + "', " + creditscore + "," + income + ")")
  buyer_id = pkey
  return redirect('/property')

@app.route('/existingbuyer', methods=['POST'])
def existingbuyer():
  print "existingbuyer"
  email = request.form['email']
  print email
  cursor = g.conn.execute("SELECT buyer_id, email FROM buyer_copy where email = '" + email + "'")
  emails = []
  id_array = []
  for result in cursor:
    emails.append(result['email'])  # can also be accessed using result[0]
    id_array.append(result['buyer_id'])
  cursor.close()
  print emails
  print id_array
  global buyer_id
  if len(emails) == 1:
    buyer_id = id_array[0]
    print buyer_id
    return redirect('/property')
  else:
    return redirect('/buyer')

@app.route('/newseller', methods=['POST'])
def newseller():
  name = request.form['name']
  email = request.form['email']
  address = request.form['address']
  #print email,address,creditscore,income
  #g.conn.execute("INSERT INTO buyer_copy VALUES (, '" + name + "')")
  cursor = g.conn.execute("SELECT count(*) from seller_copy")
  for result in cursor:
      pkey = result['count']
  cursor.close()
  pkey = pkey + 1
  # print pkey
  # print type(pkey)
  pkey = unicode(str(pkey), "utf-8")
  global seller_id
  g.conn.execute("INSERT INTO seller_copy VALUES (" + pkey + ", '" + name + "', '" + email + "', '" + address + "', 1)")
  seller_id = pkey
  return redirect('/listproperty')


@app.route('/existingseller', methods=['POST'])
def existingseller():
  print "existingseller"
  email = request.form['email']
  print email
  cursor = g.conn.execute("SELECT seller_id, email FROM seller_copy where email = '" + email + "'")
  emails = []
  id_array = []
  for result in cursor:
    emails.append(result['email'])  # can also be accessed using result[0]
    id_array.append(result['seller_id'])
  cursor.close()
  print emails
  print id_array
  global seller_id
  if len(emails) == 1:
    seller_id = id_array[0]
    print seller_id
    return redirect('/listproperty')
  else:
    return redirect('/seller')

@app.route('/loancompany')
def loancompany():
  #print "Here"

  tuples = []
  tuples2 = []
  cursor2 = g.conn.execute("SELECT * FROM loan_company_copy L3 WHERE L3.company_id IN (SELECT ONE.company_id FROM (SELECT L1.company_id FROM loan_company_copy L1 WHERE L1.rate_of_interest < (SELECT avg(rate_of_interest) FROM loan_company_copy) AND L1.rating > (SELECT avg(rating) FROM loan_company_copy)) ONE JOIN loan_transaction_copy L2 ON ONE.company_id = L2.company_id GROUP BY ONE.company_id HAVING count(*) > (SELECT avg(cnt) FROM (SELECT ONE.company_id, count(*) AS cnt FROM (SELECT L1.company_id FROM loan_company_copy L1 WHERE L1.rate_of_interest < (SELECT avg(rate_of_interest) FROM loan_company_copy) AND L1.rating > (SELECT avg(rating) FROM loan_company_copy)) ONE JOIN loan_transaction_copy L2 ON ONE.company_id = L2.company_id GROUP BY ONE.company_id) AS TWO))")
  cursor = g.conn.execute("SELECT * from loan_company_copy")
  for result in cursor2:
    tuples2.append(result)
  for result in cursor:
    tuples.append(result)
  cursor2.close()
  cursor.close()
  context = dict(data=tuples, data2=tuples2)
  return render_template("loancompany.html", **context)

@app.route('/buyproperty', methods=['POST'])
def buyproperty():
  prop_id = request.form['clicked']
  global property_id
  property_id = prop_id
  property_id = unicode(str(property_id), "utf-8")
  return redirect('/currency')

@app.route('/addcart', methods=['POST'])
def addcart():
  prop_id = request.form['clicked']
  global property_id
  property_id = prop_id
  property_id = unicode(str(property_id), "utf-8")
  print property_id
  global buyer_id
  buyer_id = unicode(str(buyer_id), "utf-8")
  print buyer_id
  g.conn.execute(" INSERT INTO add_cart_copy VALUES(" + buyer_id + ", " + property_id + " ) ")
  print "done"
  return redirect('/property')


@app.route('/cart')
def cart():
    tuples = []
    global buyer_id
    buyer_id = unicode(str(buyer_id), "utf-8")
    cursor = g.conn.execute(" SELECT property_id, type, price, location, washing_machine, pets_allowed, heating, hot_water from add_cart_copy c JOIN property_copy p ON c.property_left_id = p.property_id where c.buyer_id = " + buyer_id)
    for result in cursor:
        tuples.append(result)
    cursor.close()
    context = dict(data=tuples)
    print tuples
    return render_template("cart.html", **context)





@app.route('/currency')
def currency():
  return render_template("currency.html")

@app.route('/finalbuy', methods=['POST'])
def finalbuy():
  mode = request.form['paymentmode']
  currency = request.form['currency']
  tuples = []
  global property_id
  global buyer_id
  print "Buyer "
  print buyer_id
  property_id = unicode(str(property_id), "utf-8")
  cursor3 = g.conn.execute("SELECT seller_id from property_owned_copy where property_id = " + property_id)
  s_id = []
  for result in cursor3:
      s_id.append(result['seller_id'])
  seller = unicode(str(s_id[0]), "utf-8")
  date_trans= datetime.date.today()
  print type(datetime.date.today())
  cursor3.close()


  cursor = g.conn.execute("SELECT price from property_left_copy where property_left_id = " + property_id)
  price = []
  for result in cursor:
      price.append(result['price'])
  final_price = unicode(str(price[0]), "utf-8")
  cursor.close()

  cursor2 = g.conn.execute("SELECT count(*) from payment_copy")
  for result in cursor2:
      pkey = result['count']
  cursor2.close()
  pkey = pkey + 1

  cursor4 = g.conn.execute("SELECT count(*) from transaction_copy")
  for result in cursor4:
      pkey1 = result['count']
  cursor4.close()
  pkey1 = pkey1 + 1
  # print pkey
  # print type(pkey)
  pkey = unicode(str(pkey), "utf-8")
  pkey1 = unicode(str(pkey1), "utf-8")
  buyer_id = unicode(str(buyer_id), "utf-8")
  date_trans = unicode(str(date_trans), "utf-8")
  g.conn.execute("INSERT INTO transaction_copy VALUES("+ pkey1 +", '"+ date_trans +"',"+ buyer_id +"," + seller + "," + pkey + ","+ property_id +")")
  g.conn.execute("INSERT INTO payment_copy VALUES(" + pkey + ", '" + mode + "', '" + currency + "', " + final_price + ")")

  g.conn.execute("INSERT INTO property_sold_copy (property_sold_id,type,price,location,washing_machine,pets_allowed,heating,hot_water) SELECT * FROM property_left_copy where property_left_id = " + property_id)

  g.conn.execute("DELETE FROM property_left_copy where property_left_id = " + property_id)
  print "done"
  return redirect('/property')

@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  print name
  g.conn.execute("INSERT INTO test2 VALUES (, '" + name + "')")
  return redirect('/')


@app.route('/removecart',methods=['POST'])
def removecart():
    print "hello"
    prop_id = request.form['clicked']
    global property_id
    property_id = prop_id
    property_id = unicode(str(property_id), "utf-8")
    print property_id
    global buyer_id
    buyer_id = unicode(str(buyer_id), "utf-8")
    print buyer_id
    g.conn.execute(" DELETE FROM add_cart_copy where buyer_id = " + buyer_id + " and property_left_id = " + property_id )
    print "done"
    return redirect('/cart')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8000, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
