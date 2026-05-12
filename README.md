# Microshop Products Service

## Description

This is the Products microservice for the Microshop project, a microservices-based e-commerce platform. It manages product information including creation, inventory, and pricing.

This service will integrate with other microservices: User, Orders, Middleware, and Notification.

## Current Implementation

- **Framework**: FastAPI with SQLModel (SQLAlchemy + Pydantic)
- **Database**: PostgreSQL
- **Models**: Product model with fields: id, name, description, price, stock, created_at
- **Schemas**: ProductCreate, ProductOut, ProductUpdate
- **Services**: Only create_product service implemented
- **Routers**: Only POST /products endpoint for creating products
- **Health Checks**: /health and /ready endpoints
- **Configuration**: Environment-based config for database and JWT (though JWT not used yet)

## Features Implemented

- Product creation with duplicate name validation
- Database session management
- Basic health checks

## Missing Features / Future Work

- Complete CRUD operations: Read (GET), Update (PUT), Delete (DELETE) for products
- Docker containerization
- Integration with User service (authentication/authorization)
- Event-driven architecture (events folder)
- Middleware implementation
- Repository pattern for data access
- Clients for communicating with other microservices (Orders, Notification, etc.)

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables for PostgreSQL (see config.py for details)
3. Run the app: `uvicorn app.main:app --reload`

## API Documentation

Available at /docs when running the service.