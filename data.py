from datetime import datetime
from models import Restaurant, Review

def populate_db():
    one = Restaurant(
        name = "Mission Chinese Food",
        borough = "Manhattan",
        photograph = "/static/img/1.jpg",
        img_description = "An inside view of a busy restaurant with all tables ocupied by people enjoying their meal",
        address = "171 E Broadway, New York, NY 10002",
        latlng = [40.713829, -73.989667],
        cuisine = "Chinese",
        operating_hours = {
          "Monday": "5:30 pm - 11:00 pm",
          "Tuesday": "5:30 pm - 12:00 am",
          "Wednesday": "5:30 pm - 12:00 am",
          "Thursday": "5:30 pm - 12:00 am",
          "Friday": "5:30 pm - 12:00 am",
          "Saturday": "12:00 pm - 4:00 pm",
          "Sunday": "12:00 pm - 4:00 pm"
        })
    one.insert()

    one_review1 = Review(
        restaurant_id = 1,
        name = "Steve",
        date = datetime.today(),
        rating = 4,
        comments = "Mission Chinese Food has grown up from its scrappy Orchard Street days into a big, two story restaurant equipped with a pizza oven, a prime rib cart, and a much broader menu. Yes, it still has all the hits — the kung pao pastrami, the thrice cooked bacon —but chef/proprietor Danny Bowien and executive chef Angela Dimayuga have also added a raw bar, two generous family-style set menus, and showstoppers like duck baked in clay. And you can still get a lot of food without breaking the bank.")
    one_review1.insert()

    one_review2 = Review(
        restaurant_id = 1,
        name = "Morgan",
        date = datetime.today(),
        rating = 4,
        comments= "This place is a blast. Must orders: GREEN TEA NOODS, sounds gross (to me at least) but these were incredible!, Kung pao pastrami (but you already knew that), beef tartare was a fun appetizer that we decided to try, the spicy ma po tofu SUPER spicy but delicous, egg rolls and scallion pancake i could have passed on... I wish we would have gone with a larger group, so much more I would have liked to try!")
    one_review2.insert()

    one_review3 = Review(
        restaurant_id = 1,
        name = "Alba",
        date = datetime.today(),
        rating = 3,
        comments= "I was VERY excited to come here after seeing and hearing so many good things about this place. Having read much, I knew going into it that it was not going to be authentic Chinese. The place was edgy, had a punk rock throwback attitude, and generally delivered the desired atmosphere. Things went downhill from there though. The food was okay at best and the best qualities were easily overshadowed by what I believe to be poor decisions by the kitchen staff.")
    one_review3.insert()

    two = Restaurant(
        name = "Emily",
        borough = "Brooklyn",
        photograph = "/static/img/2.jpg",
        img_description = "A traditional margherita pizza",
        address = "919 Fulton St, Brooklyn, NY 11238",
        latlng = [40.683555, -73.966393],
        cuisine = "Italian",
        operating_hours = {
          "Monday": "5:30 pm - 11:00 pm",
          "Tuesday": "5:30 pm - 11:00 pm",
          "Wednesday": "5:30 pm - 11:00 pm",
          "Thursday": "5:30 pm - 11:00 pm",
          "Friday": "5:30 pm - 11:00 pm",
          "Saturday": "5:00 pm - 11:30 pm",
          "Sunday": "12:00 pm - 3:00 pm"
        })
    two.insert()

    two_review1 = Review(
        restaurant_id = 2,
        name = "Steph",
        date = datetime.today(),
        rating = 4,
        comments = "Five star food, two star atmosphere. I would definitely get takeout from this place - but dont think I have the energy to deal with the hipster ridiculousness again. By the time we left the wait was two hours long.")
    two_review1.insert()

    two_review2 = Review(
        restaurant_id = 2,
        name = "Steve",
        date = datetime.today(),
        rating = 4,
        comments = "This cozy Clinton Hill restaurant excels at both straightforward and unusual wood-fired pizzas. If you want a taste of the latter, consider ordering the Emily, which is topped with mozzarella, pistachios, truffled sottocenere cheese, and honey. The menu includes salads and a handful of starters, as well as a burger that some meat connoisseurs consider to be among the best in the city.")
    two_review2.insert()

    two_review3 = Review(
        restaurant_id = 2,
        name = "Sam",
        date = datetime.today(),
        rating = 5,
        comments = "5 star atmosphere as it is very cozy with great staff. 5 star food as their Emmy burger is outrageously good and its on a pretzel bun... Too juicy for its own good and downright addicting. Also try the Colony pizza. Many others looked like worth competitors, but the Colony really found its way to my heart. when you start with a great crust, top it with top notch cheese and sauce, you've got a winner. But, if you go a step further and add the salty from the pepperoni, the sweet from the honey, and the spicy from the chili oil.... your mouth is confused and happy at the same time.")
    two_review3.insert()

    three = Restaurant(
        name = "Kang Ho Dong Baekjeong",
        borough = "Manhattan",
        photograph = "/static/img/3.jpg",
        img_description = "An inside view of an empty restaurant. There is a steam pot in the middle of each table",
        address = "1 E 32nd St, New York, NY 10016",
        latlng = [40.747143, -73.985414],
        cuisine = "Korean",
        operating_hours = {
          "Monday": "11:30 am - 2:00 am",
          "Tuesday": "11:30 am - 2:00 am",
          "Wednesday": "11:30 am - 2:00 am",
          "Thursday": "11:30 am - 2:00 am",
          "Friday": "11:30 am - 6:00 am",
          "Saturday": "11:30 am - 6:00 am",
          "Sunday": "11:30 am - 2:00 am"
        })
    three.insert()

    three_review1 = Review(
        restaurant_id = 3,
        name = "Steve",
        date = datetime.today(),
        rating = 4,
        comments = "The tables at this 32nd Street favorite are outfitted with grills for cooking short ribs, brisket, beef tongue, rib eye, and pork jowl. The banchan plates are uniformly good, and Deuki Hong’s menu also includes winning dishes like stir-fried squid noodles, kimchi stew, and seafood pancakes. If it’s available, make sure to order the kimchi and rice “lunchbox.” Baekjeong is a great place for large groups and birthday parties.")
    three_review1.insert()

    three_review2 = Review(
        restaurant_id = 3,
        name = "ZS",
        date = datetime.today(),
        rating = 5,
        comments = "I've been to Korea before and many other Korean BBQ places. We had the regular pork belly and a beef (forgot which cut) and a seafood tofu soup. Two meat and a soup was just prefect for the two of us. We could have done one meat and one soup. The portions of the meat are great! The beef was juicy, tender and so good. The sides were excellent.")
    three_review2.insert()

    three_review3 = Review(
        restaurant_id = 3,
        name = "Emily",
        date = datetime.today(),
        rating = 2,
        comments = "MEH. I've tried their Jersey location as well but Kang Ho Dong meat quality is severely decreasing. A Korean bbq place with whatever meat? I think NOT!")
    three_review3.insert()

    four = Restaurant(
        name = "Katz's Delicatessen",
        borough = "Manhattan",
        photograph = "/static/img/4.jpg",
        img_description = "A night scene of people walking around the corner of a busy restaurant",
        address = "205 E Houston St, New York, NY 10002",
        latlng = [40.722216, -73.987501],
        cuisine = "American",
        operating_hours = {
          "Monday": "8:00 am - 10:30 pm",
          "Tuesday": "8:00 am - 10:30 pm",
          "Wednesday": "8:00 am - 10:30 pm",
          "Thursday": "8:00 am - 2:30 am",
          "Friday": "8:00 am - Sat",
          "Saturday": "Open 24 hours",
          "Sunday": "Sat - 10:30 pm"
        })
    four.insert()

    five = Restaurant(
        name = "Roberta's Pizza",
        borough = "Brooklyn",
        photograph = "/static/img/5.jpg",
        img_description = "An inside view of a relax and busy restaurant with a kitchen bar at the back",
        address = "261 Moore St, Brooklyn, NY 11206",
        latlng = [40.705089, -73.933585],
        cuisine = "Italian",
        operating_hours = {
          "Monday": "11:00 am - 12:00 am",
          "Tuesday": "11:00 am - 12:00 am",
          "Wednesday": "11:00 am - 12:00 am",
          "Thursday": "11:00 am - 12:00 am",
          "Friday": "11:00 am - 12:00 am",
          "Saturday": "10:00 am - 12:00 am",
          "Sunday": "10:00 am - 12:00 am"
        })
    five.insert()

    five_review1 = Review(
        restaurant_id = 5,
        name = "Maria",
        date = datetime.today(),
        rating = 4,
        comments = "Roberta's is the epicenter of the modern Brooklyn food scene.The pizzas are fantastic, but the restaurant really flexes its muscles with the vegetable dishes. In addition to the pies, consider ordering the radishes, the romaine salad, the roasted beets, and some of the charcuterie.")
    five_review1.insert()

    five_review2 = Review(
        restaurant_id = 5,
        name = "Raymond",
        date = datetime.today(),
        rating = 4,
        comments = "Roberta's, one of the best pizzas I have had in my life. Very trendy and hipsterish spot. Came here for lunch on a random weekday afternoon and when we arrived, there was a line forming already. The space is a bit cramped. You'll get to know your neighbors soon enough. The pizza is just delightful and delicious. It's a ncie plus that you get to see them firing up the pizzas in the corner. The major issue with Roberta's is the trek out to the Williamsburg/Bushwick.")
    five_review2.insert()

    six = Restaurant(
        name = "Casa Enrique",
        borough = "Queens",
        photograph = "/static/img/10.jpg",
        img_description = "An inside view of an empty restaurant with a big bar and stools",
        address = "5-48 49th Ave, Queens, NY 11101",
        latlng = [40.743394, -73.954235],
        cuisine = "Mexican",
        operating_hours = {
          "Monday": "5:00 pm - 12:00 am",
          "Tuesday": "5:00 pm - 12:00 am",
          "Wednesday": "5:00 pm - 12:00 am",
          "Thursday": "5:00 pm - 12:00 am",
          "Friday": "5:00 pm - 12:00 am",
          "Saturday": "11:00 am - 12:00 am",
          "Sunday": "11:00 am - 12:00 am"
        })
    six.insert()

    six_review1 = Review(
        restaurant_id = 6,
        name = "Sandra",
        date = datetime.today(),
        rating = 5,
        comments = "Head to this laid-back Long Island City restaurant for beef tongue tacos, chicken smothered in a heady mole sauce, and a monster crab tostada. New York's only Michelin-starred Mexican restaurant is an especially cool choice for lunch during the week or drinks after work. Eater critic Ryan Sutton awarded this restaurant two stars.")
    six_review1.insert()
