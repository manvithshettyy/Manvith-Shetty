from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
import os
from models import db, User, Category, Transaction, Budget
from services.finance_service import FinanceService
from services.analytics_service import AnalyticsService

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db.init_app(app)
CORS(app)

# Initialize services
finance_service = FinanceService()
analytics_service = AnalyticsService()

@app.before_first_request
def create_tables():
    """Create database tables and seed initial data"""
    db.create_all()
    
    # Create default categories if they don't exist
    default_categories = [
        'Food & Dining', 'Transportation', 'Shopping', 'Entertainment',
        'Bills & Utilities', 'Healthcare', 'Education', 'Travel',
        'Salary', 'Freelance', 'Investment', 'Other'
    ]
    
    for cat_name in default_categories:
        if not Category.query.filter_by(name=cat_name).first():
            category = Category(name=cat_name)
            db.session.add(category)
    
    db.session.commit()

# User Routes
@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        user = finance_service.create_user(
            name=data['name'],
            email=data['email']
        )
        return jsonify(user.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user by ID"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

# Category Routes
@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])

@app.route('/api/categories', methods=['POST'])
def create_category():
    """Create a new category"""
    try:
        data = request.get_json()
        category = finance_service.create_category(data['name'])
        return jsonify(category.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Transaction Routes
@app.route('/api/transactions', methods=['POST'])
def create_transaction():
    """Create a new transaction"""
    try:
        data = request.get_json()
        transaction = finance_service.create_transaction(
            user_id=data['user_id'],
            category_id=data['category_id'],
            amount=data['amount'],
            description=data.get('description', ''),
            transaction_type=data['type'],
            date=datetime.fromisoformat(data.get('date', datetime.now().isoformat()))
        )
        return jsonify(transaction.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Get transactions with optional filters"""
    user_id = request.args.get('user_id', type=int)
    category_id = request.args.get('category_id', type=int)
    transaction_type = request.args.get('type')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    transactions = finance_service.get_transactions(
        user_id=user_id,
        category_id=category_id,
        transaction_type=transaction_type,
        start_date=start_date,
        end_date=end_date
    )
    
    return jsonify([transaction.to_dict() for transaction in transactions])

@app.route('/api/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    """Update a transaction"""
    try:
        data = request.get_json()
        transaction = finance_service.update_transaction(transaction_id, data)
        return jsonify(transaction.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    """Delete a transaction"""
    try:
        finance_service.delete_transaction(transaction_id)
        return jsonify({'message': 'Transaction deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Budget Routes
@app.route('/api/budgets', methods=['POST'])
def create_budget():
    """Create a new budget"""
    try:
        data = request.get_json()
        budget = finance_service.create_budget(
            user_id=data['user_id'],
            category_id=data['category_id'],
            amount=data['amount'],
            period=data.get('period', 'monthly')
        )
        return jsonify(budget.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/budgets', methods=['GET'])
def get_budgets():
    """Get budgets for a user"""
    user_id = request.args.get('user_id', type=int)
    budgets = finance_service.get_budgets(user_id)
    return jsonify([budget.to_dict() for budget in budgets])

@app.route('/api/budgets/<int:budget_id>', methods=['PUT'])
def update_budget(budget_id):
    """Update a budget"""
    try:
        data = request.get_json()
        budget = finance_service.update_budget(budget_id, data)
        return jsonify(budget.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/budgets/<int:budget_id>', methods=['DELETE'])
def delete_budget(budget_id):
    """Delete a budget"""
    try:
        finance_service.delete_budget(budget_id)
        return jsonify({'message': 'Budget deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Analytics Routes
@app.route('/api/analytics/summary/<int:user_id>', methods=['GET'])
def get_financial_summary(user_id):
    """Get financial summary for a user"""
    try:
        period = request.args.get('period', 'monthly')
        summary = analytics_service.get_financial_summary(user_id, period)
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/analytics/spending-by-category/<int:user_id>', methods=['GET'])
def get_spending_by_category(user_id):
    """Get spending breakdown by category"""
    try:
        period = request.args.get('period', 'monthly')
        data = analytics_service.get_spending_by_category(user_id, period)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/analytics/monthly-trend/<int:user_id>', methods=['GET'])
def get_monthly_trend(user_id):
    """Get monthly spending/income trend"""
    try:
        months = request.args.get('months', 6, type=int)
        data = analytics_service.get_monthly_trend(user_id, months)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/analytics/budget-status/<int:user_id>', methods=['GET'])
def get_budget_status(user_id):
    """Get budget status and alerts"""
    try:
        data = analytics_service.get_budget_status(user_id)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Health check route
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
