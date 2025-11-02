# DevArena

**An interactive coding assessment and tracking platform for higher institutions.**
DevArena enables instructors to create and grade programming challenges automatically, while students can practice, submit solutions, and track their learning progress in real time.

---

## 🚀 Key Features

* **User Authentication** – Secure login and role-based access for students, instructors, and admins.
* **Task Management** – Create, assign, and manage coding challenges with deadlines.
* **Automated Grading** – Submissions are tested in a sandboxed environment with auto-scoring.
* **Progress Tracking** – Visual dashboards for monitoring student performance over time.
* **Collaboration** – Students and instructors can share resources and discuss solutions.
* **Resource Sharing** – Upload and organize course-related materials within the platform.

---

## 🧩 Tech Stack

| Layer              | Technology                                         |
| :----------------- | :------------------------------------------------- |
| **Frontend**       | React + TailwindCSS (bundled with Vite)            |
| **Backend**        | Python Flask (REST API) + SQLAlchemy ORM           |
| **Database**       | MySQL                                              |
| **Cache / Broker** | Redis                                              |
| **Async Tasks**    | Background worker for grading heavy code execution |

---

## 🏗️ Architecture Overview

```
┌──────────────┐        HTTPS / REST API        ┌──────────────┐
│   Frontend   │  <──────────────────────────>  │   Flask API  │
│ (React/Vite) │                                │  (Python)    │
└──────────────┘                                └──────────────┘
                                                         │
                                                         ▼
                                                ┌────────────────┐
                                                │    MySQL DB     │
                                                └────────────────┘
                                                         │
                                                         ▼
                                                ┌────────────────┐
                                                │  Redis Broker   │
                                                └────────────────┘
                                                         │
                                                         ▼
                                                ┌────────────────┐
                                                │ Async Worker   │
                                                │ (Grading jobs) │
                                                └────────────────┘
```

The **frontend** communicates with the **Flask backend** via REST APIs.
The backend interacts with **MySQL** for persistent data storage and **Redis** for caching and task queuing.
Long-running operations such as grading student submissions are handled asynchronously by a background worker.

---

## ⚙️ Setup & Installation

### Prerequisites

Ensure the following are installed on your system:

* **Python 3.9+**
* **Node.js 18+** and **npm**
* **MySQL 8+**
* **Redis Server**

### Clone Repository

```bash
git clone https://github.com/yourusername/DevArena.git
cd DevArena
```

### Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Backend
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/devarena
REDIS_URL=redis://localhost:6379/0

# Frontend
VITE_API_BASE_URL=http://localhost:5000/api/v1
```

---

## 🐍 Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Build runner images and bring up Redis (for local testing):
```bash
cd backend
docker compose build
docker compose up -d redis
```

Or just start Redis separately:
```bash
sudo service redis-server start
```

Install Python deps and start worker:
```bash
pip install -r backend/requirements.txt
python3 backend/worker.py
```

(Or run rq worker grading after installing rq.)
```bash
rq worker grading
```

Start the API (as you were doing):


Run database migrations (if using Flask-Migrate):

```bash
flask db upgrade
```

Start the development server:

```bash
python -m api.v1.app
```

Production (via Gunicorn):

```bash
gunicorn -w 4 -b 0.0.0.0:5000 api.v1.app:app
```

---

## ⚛️ Frontend Setup

```bash
cd frontend
npm install
```

Start development server:

```bash
npm run dev
```

Build for production:

```bash
npm run build
```

Serve static files (example with `serve`):

```bash
npm install -g serve
serve -s dist
```

---

## 💻 Running the Application Locally

Start all components in separate terminals:

```bash
# Terminal 1 – MySQL & Redis (ensure both are running)
sudo service mysql start
redis-server

# Terminal 2 – Flask API
cd backend
source venv/bin/activate
python -m api.v1.app

# Terminal 3 – React Frontend
cd frontend
npm run dev
```

Visit [http://localhost:5173](http://localhost:5173) to access the DevArena UI.

---

## 🧭 Usage

### 👩‍🎓 For Students

* Register and log in to the portal.
* View assigned challenges under **Tasks**.
* Submit code solutions; results appear after automated grading.
* Track progress under **Dashboard**.

### 👨‍🏫 For Instructors

* Log in as instructor.
* Create and manage coding tasks.
* Review submissions, override grades if needed.
* Share resources and monitor overall course performance.

### Example API Endpoints

| Method | Endpoint                        | Description       |
| :----- | :------------------------------ | :---------------- |
| `POST` | `/api/v1/auth/login`            | User login        |
| `GET`  | `/api/v1/tasks`                 | List all tasks    |
| `POST` | `/api/v1/submissions`           | Submit a solution |
| `GET`  | `/api/v1/students/:id/progress` | Get progress data |

---

## 🛠️ Admin & Deployment Notes

* Run behind a **WSGI server** such as Gunicorn or uWSGI.
* Use **Nginx** or **Caddy** as a reverse proxy.
* Manage services via **systemd** or **Docker Compose**.
* Ensure all secrets and database credentials are provided via environment variables.
* For database schema changes:

```bash
flask db migrate -m "Add new table"
flask db upgrade
```

* Background worker example (Celery or RQ):

```bash
python worker.py
```

---

## ⚡ Performance & Scaling

**Current Design:**

* Flask synchronous API for most requests.
* Asynchronous worker handles heavy grading operations.
* Redis cache reduces repeated database queries.

**Recommended Improvements:**

* Introduce containerized sandboxing for code execution.
* Use horizontal scaling for the worker pool.
* Optimize query performance and enable connection pooling.
* Add WebSocket support for live feedback updates.

---

## 🔒 Security & Sandboxing

* Student code is executed in a **sandboxed environment** (e.g., Docker or Firejail).
* Uploads are validated and restricted by MIME type.
* All API endpoints are **rate-limited** and protected by JWT tokens.
* Avoid arbitrary file access or code execution on the host machine.

---

## 🧑‍💻 Contributing

We welcome contributions!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/awesome-feature`)
3. Commit your changes (`git commit -m 'Add awesome feature'`)
4. Push to your fork and open a pull request

---

## 📜 License

This project is licensed under the **MIT License**.
See the [LICENSE](LICENSE) file for more details.

---

## 🙌 Acknowledgments

* OpenAI & Flask communities for inspiration.
* Educational contributors who helped shape the problem sets.
* MySQL, Redis, and TailwindCSS developers for their open-source excellence.

---

## 🧩 Troubleshooting

| Issue                              | Possible Cause                       | Solution                                         |
| :--------------------------------- | :----------------------------------- | :----------------------------------------------- |
| `ModuleNotFoundError`              | Virtualenv not activated             | Run `source venv/bin/activate`                   |
| `ECONNREFUSED` on frontend         | Backend not running or wrong API URL | Ensure Flask API is up and check `.env`          |
| `redis.exceptions.ConnectionError` | Redis server not started             | Run `redis-server`                               |
| Database migration errors          | Version mismatch                     | Run `flask db downgrade` then `flask db upgrade` |

### Run Tests

```bash
pytest tests/
```

---

**DevArena** – Empowering institutions to teach, test, and track programming excellence.
🧠💻🎓

