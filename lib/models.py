from sqlalchemy import String, Integer, ForeignKey, Column, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    price = Column(Integer())

    reviews = relationship('Review', backref='restaurant')
    customers = relationship ('Customer', secondary='reviews', back_populates='restaurants')


    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()
    
    def all_reviews(self):
        all_review_list = []
        for review in self.reviews:
            customer_name = f"Name:{review.customer}, {review.customer.last_name}"
            string_review = f"Review for {self.name} by {customer_name}: {review.rating} stars."
            all_review_list.append(string_review)

        return all_review_list

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    reviews = relationship('Review', backref='customer') 
    restaurants = relationship('Restaurant', secondary='reviews', back_populates='customers')

    def full_name(self):
        return f"First Name:{self.first_name} Last Name:{self.last_name}"
    
    def favorite_restaurant(self):
        max_rating = 0
        favorite_restaurant = None
        for review in self.reviews:
            if review.rating > max_rating:
                max_rating = review.rating
                favorite_restaurant = review.restaurant
        return favorite_restaurant

    def add_review(self,restaurant, rating):
        new_review = Review(restaurant=restaurant, rating=rating)
        session.add(new_review)
        session.commit()

    def delete_reviews(self, restaurant):
       
        delete_reviews = [review for review in self.reviews if review.restaurant == restaurant]

        for review in delete_reviews:
            session.delete(review)
        session.commit()



class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer(), primary_key=True)
    restaurant_id = Column(Integer())
    customer_id = Column(Integer())

    restaurant_iden = Column(Integer(), ForeignKey('restaurants.id'))
    customer_iden = Column(Integer(), ForeignKey('customers.id'))



    def full_review(self):
        return f"Review for: {self.restaurant.name} by {self.full_name()}: {self.rating} stars"
    




engine = create_engine('sqlite:///many_to_many.db', echo=True)
Base.metadata.create_all(bind = engine)
Session = sessionmaker(bind=engine)
session = Session()


#Test
customer1 = Customer(first_name="Sam", last_name="Oladele")
# customer2 = Customer(first_name="Sharon", last_name="Stev")
# customer3 = Customer(first_name="Esta", last_name="Woods")
# customer4 = Customer(first_name="Olivia", last_name="Olle")
# customer5 = Customer(first_name="Abi", last_name="Shana")
# customer6 = Customer(first_name="Jay", last_name="White")
# customer7 = Customer(first_name="Kay", last_name="Villian")
# customer8 = Customer(first_name="Ann", last_name="Ospot")
session.add(customer1)
# session.add(customer2)
# session.add(customer3)
# session.add(customer4)
# session.add(customer5)
# session.add(customer6)
# session.add(customer7)
# session.add(customer8)
session.commit()


# customer1.add_review("Dominos", 5)

restaurant1 = Restaurant(name="Dominos", price=4600)
# restaurant3 = Restaurant(name="KFC", price=2345)
# restaurant2 = Restaurant(name="Amala Joint", price=6868)
# restaurant4 = Restaurant(name="Tastee", price=3556)
# restaurant5 = Restaurant(name="Thiancee", price=3865)
# restaurant6 = Restaurant(name="Chicken Rep", price=2994)
# restaurant7 = Restaurant(name="Coldstone", price=6584)
# restaurant8 = Restaurant(name="Dodo Pizza", price=3848)


session.add(restaurant1)
# session.add(restaurant2)
# session.add(restaurant3)
# session.add(restaurant4)
# session.add(restaurant5)
# session.add(restaurant6)
# session.add(restaurant7)
# session.add(restaurant8)
session.commit()


review1 = Review(restaurants=restaurant1, customers=customer1, rating=5)
# review2 = Review(restaurant_id=restaurant1, customer_id=customer1, rating=3)
# review3 = Review(restaurant_id=restaurant5, customer_id=customer5, rating=4)
# review4 = Review(restaurant_id=restaurant6, customer_id=customer6, rating=5)
# review5 = Review(restaurant_id=restaurant4, customer_id=customer4, rating=2)
# review6 = Review(restaurant_id=restaurant1, customer_id=customer1, rating=1)
# review7 = Review(restaurant_id=restaurant7, customer_id=customer7, rating=5)
# review8 = Review(restaurant_id=restaurant2, customer_id=customer2, rating=3)
# review9 = Review(restaurant_id=restaurant8, customer_id=customer8, rating=2)
# review10 = Review(restaurant_id=restaurant1, customer_id=customer8, rating=2)

session.add(review1)
# session.add(review2)
# session.add(review3)
# session.add(review4)
# session.add(review5)
# session.add(review6)
# session.add(review7)
# session.add(review8)
# session.add(review9)
# session.add(review10)
session.commit()