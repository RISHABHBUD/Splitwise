# Splitwise
# Expense Sharing App

## Overview

The Expense Sharing App is a web application designed to help users share expenses with their friends and family. It allows users to create expenses, split costs, and keep track of balances.

![System Architecture](architecture.png)

## Table of Contents

- [Database Schema](#database-schema)
- [System Architecture](#system-architecture)
- [API Endpoints](#api-endpoints)
- [Scheduled Email Reminders](#scheduled-email-reminders)
- [Getting Started](#getting-started)
- [Running the Application](#running-the-application)
- [Contributing](#contributing)
- [Contact](#contact)

## Database Schema

The application uses the following database models:

- **User**: Represents users with name, email, and mobile number.
- **Expense**: Describes expenses with amount, description, payer, expense type, split percentages, and participants.
- **Transaction**: Records transactions between users, including the sender, receiver, amount, and description.

## System Architecture

The system follows a typical Django web application structure. It includes views, serializers, models, and URLs to define the application's behavior. Celery is used for asynchronous task scheduling, such as sending email reminders.

## API Endpoints

### Create Expense

- `POST /api/expenses/`: Create a new expense with details such as amount, description, payer, expense type, split percentages, and participants.

### Get Balances

- `GET /api/expenses/balances/`: Retrieve balances between users. Shows who owes whom and the amount.

## Scheduled Email Reminders

The application sends email reminders to users about their weekly balances. This is achieved through a Celery task that runs once a week, calculating balances and sending notifications.

## Getting Started

To get started with this project, follow these steps:

1. Clone the repository to your local machine.

2. Set up your virtual environment and install project dependencies from the `requirements.txt` file.

   ```bash
   pip install -r requirements.txt
