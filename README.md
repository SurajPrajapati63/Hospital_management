# 🏥 Hospital Management System

A comprehensive, full-stack hospital management platform with AI-powered assistant, real-time analytics, appointment scheduling, billing, and patient management. Built with **FastAPI** backend and **Streamlit** frontend.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Project Components](#project-components)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The Hospital Management System is a multi-module platform designed to streamline hospital operations including:
- **Patient Management**: Complete patient records and medical history
- **Doctor Management**: Doctor profiles and specializations
- **Appointment Scheduling**: Book, reschedule, and manage appointments
- **Prescription Management**: Digital prescription creation and tracking
- **Billing & Payments**: Invoice generation and payment tracking
- **Analytics & Reporting**: Real-time insights and system analytics
- **AI Assistant**: Intelligent medical assistant for queries and recommendations
- **Authentication & Authorization**: Secure JWT-based authentication

---

## ✨ Features

### 🔐 Authentication & Security
- JWT token-based authentication
- Password hashing with bcrypt
- Role-based access control (RBAC)
- Secure token refresh mechanism

### 👥 Patient Management
- Create and manage patient records
- Store medical history and health records
- Track patient demographics and contact information
- View patient appointments and prescriptions

### 👨‍⚕️ Doctor Management
- Manage doctor profiles and specializations
- Track doctor availability and schedules
- View doctor appointments and patient lists

### 📅 Appointment Scheduling
- Book, update, and cancel appointments
- Check doctor availability
- Send appointment notifications
- Automated appointment reminders

### 💊 Prescription Management
- Create and issue digital prescriptions
- Track prescription history
- Manage medication details and dosages
- Prescription analytics

### 💳 Billing & Payments
- Generate invoices and bills
- Track payment status
- Manage billing history
- Support multiple payment methods

### 📊 Analytics & Reporting
- Real-time dashboard analytics
- Appointment statistics
- Revenue insights
- Patient demographics analysis
- System health monitoring

### 🤖 AI Assistant
- Natural Language Processing for medical queries
- Intelligent prescription recommendations
- Medical report summarization
- RAG (Retrieval-Augmented Generation) engine
- Anomaly detection in medical data
- Integrated memory system for context

---

## 📁 Project Structure

```
Hospital_management/
├── BACKEND/                          # FastAPI Backend Application
│   ├── requirements.txt              # Python dependencies
│   ├── run.py                        # Application entry point
│   ├── test.py                       # Test suite
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI initialization & middleware
│   │   ├── config.py                 # Configuration management
│   │   ├── database.py               # MongoDB connection & setup
│   │   │
│   │   ├── models/                   # Database models
│   │   │   ├── patients_model.py     # Patient schema
│   │   │   ├── doctor_model.py       # Doctor schema
│   │   │   ├── appointment_model.py  # Appointment schema
│   │   │   ├── prescription_model.py # Prescription schema
│   │   │   ├── billing_model.py      # Billing schema
│   │   │   └── report_model.py       # Medical report schema
│   │   │
│   │   ├── schemas/                  # Pydantic request/response schemas
│   │   │   ├── patient_schema.py
│   │   │   ├── doctor_schema.py
│   │   │   ├── appointment_schema.py
│   │   │   ├── prescription_schema.py
│   │   │   ├── billing_schema.py
│   │   │   ├── auth_schema.py
│   │   │   └── ai_schema.py
│   │   │
│   │   ├── routers/                  # API route handlers
│   │   │   ├── auth.py               # Authentication endpoints
│   │   │   ├── patients.py           # Patient management endpoints
│   │   │   ├── doctors.py            # Doctor management endpoints
│   │   │   ├── appointments.py       # Appointment endpoints
│   │   │   ├── prescriptions.py      # Prescription endpoints
│   │   │   ├── billing.py            # Billing endpoints
│   │   │   └── ai_routes.py          # AI assistant endpoints
│   │   │
│   │   ├── services/                 # Business logic layer
│   │   │   ├── auth_service.py       # Authentication logic
│   │   │   ├── patient_service.py    # Patient operations
│   │   │   ├── appointment_service.py # Appointment management
│   │   │   ├── prescription_service.py
│   │   │   ├── billing_service.py
│   │   │   └── analytics_service.py  # Analytics & reporting
│   │   │
│   │   ├── AI/                       # AI/LLM Module
│   │   │   ├── llm_provider.py       # LLM integration (OpenAI, Gemini)
│   │   │   ├── medical_assistant.py  # Main AI assistant logic
│   │   │   ├── agent_tools.py        # AI agent tools & utilities
│   │   │   ├── rag_engine.py         # RAG (Retrieval-Augmented Generation)
│   │   │   ├── memory.py             # Conversation memory management
│   │   │   ├── prescription.py       # AI-powered prescription logic
│   │   │   ├── report_summarizer.py  # Medical report summarization
│   │   │   └── anomaly_detector.py   # Anomaly detection in data
│   │   │
│   │   ├── utils/                    # Utility functions
│   │   │   ├── jwt_handler.py        # JWT token management
│   │   │   ├── hash.py               # Password hashing utilities
│   │   │   └── logger.py             # Logging configuration
│   │   │
│   │   └── __pycache__/
│   │
│   ├── logs/                         # Application logs
│   └── __pycache__/
│
├── frontend/                         # Streamlit Frontend Application
│   ├── app.py                        # Main Streamlit app entry point
│   ├── config.py                     # Frontend configuration
│   │
│   ├── pages/                        # Streamlit pages
│   │   ├── Login.py                  # Authentication page
│   │   ├── Patients.py               # Patient management page
│   │   ├── Doctors.py                # Doctor management page
│   │   ├── Appointments.py           # Appointment scheduling page
│   │   ├── Prescriptions.py          # Prescription management page
│   │   ├── Billing.py                # Billing & payments page
│   │   ├── AI_Assistant.py           # AI assistant chat interface
│   │   └── Analytics.py              # Analytics dashboard
│   │
│   ├── components/                   # Reusable UI components
│   │   ├── forms.py                  # Form components
│   │   ├── tables.py                 # Table display components
│   │   └── chat_ui.py                # Chat UI components
│   │
│   ├── api/                          # API client modules
│   │   ├── auth_api.py               # Authentication API client
│   │   ├── patient_api.py            # Patient API client
│   │   ├── appointment_api.py        # Appointment API client
│   │   └── ai_api.py                 # AI assistant API client
│   │
│   ├── __pycache__/
│   └── .streamlit/                   # Streamlit configuration
│
└── README.md                         # This file
```

---

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI 0.110.0
- **Server**: Uvicorn 0.29.0
- **Database**: MongoDB (with pymongo 4.6.3)
- **Authentication**: JWT with python-jose & passlib
- **AI/LLM**: OpenAI & Google Gemini APIs
- **Validation**: Pydantic 2.6.4
- **Utilities**: 
  - python-dotenv for environment variables
  - python-multipart for file uploads
  - requests for HTTP calls

### Frontend
- **Framework**: Streamlit (Python web framework)
- **Configuration**: Python-dotenv
- **API Communication**: HTTP requests to FastAPI backend

### Development & Testing
- **Testing**: pytest 8.1.1
- **HTTP Client**: httpx 0.27.0

---

## 📋 Prerequisites

Before getting started, ensure you have:

- **Python**: 3.10 or higher
- **MongoDB**: 5.0 or higher (local or cloud instance)
- **pip**: Latest version
- **API Keys** (Optional but recommended):
  - OpenAI API Key (for GPT-based features)
  - Google Gemini API Key (alternative LLM)
- **Git**: For version control

### System Requirements
- RAM: Minimum 4GB (8GB recommended)
- Disk Space: 2GB for dependencies and logs
- Internet Connection: Required for LLM APIs and MongoDB Atlas

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Hospital_management.git
cd Hospital_management
```

### 2. Backend Setup

#### Create Virtual Environment

```bash
cd BACKEND
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Environment Configuration

Create a `.env` file in the `BACKEND/` directory:

```env
# App Configuration
APP_NAME="Hospital Management AI"
DEBUG=True
JWT_SECRET_KEY=9f8c1a4d9a3e7f8b4c2d6e5a1b3c9d7f6a2b8c4d1e9f7a6b3c2d4e5f6a7b8c9
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Configuration
MONGO_URI=mongodb+srv://username:password@clustername.mongodb.net/hospital_db?retryWrites=true&w=majority
MONGO_DB_NAME=hospital_db

# CORS Configuration
ALLOWED_ORIGINS=http://localhost,http://localhost:8501,http://localhost:3000

# LLM Provider Configuration
LLM_PROVIDER=gemini  # or 'openai'
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Frontend Setup

#### Install Streamlit & Dependencies

```bash
cd frontend
pip install streamlit requests python-dotenv
```

#### Frontend Environment Configuration

Create a `.env` file in the `frontend/` directory:

```env
BACKEND_URL=http://localhost:8000
DATABASE_NAME=hospital_management
JWT_SECRET_KEY=9f8c1a4d9a3e7f8b4c2d6e5a1b3c9d7f6a2b8c4d1e9f7a6b3c2d4e5f6a7b8c9
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DEBUG=True
```

---

## ⚙️ Configuration

### Backend Configuration (`app/config.py`)

The backend uses a `Settings` class that loads configuration from environment variables:

```python
class Settings:
    APP_NAME: str = "Hospital Management AI"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "default-key")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "hospital_db")
