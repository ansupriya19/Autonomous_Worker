# 🤖 Autonomous Enterprise AI Task Worker

An autonomous AI worker prototype that converts natural-language business requests into enterprise data retrieval, policy evaluation, decision-making, and explainable outcomes.

The system is designed around a simple idea:

> **The user describes the business outcome. The worker determines what information is required, applies the appropriate business rules, and returns the result with evidence.**

This prototype uses a local MySQL database containing simulated enterprise data for employees, customers, orders, refunds, inventory, vendors, payroll, performance, and support tickets.

---

## 🚀 What This Project Demonstrates

The worker can understand natural-language requests such as:

```text
Check low stock items
```

```text
What is the name of employee EMP-20001?
```

```text
What is the paycheck status for employee EMP-20001?
```

```text
Check refund eligibility for order ORD-10001
```

```text
Show pending customer tickets
```

Instead of requiring the user to manually select a workflow, the worker determines the relevant operation and retrieves the required company data.

The response contains:

* **Result** — the direct answer to the user's request
* **Action** — what the worker actually did
* **Evidence** — which company data/policies supported the result
* **Status** — completed, clarification required, or human approval required
* **Confidence**
* **Structured data tables** where useful

---

# 🏗️ Architecture

```text
                Natural Language Request
                         │
                         ▼
                 ┌───────────────┐
                 │  Streamlit UI │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │    FastAPI    │
                 │   /task API   │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │ Autonomous    │
                 │ Worker        │
                 └───────┬───────┘
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
          Discover     Policy     Execute/
           Data       Evaluation   Decide
             │           │           │
             └───────────┼───────────┘
                         ▼
                   ┌───────────┐
                   │   MySQL   │
                   │ Database  │
                   └─────┬─────┘
                         │
                         ▼
                Evidence + Outcome
                         │
                         ▼
                   Streamlit UI
```

---

# 🛠️ Technology Stack

* Python 3.10+
* FastAPI
* Uvicorn
* Streamlit
* MySQL 8.0+
* mysql-connector-python
* python-dotenv
* Requests

The project does **not require Docker**.

---

# 📁 Project Structure

```text
final_worker/
│
├── app/
│   ├── main.py
│   ├── worker.py
│   └── db.py
│
├── data/
│   └── company.sql
│
├── streamlit_app.py
├── requirements.txt
├── setup.bat
├── run.bat
├── .env.example
├── .gitignore
└── README.md
```

---

# 💾 Database

The prototype uses **MySQL 8.0** as the source of truth.

The SQL seed file is:

```text
data/company.sql
```

The database contains simulated company information such as:

```text
employees
employee_performance
payroll
customers
orders
refunds
inventory
vendors
tickets
```

No production or confidential company data is required.

---

# ⚙️ Prerequisites

Before running the project, install:

### 1. Python

Python 3.10 or newer.

Check:

```powershell
python --version
```

or:

```powershell
py --version
```

### 2. MySQL Server

Install MySQL Server 8.0 or newer.

Check that the MySQL service is running:

```powershell
Get-Service MySQL80
```

You should see:

```text
Status   Name
------   ----
Running  MySQL80
```

---

# 📥 1. Clone the Repository

```powershell
git clone https://github.com/YOUR-USERNAME/autonomous-ai-task-worker.git
```

Enter the project directory:

```powershell
cd autonomous-ai-task-worker
```

---

# 🐍 2. Create the Python Virtual Environment

Windows PowerShell:

```powershell
py -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell activation is restricted, you can run the project using:

```powershell
.\.venv\Scripts\python.exe
```

without activating the environment.

---

# 📦 3. Install Dependencies

With the virtual environment activated:

```powershell
python -m pip install -r requirements.txt
```

If you use the included setup script:

```powershell
.\setup.bat
```

---

# 🔐 4. Configure MySQL

Create a `.env` file in the project root.

You can copy the example:

```powershell
copy .env.example .env
```

Then open `.env` and configure your MySQL password:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD
DB_NAME=enterprise_ai_worker

REFUND_APPROVAL_THRESHOLD=10000
```

