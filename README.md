# Personal Finance Management System

A comprehensive REST API-based personal finance management system built with Flask, featuring expense tracking, budget management, and financial analytics.

## Features

### Core Functionality
- **User Management**: Create and manage user accounts
- **Transaction Tracking**: Record income and expenses with categories
- **Budget Management**: Set and monitor spending budgets by category
- **Category Organization**: Organize transactions with customizable categories
- **Financial Analytics**: Comprehensive reporting and insights

### API Endpoints
- **Users**: CRUD operations for user management
- **Transactions**: Full transaction management with filtering
- **Budgets**: Budget creation and monitoring
- **Analytics**: Financial summaries, trends, and budget status
- **Categories**: Category management for transaction organization

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Architecture**: Object-Oriented Programming with service layer pattern
- **API**: RESTful API design
- **Database Connectivity**: SQLAlchemy for database operations

## Project Structure

\`\`\`
finance-management-system/
├── app.py                 # Main Flask application
├── models.py             # Database models (User, Transaction, Category, Budget)
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── services/
│   ├── finance_service.py    # Business logic for finance operations
│   └── analytics_service.py  # Analytics and reporting logic
├── utils/
│   └── helpers.py        # Utility functions
├── scripts/
│   └── seed_data.py      # Database seeding script
└── README.md            # Project documentation
\`\`\`

## Installation & Setup

1. **Clone the repository**
   \`\`\`bash
   git clone <repository-url>
   cd finance-management-system
   \`\`\`

2. **Create virtual environment**
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   \`\`\`

3. **Install dependencies**
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. **Initialize database**
   \`\`\`bash
   python scripts/seed_data.py
   \`\`\`

5. **Run the application**
   \`\`\`bash
   python app.py
   \`\`\`

The API will be available at `http://localhost:5000`

## API Documentation

### Users
- `POST /api/users` - Create a new user
- `GET /api/users` - Get all users
- `GET /api/users/<id>` - Get user by ID

### Categories
- `GET /api/categories` - Get all categories
- `POST /api/categories` - Create a new category

### Transactions
- `POST /api/transactions` - Create a new transaction
- `GET /api/transactions` - Get transactions (with optional filters)
- `PUT /api/transactions/<id>` - Update a transaction
- `DELETE /api/transactions/<id>` - Delete a transaction

### Budgets
- `POST /api/budgets` - Create a new budget
- `GET /api/budgets` - Get budgets for a user
- `PUT /api/budgets/<id>` - Update a budget
- `DELETE /api/budgets/<id>` - Delete a budget

### Analytics
- `GET /api/analytics/summary/<user_id>` - Get financial summary
- `GET /api/analytics/spending-by-category/<user_id>` - Get spending by category
- `GET /api/analytics/monthly-trend/<user_id>` - Get monthly trends
- `GET /api/analytics/budget-status/<user_id>` - Get budget status and alerts

## Example API Usage

### Create a User
\`\`\`bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'
\`\`\`

### Add a Transaction
\`\`\`bash
curl -X POST http://localhost:5000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "category_id": 1,
    "amount": 50.00,
    "description": "Grocery shopping",
    "type": "expense",
    "date": "2024-01-15T10:30:00"
  }'
\`\`\`

### Get Financial Summary
\`\`\`bash
curl http://localhost:5000/api/analytics/summary/1?period=monthly
\`\`\`

## Object-Oriented Design

The system follows OOP principles with:

### Models (Data Layer)
- `User`: Represents user accounts
- `Transaction`: Represents financial transactions
- `Category`: Represents transaction categories
- `Budget`: Represents spending budgets

### Services (Business Logic Layer)
- `FinanceService`: Handles core finance operations
- `AnalyticsService`: Provides financial analytics and reporting

### Utilities
- `FinanceHelpers`: Utility functions for financial calculations
- `DateHelpers`: Date manipulation utilities

## Database Schema

### Users Table
- id (Primary Key)
- name
- email (Unique)
- created_at

### Categories Table
- id (Primary Key)
- name (Unique)
- created_at

### Transactions Table
- id (Primary Key)
- user_id (Foreign Key)
- category_id (Foreign Key)
- amount
- description
- type (income/expense)
- date
- created_at

### Budgets Table
- id (Primary Key)
- user_id (Foreign Key)
- category_id (Foreign Key)
- amount
- period
- created_at

## Features Demonstrated

### Functions
- Database CRUD operations
- Financial calculations
- Data validation
- Date manipulation
- Analytics computations

### Object-Oriented Programming
- Model classes with methods
- Service layer pattern
- Inheritance and encapsulation
- Method overriding

### Database Connectivity
- SQLAlchemy ORM
- Database relationships
- Query optimization
- Transaction management

### Flask Framework
- RESTful API design
- Request handling
- JSON serialization
- Error handling
- CORS support

## Sample Data

The system includes a seeding script that creates:
- 3 sample users
- 12 default categories
- 75 sample transactions (25 per user)
- 15 sample budgets (5 per user)

## Development Notes

- The application uses SQLite for simplicity but can be easily configured for PostgreSQL or MySQL
- All monetary values are stored as floats with 2 decimal precision
- Dates are stored in ISO format
- The API includes comprehensive error handling
- CORS is enabled for frontend integration

## Future Enhancements

- User authentication and authorization
- File upload for transaction imports
- Email notifications for budget alerts
- Advanced reporting with charts
- Mobile app integration
- Multi-currency support

## License

This project is created for educational purposes demonstrating Flask, OOP, and database connectivity concepts.
\`\`\`

```python file="run.py"
#!/usr/bin/env python3
"""
Main entry point for the Finance Management System
"""

from app import app
from models import db

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        print("Database tables created successfully!")
        print("Starting Finance Management System...")
        print("API available at: http://localhost:5000")
        print("Health check: http://localhost:5000/api/health")
    
    # Run the Flask application
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