```

### Frontend Configuration (`frontend/config.py`)

Similar configuration structure with API endpoints and database settings.

### Database Setup

#### MongoDB Collections

The system automatically creates the following collections:

- `users` - User accounts and authentication
- `patients` - Patient records
- `doctors` - Doctor profiles
- `appointments` - Appointment records
- `prescriptions` - Prescription data
- `billing` - Invoice and billing information
- `reports` - Medical reports and documents
- `ai_conversations` - AI assistant conversation history

---

## 🎮 Running the Application

### Start Backend Service

```bash
cd BACKEND
# Activate virtual environment (if not already active)
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

python run.py
```

The backend will start at `http://localhost:8000`

Access the **Interactive API Documentation** (Swagger UI): http://localhost:8000/docs

### Start Frontend Service (in another terminal)

```bash
cd frontend
python -m streamlit run app.py
```

The frontend will start at `http://localhost:8501`

---

## 📖 API Documentation

### Backend API Documentation

Once the backend is running, access the interactive API docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Available API Endpoints

#### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - User login
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - User logout

#### Patients
- `GET /patients` - List all patients
- `POST /patients` - Create new patient
- `GET /patients/{patient_id}` - Get patient details
- `PUT /patients/{patient_id}` - Update patient
- `DELETE /patients/{patient_id}` - Delete patient