Replace:

```text
YOUR_MYSQL_PASSWORD
```

with your local MySQL root password.

### Important

Do **not** commit `.env` to GitHub.

The repository should only contain:

```text
.env.example
```

---

# 🗄️ 5. Create the Database

Open MySQL:

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

Enter your MySQL password.

Create the database:

```sql
CREATE DATABASE enterprise_ai_worker;
```

Exit:

```sql
exit;
```

---

# 📥 6. Import the Company Data

From PowerShell:

```powershell
Get-Content .\data\company.sql | & "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p enterprise_ai_worker
```

Enter your MySQL password.

### If the SQL file already exists in the database

If you see:

```text
ERROR 1050: Table already exists
```

the database has already been initialized.

You do not need to import the schema again.

---

# 🔍 7. Verify MySQL

Run:

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p -e "USE enterprise_ai_worker; SHOW TABLES;"
```

You should see the company tables.

---

# ▶️ 8. Start the Application

The easiest method is:

```powershell
.\run.bat
```

The application starts two components:

### Worker API

```text
http://127.0.0.1:8000
```

### Streamlit UI

```text
http://127.0.0.1:8502
```

Open the Streamlit URL in your browser:

```text
http://127.0.0.1:8502
```

---

# 🧪 9. Verify the API

Open a second PowerShell terminal and run:

```powershell
Invoke-WebRequest http://127.0.0.1:8000/health | Select-Object -ExpandProperty Content
```

A healthy database connection should return:

```json
{"ok":true}
```

You can also open:

```text
http://127.0.0.1:8000/docs
```

to view the FastAPI Swagger interface.

---

# 💬 10. Using the Worker

Open:

```text
http://127.0.0.1:8502
```

Enter a natural-language task.

## Example 1 — Inventory

```text
Check low stock items
```

The worker returns:

```text
Result

6 low-stock item(s):
Wireless Headphones,
Wireless Mouse,
...
```

Then it shows a table containing:

```text
SKU
Item
Stock
Reorder Point
Reorder Quantity
Vendor
Vendor Email
```

---

## Example 2 — Employee

```text
What is the name of employee EMP-20001?
```

The worker returns the employee's name directly.

The UI also provides the underlying employee record as evidence.

---

## Example 3 — Payroll

```text
What is the paycheck status for employee EMP-20001?
```

The worker checks the payroll information and returns the relevant status.

---

## Example 4 — Refund

```text
Check refund eligibility for order ORD-10001
```

The worker evaluates:

* Payment status
* Return window
* Previous refund state
* Refund amount
* Approval threshold

The result can be:

```text
APPROVED
```

```text
PENDING
```

or:

```text
REJECTED
```

Each refund decision contains an explicit reason.

For example:

```text
PENDING

