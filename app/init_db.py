from app import app
from database import db
from models import User, Product

with app.app_context():

    db.create_all()

    if User.query.count() == 0:

        users = [

            User(
                username="admin",
                email="admin@shopsmart.local",
                password="admin123",
                role="admin"
            ),

            User(
                username="john",
                email="john@example.com",
                password="password123"
            )
        ]

        db.session.add_all(users)

    if Product.query.count() == 0:

        products = [

            Product(
                name="Laptop",
                description="15-inch business laptop",
                price=999.99
            ),

            Product(
                name="Keyboard",
                description="Mechanical keyboard",
                price=79.99
            ),

            Product(
                name="Mouse",
                description="Wireless gaming mouse",
                price=49.99
            ),

            Product(
                name="Monitor",
                description="27-inch IPS display",
                price=299.99
            )
        ]

        db.session.add_all(products)

    db.session.commit()

    print("Database initialized successfully.")