#### Doctors
- `GET /doctors` - List all doctors
- `POST /doctors` - Add new doctor
- `GET /doctors/{doctor_id}` - Get doctor details
- `PUT /doctors/{doctor_id}` - Update doctor
- `DELETE /doctors/{doctor_id}` - Delete doctor

#### Appointments
- `GET /appointments` - List appointments
- `POST /appointments` - Schedule appointment
- `GET /appointments/{appointment_id}` - Get appointment details
- `PUT /appointments/{appointment_id}` - Reschedule appointment
- `DELETE /appointments/{appointment_id}` - Cancel appointment

#### Prescriptions
- `GET /prescriptions` - List prescriptions
- `POST /prescriptions` - Create prescription
- `GET /prescriptions/{prescription_id}` - Get prescription details
- `PUT /prescriptions/{prescription_id}` - Update prescription
- `DELETE /prescriptions/{prescription_id}` - Delete prescription

#### Billing
- `GET /billing` - List bills
- `POST /billing` - Create invoice
- `GET /billing/{bill_id}` - Get bill details
- `PUT /billing/{bill_id}` - Update bill
- `DELETE /billing/{bill_id}` - Delete bill

#### Analytics
- `GET /analytics/dashboard` - Get dashboard analytics
- `GET /analytics/appointments` - Appointment statistics
- `GET /analytics/revenue` - Revenue insights
- `GET /analytics/patients` - Patient demographics

#### AI Assistant
- `POST /ai/chat` - Send message to AI assistant
- `GET /ai/chat/history` - Get conversation history
- `POST /ai/analyze` - Analyze medical report
- `POST /ai/prescribe` - Get prescription recommendations

