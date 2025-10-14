# EXPENSE TRACKER API

### pre requisites :

- docker
- python 3.12.0
- uv

### Commands to run project at the beginning :

- docker compose up -d => at the directory
- uv sync
- uv run uvicorn main:app --reload

### architecture

Layered (N-Tier) Architecture

Flow of Data
Client → Presentation Layer
API receives the request (POST /users).
Presentation → Service Layer
Endpoint calls UserService.create_user.
Service → Repository Layer
Service checks if email exists, then calls UserRepository.create.
Repository → Database Layer
Repository persists the new user with SQLAlchemy.
Database → Repository → Service → Presentation → Client
Data bubbles back up, transformed as needed.

Controllers = handle requests.
Services = define business rules.
Repositories = talk to DB.
Models = represent data.

## formatter,linter and extension config

- install ruff extension in vsc
- put this in settings.json :
  ```json
  "[python]": {
      "editor.formatOnSave": true,
      "editor.defaultFormatter": "charliermarsh.ruff",
      "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
      }
  }
  ```

### Database

- uv run alembic revision --autogenerate -m "add user model base"
- uv run alembic upgrade head
- uv run alembic history

## TO DO LATER

- check response methods , if its ok , or add something.
- create crud to auth and user register and get info, add more fields and refresh token.

## CORE FUNCTIONAL REQUIREMENTS

1. User Authentication & Security

   User registration and login (email, Google, Apple)
   Password reset and account recovery DONE
   Refresh tokens with rotated strategy DONE
   Two-factor authentication (optional)

2. Expense & Income Management
   Add income or expense entries
   Category selection (Food, Transport, Salary, etc.)
   Amount
   Date & time
   Description or notes
   Recurring toggle (e.g., every month)
   Edit/delete entries
   Attach receipt images or documents

3. Dashboard & Summaries

   Monthly/weekly summaries of income vs expenses
   Balance display (total income - total expenses)
   Calendar view of transactions

4. Charts & Reports

   Pie charts (category-wise expenses)
   Bar/line charts (monthly trends)
   Filter by category/date
   Export report to PDF or CSV

5. Notifications & Reminders

   Daily reminder to add expenses
   Budget limit alerts
   Upcoming recurring transactions

6. Budgeting Tools

   Set monthly category budgets
   Track progress (e.g., 70% of Food budget used)

7. Search & Filter

   Search by amount, category, description
   Filter by date range, income/expense type

8. Data Sync & Backup

   Cloud sync (Google Drive, iCloud, etc.)
   Local backup and restore
   Multi-device sync

## Differentiators to Stand Out

9. AI-Powered Smart Assistant

   Auto-categorize transactions using NLP
   Predict monthly expenses based on trends
   Suggest savings tips or budget adjustments

10. Bank/Email/Notification Integration

    Automatically fetch transactions from SMS, email (like BBVA or Yape), or bank APIs
    OCR for receipt scanning

11. Voice Input or Speech-to-Text

    "Hey app, I spent 20 on groceries today" → Adds expense automatically

12. Shared Wallets or Family Mode

    Allow shared access to a wallet (e.g., for couples or roommates)
    Assign roles (viewer, editor)

13. Gamification

    Earn badges for saving money
    Challenges like “No spend weekend” or “Save $100 this month”

14. Offline Mode

    Add/edit transactions without internet
    Sync when reconnected

15. Currency & Language Support

    Multi-currency accounts with auto-conversion
    Language localization for global reach

16. Custom Categories & Tags

    Users can define their own spending categories
    Use hashtags like #vacation, #business for filtering

17. AI-based Expense Forecasting

    Forecast next month's expenses and income
    Warning if future expenses exceed budget

18. Dark Mode & Personalization

    Themes and layout customizations
    Widget support for quick entry or overview

# Authentication Tokens strategy

Access Token (Stateless)
├── Never stored in DB
├── Verified by signature
├── Short-lived (15-30 min)
└── Used for API requests

Refresh Token (Stateful)
├── Stored in DB (hashed)
├── Long-lived (7-30 days)
├── Can be revoked
└── Used only for token refresh

Reset Token (Stateful)
├── Stored in DB
├── Very short-lived (15 min)
├── One-time use
└── Used only for password reset
