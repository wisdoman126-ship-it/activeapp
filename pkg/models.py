
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()


# ==================================
# USER MODEL (CUSTOMER AND ADMIN)
# ==================================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), default="customer", nullable=False)

    phone = db.Column(db.String(20))
    address = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    cart = db.relationship(
        "Cart", back_populates="user", uselist=False,
        cascade="all, delete-orphan"
    )

    orders = db.relationship("Order", back_populates="user")
    reviews = db.relationship("Review", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == "admin"


# ==================================
# CATEGORY MODEL
# ==================================

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    products = db.relationship("Product", back_populates="category")


# ==================================
# PRODUCT MODEL
# ==================================

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)

    price = db.Column(db.Numeric(10, 2), nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey("category.id"), nullable=False
    )

    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    category = db.relationship("Category", back_populates="products")

    variants = db.relationship(
        "ProductVariant", back_populates="product",
        cascade="all, delete-orphan"
    )

    images = db.relationship(
        "ProductImage", back_populates="product",
        cascade="all, delete-orphan"
    )

    reviews = db.relationship("Review", back_populates="product")


# ==================================
# PRODUCT VARIANT MODEL
# ==================================

class ProductVariant(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer, db.ForeignKey("product.id"), nullable=False
    )

    size = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(50), nullable=False)

    stock_quantity = db.Column(db.Integer, default=0)
    sku = db.Column(db.String(100), unique=True)

    product = db.relationship("Product", back_populates="variants")

    __table_args__ = (
        UniqueConstraint(
            "product_id", "size", "color",
            name="unique_product_size_color"
        ),
    )


# ==================================
# PRODUCT IMAGE MODEL
# ==================================

class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer, db.ForeignKey("product.id"), nullable=False
    )

    image_url = db.Column(db.String(255), nullable=False)

    product = db.relationship("Product", back_populates="images")


# ==================================
# CART MODEL
# ==================================

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"),
        unique=True, nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="cart")

    items = db.relationship(
        "CartItem", back_populates="cart",
        cascade="all, delete-orphan"
    )


# ==================================
# CART ITEM MODEL
# ==================================

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    cart_id = db.Column(
        db.Integer, db.ForeignKey("cart.id"), nullable=False
    )

    variant_id = db.Column(
        db.Integer, db.ForeignKey("product_variant.id"), nullable=False
    )

    quantity = db.Column(db.Integer, default=1, nullable=False)

    cart = db.relationship("Cart", back_populates="items")
    variant = db.relationship("ProductVariant")


# ==================================
# ORDER MODEL
# ==================================

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )

    total_amount = db.Column(db.Numeric(10, 2), nullable=False)

    status = db.Column(db.String(30), default="pending")
    payment_status = db.Column(db.String(30), default="unpaid")

    shipping_address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="orders")

    items = db.relationship(
        "OrderItem", back_populates="order",
        cascade="all, delete-orphan"
    )


# ==================================
# ORDER ITEM MODEL
# ==================================

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer, db.ForeignKey("order.id"), nullable=False
    )

    variant_id = db.Column(
        db.Integer, db.ForeignKey("product_variant.id"), nullable=False
    )

    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

    order = db.relationship("Order", back_populates="items")
    variant = db.relationship("ProductVariant")


# ==================================
# REVIEW MODEL
# ==================================

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )

    product_id = db.Column(
        db.Integer, db.ForeignKey("product.id"), nullable=False
    )

    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="reviews")
    product = db.relationship("Product", back_populates="reviews")