Reason:
Eligible, but the refund amount meets or exceeds
the configured human approval threshold.
```

---

## Example 5 — Support Tickets

```text
Show pending customer tickets
```

The worker separates the relevant ticket records and displays them in a table.

---

# 🧠 Autonomous Behavior

The prototype demonstrates bounded autonomy.

The worker can:

1. Understand a natural-language objective
2. Identify the relevant business workflow
3. Extract identifiers from the request
4. Query the appropriate company data
5. Apply business rules
6. Produce a decision
7. Explain the decision
8. Provide supporting evidence
9. Route high-risk refund decisions for human approval

The system deliberately does not allow unrestricted autonomous execution of high-risk financial operations.

---

# 🛡️ Human Approval

High-value refunds are not silently approved.

The prototype uses:

```env
REFUND_APPROVAL_THRESHOLD=10000
```

If an otherwise eligible refund reaches the configured threshold, the worker returns:

```text
HUMAN_APPROVAL_REQUIRED
```

with the reason.

This separates:

```text
AI reasoning
```

from:

```text
business safety controls
```

This is intentional.

---

# 🔎 Explainability

Every task response contains:

### Result

The direct answer to the user's question.

### Action

What the worker actually did.

### Evidence

The company data and policies used to reach the result.

### Structured Data

Relevant records are displayed in tables where appropriate.

This makes the worker easier to audit and debug than a system that simply generates an answer.

---

# ⚠️ Current Limitations

This is a prototype rather than a production enterprise agent.

Current limitations include:

* Supported workflows are bounded
* Business policies are implemented in application logic
* MySQL is the primary data source
* Enterprise tools are simulated rather than connected to real company systems
* Authentication and authorization are not production-ready
* Long-term task memory is not implemented
* Tool discovery is not yet dynamic
* Human approval is represented as a workflow state rather than a production approval service
* Vendor email integration is not yet a production mail system

---

# 🚀 Future Improvements

With additional development, the worker could be extended with:

* LLM-based task planning
* Dynamic tool discovery
* Tool registry
* Policy/RAG layer
* Browser automation
* Email integration
* Enterprise API connectors
* Persistent task memory
* Task retry and recovery
* Idempotency controls
* Audit logs
* Human approval UI
* Role-based access control
* Confidence-based escalation
* Production authentication
* Observability and tracing
* Automated evaluation datasets

The long-term architecture would allow the same worker to operate across browsers, files, internal APIs, SaaS applications, and desktop systems.

---

# 🔒 Security Notes

Never commit real credentials.

Do not upload:

```text
.env
database passwords
API keys
access tokens
production data
company credentials
```

The `.gitignore` file should exclude:

```text
.env
.venv/
__pycache__/
*.pyc
```

The included SQL data should be treated as simulated/demo company data.

---

# 🐛 Troubleshooting

## MySQL is not reachable

Check:

```powershell
Get-Service MySQL80
```

If it is stopped:

```powershell
Start-Service MySQL80
```

Then test:

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

---

## `mysql` is not recognized

Use the full MySQL path:

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
```

Optionally add the MySQL `bin` directory to your Windows PATH.

---

## Port 8000 is already in use

Check which process is using it:

```powershell
netstat -ano | findstr :8000
```

Then either stop the old worker process or close the old terminal running Uvicorn.

Do not start multiple API instances on port 8000.

---

## Port 8502 is already in use

Check:

```powershell
netstat -ano | findstr :8502
```

Close the previous Streamlit process or use another port.

---

## API is not running

Test:

```powershell
Invoke-WebRequest http://127.0.0.1:8000/health
```

If connection fails, start the API manually:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Then start Streamlit in another terminal:

```powershell
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py --server.address 127.0.0.1 --server.port 8502
```

---

# 🎥 Demo

The recommended demonstration flow is:

```text
1. Low-stock inventory
2. Refund policy decision
3. Employee lookup
4. Support tickets
5. Show FastAPI / worker architecture
6. Show MySQL source data
```

The demo focuses on actual task execution rather than only showing generated explanations.

---

# 📜 AI Coding Disclosure

AI coding assistance was used during development.

Tools used include:

* ChatGPT
* Antigravity

AI assistance was used for implementation support, debugging, code generation, documentation, and iterative development.

The submitted system and architecture are understood by the author and can be explained, debugged, and modified during a technical review.

---

# 👨‍💻 Project Goal

The goal of this prototype is not to demonstrate a chatbot.

The goal is to demonstrate the foundation of an **autonomous enterprise worker**:

```text
Natural Language Goal
        ↓
Understand
        ↓
Discover Data
        ↓
Apply Policy
        ↓
Decide / Execute
        ↓
Verify
        ↓
Evidence + Outcome
        ↓
Human Approval when Required
```

A future production version would extend this architecture from the simulated MySQL environment to real enterprise tools, browsers, APIs, files, email systems, and internal applications.
