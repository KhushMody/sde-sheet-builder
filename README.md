# SDE Sheet Builder 🚀

[![CI/CD Pipeline](https://github.com/yourusername/sde-sheet-builder/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/yourusername/sde-sheet-builder/actions/workflows/ci-cd.yml)
[![codecov](https://codecov.io/gh/yourusername/sde-sheet-builder/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/sde-sheet-builder)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An intelligent web application that helps software engineers create personalized LeetCode practice sheets based on company preferences, difficulty levels, and specific topics. Built with React, Flask, PostgreSQL, and powered by AI for intelligent question selection.

## 🌟 Features

- **AI-Powered Question Selection**: Uses Groq LLM to intelligently parse user queries and select relevant questions
- **Company-Specific Practice**: Get questions frequently asked by top tech companies
- **Topic-Based Filtering**: Focus on specific data structures and algorithms topics
- **Difficulty Customization**: Choose from Easy, Medium, or Hard difficulty levels
- **Real-time Results**: Get instant, curated question lists with direct LeetCode links
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│───▶│  Flask Backend  │───▶│  PostgreSQL DB  │
│   (Port 3000)   │    │   (Port 5000)   │    │   (Port 5432)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   Groq LLM API  │
                    │  (AI Processing)│
                    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 16+ (for local development)
- Python 3.10+ (for local development)
- Git

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/sde-sheet-builder.git
   cd sde-sheet-builder
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - Database: localhost:5432

### Local Development Setup

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   export DATABASE_URL="postgresql://username:password@localhost:5432/interview_prep"
   export GROQ_API_KEY="your_groq_api_key"
   ```

5. **Run the Flask application**
   ```bash
   flask run --debug
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend-interview-prep
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the React application**
   ```bash
   npm start
   ```

## 📖 Usage

### Basic Usage

1. **Open the application** in your browser at `http://localhost:3000`

2. **Enter your query** in natural language, for example:
   - "I want 10 medium difficulty array questions from Google"
   - "Give me 5 easy graph questions for Amazon interview prep"
   - "Create a sheet with hard dynamic programming questions from Microsoft"

3. **Get instant results** with a curated list of questions including:
   - Question titles
   - Difficulty levels
   - Acceptance rates
   - Direct links to LeetCode

### Query Examples

```
✅ "I want a SDE sheet for Google with 10 medium array questions"
✅ "Give me 5 easy tree problems from Amazon"
✅ "Create 15 hard dynamic programming questions for Facebook"
✅ "Show me medium graph questions from Microsoft, need 8 problems"
```

## 🛠️ API Documentation

### Endpoints

#### `POST /api/analyze`

Analyzes user query and returns curated question list.

**Request Body:**
```json
{
  "question": "I want 10 medium array questions from Google"
}
```

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "company": "google",
      "question": "Two Sum",
      "acceptance": "49.1%",
      "difficulty": "Medium",
      "question_link": "https://leetcode.com/problems/two-sum/"
    }
  ],
  "question": "I want 10 medium array questions from Google"
}
```

## 🗄️ Database Schema

### Questions Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| company | VARCHAR(100) | Company name (e.g., 'google', 'amazon') |
| question | TEXT | Question title |
| acceptance | VARCHAR(50) | Acceptance rate (e.g., '49.1%') |
| difficulty | VARCHAR(50) | Difficulty level (Easy/Medium/Hard) |
| question_link | TEXT | Direct LeetCode URL |

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=postgresql://myuser:mypassword@database:5432/interview_prep
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=interview_prep

# API Keys
GROQ_API_KEY=your_groq_api_key_here
GITHUB_TOKEN=your_github_token_for_data_population

# Production Settings
FLASK_ENV=production
NODE_ENV=production
```

### Supported Companies

The application currently supports questions from major tech companies including:
- Google
- Amazon
- Microsoft
- Facebook/Meta
- Apple
- Netflix
- Uber
- Airbnb
- And many more...

## 🧪 Testing

### Backend Tests

```bash
cd backend
python -m pytest tests/ -v --cov=.
```

### Frontend Tests

```bash
cd frontend-interview-prep
npm test -- --coverage
```

### Integration Tests

```bash
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

## 🚀 Deployment

### Production Deployment on AWS EC2

1. **Set up EC2 instance** with Docker and Docker Compose
2. **Configure security groups** for ports 80, 443, 22
3. **Set up domain and SSL** (optional but recommended)
4. **Deploy using Docker Compose**:

```bash
# On EC2 instance
git clone https://github.com/yourusername/sde-sheet-builder.git
cd sde-sheet-builder
cp .env.example .env
# Configure production environment variables
docker-compose -f docker-compose.prod.yml up -d
```

### CI/CD Pipeline

The project includes a comprehensive GitHub Actions pipeline that:

- ✅ Runs automated tests for both frontend and backend
- 🔍 Performs code quality checks and security scans
- 🐳 Builds and pushes Docker images
- 🚀 Deploys to production automatically on main branch pushes
- 📢 Sends deployment notifications

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Run tests**: `npm test` and `pytest`
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Code Style

- **Python**: Follow PEP 8, use Black for formatting
- **JavaScript/React**: Use ESLint and Prettier
- **Commit Messages**: Use conventional commit format

## 📊 Performance & Monitoring

- **Response Time**: < 2 seconds for typical queries
- **Database**: Optimized with proper indexing
- **Caching**: Redis caching for frequently accessed data
- **Monitoring**: Application metrics via Prometheus/Grafana
- **Logging**: Structured logging with ELK stack

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check if PostgreSQL is running
docker-compose ps
# Restart database service
docker-compose restart database
```

**LLM API Errors**
- Verify your GROQ_API_KEY is valid
- Check API rate limits
- Ensure network connectivity

**Frontend Not Loading**
- Check if backend is running on port 5000
- Verify CORS configuration
- Check browser console for errors

## 🔮 Roadmap

- [ ] **AI Chat Interface**: Natural language conversation for question selection
- [ ] **Progress Tracking**: Save and track solving progress
- [ ] **Difficulty Analysis**: AI-powered difficulty assessment
- [ ] **Custom Topics**: User-defined topic categories
- [ ] **Mobile App**: React Native mobile application
- [ ] **Social Features**: Share and collaborate on practice sheets
- [ ] **Interview Simulation**: Mock interview environment

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Khush Mody** - *Initial work* - [@khushmody](https://github.com/khushmody)

## 🙏 Acknowledgments

- [LeetCode](https://leetcode.com/) for providing the problem database
- [Groq](https://groq.com/) for AI/LLM capabilities
- [krishnadey30/LeetCode-Questions-CompanyWise](https://github.com/krishnadey30/LeetCode-Questions-CompanyWise) for company-wise question data
- Open source community for amazing tools and libraries

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/sde-sheet-builder/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/sde-sheet-builder/discussions)
- **Email**: your.email@example.com

---

⭐ **Star this repo** if you find it helpful! It motivates us to keep improving.

**Happy Coding! 🎯**