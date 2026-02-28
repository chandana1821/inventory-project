from flask import Flask, render_template, request, jsonify
from datetime import datetime
from config import Config

from models.mysql_models import db
from models.mongo_models import mongo


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    mongo.init_app(app)

    register_routes(app)

    return app


def register_routes(app):

    # ================= FRONTEND ROUTES =================

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/users')
    def users_page():
        return render_template('users.html')

    @app.route('/products')
    def products_page():
        return render_template('products.html')

    @app.route('/orders')
    def orders_page():
        return render_template('orders.html')

    @app.route('/logs')
    def logs_page():
        return render_template('logs.html')

    # ================= USER CRUD =================

    @app.route('/api/users', methods=['GET'])
    def get_users():
        try:
            from models.mysql_models import User

            users = User.query.all()
            result = [{
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'full_name': u.full_name,
                'is_admin': u.is_admin,
                'created_at': u.created_at.isoformat() if u.created_at else None
            } for u in users]

            return jsonify(result)

        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @app.route('/api/users', methods=['POST'])
    def create_user():
        try:
            from models.mysql_models import User
            from models.mongo_models import ActivityLog

            data = request.json

            user = User(
                username=data['username'],
                email=data['email'],
                password_hash='temp_hash',
                full_name=data['full_name'],
                is_admin=data.get('is_admin', False)
            )

            db.session.add(user)
            db.session.commit()

            ActivityLog.log_action(
                user_id=user.id,
                action='USER_CREATE',
                details=f'User {user.username} created'
            )

            return jsonify({'message': 'User created', 'id': user.id}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


    @app.route('/api/users/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        try:
            from models.mysql_models import User
            from models.mongo_models import ActivityLog

            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404

            data = request.json
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.full_name = data.get('full_name', user.full_name)
            user.is_admin = data.get('is_admin', user.is_admin)

            db.session.commit()

            ActivityLog.log_action(
                user_id=user_id,
                action='USER_UPDATE',
                details=f'User {user.username} updated'
            )

            return jsonify({'message': 'User updated'})

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


    @app.route('/api/users/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        try:
            from models.mysql_models import User
            from models.mongo_models import ActivityLog

            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'User not found'}), 404

            username = user.username

            ActivityLog.log_action(
                user_id=user_id,
                action='USER_DELETE',
                details=f'User {username} deleted'
            )

            db.session.delete(user)
            db.session.commit()

            return jsonify({'message': 'User deleted'})

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


    # ================= PRODUCT CRUD =================

    @app.route('/api/products', methods=['GET'])
    def get_products():
        try:
            from models.mysql_models import Product, Inventory

            products = Product.query.all()
            result = []

            for p in products:
                inventory = Inventory.query.filter_by(product_id=p.id).first()
                result.append({
                    'id': p.id,
                    'name': p.name,
                    'description': p.description,
                    'price': float(p.price),
                    'stock_quantity': inventory.quantity if inventory else 0,
                    'created_at': p.created_at.isoformat() if p.created_at else None
                })

            return jsonify(result)

        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @app.route('/api/products', methods=['POST'])
    def create_product():
        try:
            from models.mysql_models import Product, Inventory
            from models.mongo_models import ActivityLog

            data = request.json

            product = Product(
                name=data['name'],
                description=data.get('description', ''),
                price=data['price']
            )

            db.session.add(product)
            db.session.flush()

            inventory = Inventory(
                product_id=product.id,
                quantity=data.get('stock_quantity', 0)
            )

            db.session.add(inventory)
            db.session.commit()

            ActivityLog.log_action(
                action='PRODUCT_CREATE',
                details=f'Product {product.name} created'
            )

            return jsonify({'message': 'Product created', 'id': product.id}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


    @app.route('/api/products/<int:product_id>', methods=['DELETE'])
    def delete_product(product_id):
        try:
            from models.mysql_models import Product
            from models.mongo_models import ActivityLog

            product = Product.query.get(product_id)
            if not product:
                return jsonify({'error': 'Product not found'}), 404

            ActivityLog.log_action(
                action='PRODUCT_DELETE',
                details=f'Product {product.name} deleted'
            )

            db.session.delete(product)
            db.session.commit()

            return jsonify({'message': 'Product deleted'})

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


    # ================= INVENTORY =================

    @app.route('/api/inventory', methods=['GET'])
    def get_inventory():
        try:
            from models.mysql_models import Inventory, Product

            inventory_items = Inventory.query.all()
            result = []

            for item in inventory_items:
                product = Product.query.get(item.product_id)
                result.append({
                    'product_id': item.product_id,
                    'product_name': product.name if product else 'Unknown',
                    'quantity': item.quantity,
                    'low_stock_threshold': item.low_stock_threshold,
                    'is_low_stock': item.quantity <= item.low_stock_threshold
                })

            return jsonify(result)

        except Exception as e:
            return jsonify({'error': str(e)}), 500


    # ================= ORDERS =================

    @app.route('/api/orders', methods=['GET'])
    def get_orders():
        try:
            from models.mysql_models import Order, User

            orders = Order.query.all()
            result = [{
                'id': o.id,
                'user_id': o.user_id,
                'total_amount': float(o.total_amount),
                'status': o.status
            } for o in orders]

            return jsonify(result)

        except Exception as e:
            return jsonify({'error': str(e)}), 500


    # ================= TEST =================

    @app.route('/api/test', methods=['GET'])
    def test_connection():
        try:
            from models.mysql_models import User
            count = User.query.count()
            return jsonify({'status': 'success', 'user_count': count})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)