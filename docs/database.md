# Database Design

## Overview

FINWISE uses MySQL to store user accounts, prediction results, chat history, and financial goals.

## app_users

Stores user account information.

| Column | Description |
| --- | --- |
| user_id | Primary key |
| full_name | User full name |
| email | User email |
| password_hash | Hashed password |

## prediction_history

Stores all financial analysis results.

| Column | Description |
| --- | --- |
| prediction_id | Primary key |
| user_id | Foreign key to app_users |
| umur | User age |
| pendapatan_bulanan | Monthly income |
| pengeluaran_bulanan | Monthly expense |
| total_tabungan | Total savings |
| total_utang | Total debt |
| jumlah_tanggungan | Number of dependents |
| debt_ratio | Debt ratio |
| expense_ratio | Expense ratio |
| saving_rate | Saving rate |
| predicted_label | Risk label |
| created_at | Timestamp of analysis |

## chat_history

Stores AI conversation history.

| Column | Description |
| --- | --- |
| chat_id | Primary key |
| user_id | Foreign key to app_users |
| role | Message role: user or assistant |
| message | Chat content |
| created_at | Timestamp of message |

## financial_goals

Stores user financial targets.

| Column | Description |
| --- | --- |
| goal_id | Primary key |
| user_id | Foreign key to app_users |
| goal_name | Goal name |
| target_amount | Target amount |
| created_at | Timestamp of goal creation |

## Notes

- The application reads prediction data in descending order of `created_at` for the dashboard and AI advisor.
- Dashboard statistics are calculated directly from `prediction_history`.
- Chat history is stored persistently so the AI advisor can continue previous conversations.
