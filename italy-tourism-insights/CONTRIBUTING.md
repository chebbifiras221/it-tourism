# Contributing Guidelines

## How to Contribute

We welcome contributions to the Italian Tourism Intelligence Dashboard! Here's how to get involved:

### Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/italy-tourism-insights.git
   cd italy-tourism-insights
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up your environment**
   - Follow [SETUP.md](SETUP.md) for installation
   - Ensure all tests pass

### Development Workflow

1. **Make your changes**
   - Keep commits atomic and well-described
   - Follow existing code style
   - Add comments for complex logic

2. **Test your changes**
   ```bash
   # Backend
   cd backend
   pytest tests/

   # Frontend
   cd frontend
   npm run lint
   ```

3. **Push and create a Pull Request**
   - Provide clear description of changes
   - Reference related issues
   - Include before/after screenshots if UI changes

### Code Style

#### Python (Backend)
- Follow PEP 8
- Use type hints
- Write docstrings for functions/classes
- Keep functions focused and small

#### TypeScript/React (Frontend)
- Use functional components with hooks
- Maintain consistent naming conventions
- Document complex logic
- Keep components modular and reusable

#### Commit Messages
```
[FEATURE/FIX/DOCS] Brief description

Detailed explanation of changes made.
- Specific changes
- Related issues #123
```

### Areas for Contribution

#### Backend
- [ ] Add more ML models (XGBoost, Random Forest)
- [ ] Implement database connection pooling
- [ ] Add authentication/authorization
- [ ] Write unit tests
- [ ] Optimize database queries
- [ ] Add caching layer

#### Frontend
- [ ] Create additional dashboard pages
- [ ] Enhance visualizations
- [ ] Improve mobile responsiveness
- [ ] Add dark mode
- [ ] Performance optimization
- [ ] Add E2E tests

#### Data Science
- [ ] Improve forecasting accuracy
- [ ] Add new analytical features
- [ ] Collect real tourism data
- [ ] Build anomaly detection
- [ ] Create clustering models

#### Documentation
- [ ] Expand API documentation
- [ ] Create video tutorials
- [ ] Add architecture diagrams
- [ ] Write deployment guides
- [ ] Improve README

### Reporting Issues

When creating an issue, include:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Environment details (OS, Python version, Node version)

### Questions?

- Open an issue for discussion
- Check existing issues first
- Join our community discussions

---

Thank you for contributing to make tourism data intelligence better! 🇮🇹