---

## 🏗 Project Components

### Backend Architecture

#### 1. **Models** (`app/models/`)
- Database schema definitions using MongoDB
- Represents core entities: Patients, Doctors, Appointments, Prescriptions, etc.

#### 2. **Schemas** (`app/schemas/`)
- Pydantic models for request/response validation
- Ensures type safety and automatic documentation

#### 3. **Routers** (`app/routers/`)
- FastAPI route handlers organizing endpoints by feature
- Implements RESTful API design

#### 4. **Services** (`app/services/`)
- Business logic implementation
- Separates concerns from route handling
- Includes validation and data processing

#### 5. **AI Module** (`app/AI/`)
- **llm_provider.py**: Interface for multiple LLM providers
- **medical_assistant.py**: Main AI logic for healthcare queries
- **rag_engine.py**: RAG system for document retrieval
- **memory.py**: Conversation context management
- **report_summarizer.py**: Summarize medical reports
- **anomaly_detector.py**: Detect anomalies in patient data
- **prescription.py**: AI-driven prescription generation

#### 6. **Database** (`app/database.py`)
- MongoDB connection management
- Index creation for performance
- Connection pooling

#### 7. **Utilities** (`app/utils/`)
- JWT token handling
- Password hashing
- Logging configuration

### Frontend Architecture

#### 1. **Pages** (`frontend/pages/`)
- Individual Streamlit pages for each feature
- Modular, self-contained user interfaces

#### 2. **Components** (`frontend/components/`)
- Reusable UI components (forms, tables, chat interface)
- DRY principle implementation

#### 3. **API Clients** (`frontend/api/`)
- HTTP wrappers for backend communication
- Centralized API interaction logic

---

## 🔄 Workflow

### User Registration & Authentication
1. User registers via `Login.py` page
2. Password hashed with bcrypt
3. JWT token generated upon successful login
4. Token stored in Streamlit session state
5. All subsequent requests include token in headers

### Appointment Scheduling
1. User selects doctor and available time
2. Frontend sends request to `/appointments` endpoint
3. Service validates doctor availability
4. Appointment created in MongoDB
5. Notifications sent to both patient and doctor

### AI Assistant Interaction
1. User sends message in `AI_Assistant.py`
2. Frontend calls `/ai/chat` endpoint
3. LLM provider processes message
4. RAG engine retrieves relevant medical information
5. Response generated and displayed
6. Conversation stored in memory

### Analytics Generation
1. Various services collect operational data
2. Analytics service aggregates and calculates metrics
3. Dashboard page displays real-time insights
4. Charts and visualizations updated dynamically

---

## 🧪 Testing

### Run Backend Tests

```bash
cd BACKEND
pytest test.py -v
```

### Test Specific Module

```bash
pytest test.py::test_patient_creation -v
```

---

## 🐛 Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running locally or Atlas cluster is accessible
- Verify `MONGO_URI` in `.env` is correct
- Check internet connection for MongoDB Atlas

### JWT Authentication Errors
- Verify `JWT_SECRET_KEY` matches between backend and frontend
- Ensure token is not expired
- Check token is sent in `Authorization: Bearer <token>` format

### Streamlit Connection Issues
- Backend must be running on port 8000
- Check `BACKEND_URL` in frontend `.env`
- Verify CORS is properly configured

### LLM API Errors
- Ensure valid API keys are provided
- Check API key quotas and billing
- Verify internet connection for API calls

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc7519)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Google Gemini API Docs](https://ai.google.dev/docs)

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Create a feature branch (`git checkout -b feature/AmazingFeature`)
2. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
3. Push to the branch (`git push origin feature/AmazingFeature`)
4. Open a Pull Request

---

## 📞 Support & Contact

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the development team
- Check documentation at `/docs` on running application

---

## 🎉 Acknowledgments

- FastAPI community for the excellent framework
- MongoDB for reliable database solutions
- OpenAI & Google for LLM capabilities
- Streamlit for intuitive UI framework

---

**Last Updated**: February 22, 2026

**Version**: 1.0.0
