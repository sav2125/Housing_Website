# Housing_Website

Developed a Housing website using Flask Framework in which we have used tables that were created and then populated using 
PostgreSQL. We have covered all the entities. We implemented a system which has 2 views. One is a buyer, the other is a seller.
Buyer and seller login the application. If they are new their information is added to the database. After logging in a buyer 
has the option to buy the listed properties. We have provided a feature of adding to cart as well where buyer can see his 
favourite properties. A buyer can delete from the cart as well. We have provided the functionality of filters where user can 
look for his dream apartment by setting the property features. A seller can view his sold and unsold properties. He can also 
add new properties. 

Page 1: Buyer
This page allows the buyer to view all the listed properties and buy the property. One of the interesting feature on the page 
is the hot properties. Hot Properties: Properties which had the utilities of washing machine and heating enabled were grouped 
by city and only those properties were considered which had price less than the average price for a particular city. These 
properties are hot properties in their city since they have the utilities and their price is comparatively lower. These 
properties along with their owner information is displayed. Second interesting feature is the star sellers.
Star Seller: Information of all the sellers whose properties have been sold more than the average number of properties sold by
a seller.

Page 2: Seller
This page allows seller to view his sold and unsold properties as well as add properties..
Interesting property : Seller can also insert a new property to the application. While showing
the sold properties, we join the tables property_owned, transaction, payment to show the
properties.
