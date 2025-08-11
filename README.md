# RE VLab - Requirements Engineering Virtual Laboratory

A comprehensive web-based virtual laboratory for Requirements Engineering education, designed to provide students with hands-on experience in requirements elicitation, analysis, and documentation through interactive scenarios.

## 🚀 Quick Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fthejadex%2FRE-VLab&env=SECRET_KEY,DEBUG&envDescription=Required%20environment%20variables%20for%20Django&envLink=https%3A%2F%2Fdocs.djangoproject.com%2Fen%2F4.2%2Fref%2Fsettings%2F&project-name=re-vlab&repository-name=RE-VLab)

**Environment Variables Required:**
- `SECRET_KEY`: Your Django secret key (generate a long random string)
- `DEBUG`: Set to `False` for production

**Default Admin Login:** admin/admin123

## 🎯 Project Overview

RE VLab is an innovative educational platform that transforms traditional requirements engineering learning into an immersive, interactive experience. The system provides students with realistic software project scenarios where they can practice requirements gathering, classification, and documentation under expert guidance.

## ✨ Key Features

### For Students
- **Interactive Scenarios**: Engage with realistic software project scenarios
- **Requirements Elicitation**: Practice identifying and classifying requirements
- **Progress Tracking**: Monitor learning progress and completion status
- **Expert Feedback**: Receive detailed feedback from instructors
- **Real-time Notifications**: Stay updated with system notifications

### For Administrators
- **Scenario Management**: Create, edit, and manage learning scenarios
- **Student Oversight**: Monitor student progress and submissions
- **Feedback System**: Provide comprehensive feedback to students
- **Analytics Dashboard**: Track system usage and student performance

## 🛠 Technology Stack

### Backend
- **Django 5.2.4** - Python web framework
- **SQLite** - Database (development)
- **Django ORM** - Database operations
- **Django Forms** - Data validation
- **Django Authentication** - User management

### Frontend
- **HTML5, CSS3, JavaScript** - Core web technologies
- **Tailwind CSS** - Utility-first CSS framework
- **Alpine.js** - Lightweight reactive framework
- **Font Awesome** - Icon library
- **Responsive Design** - Mobile-first approach

### Architecture
- **MVT Pattern** - Model-View-Template architecture
- **RESTful Design** - API design principles
- **Context Processors** - Global template data
- **Template Inheritance** - Code reusability

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd requirements-lab
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

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open browser and navigate to `http://127.0.0.1:8000`
   - Login with admin credentials to access admin panel

## 📁 Project Structure

```
requirements-lab/
├── lab/                    # Main Django app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── forms.py           # Django forms
│   ├── urls.py            # URL patterns
│   └── admin.py           # Admin interface
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   └── lab/               # App-specific templates
├── static/                # Static files (CSS, JS, images)
├── requirements.txt       # Python dependencies
├── manage.py             # Django management script
└── README.md             # Project documentation
```

## 🗄 Database Models

### Core Models
- **UserProfile**: Extended user model with role-based access
- **Scenario**: Learning scenarios with difficulty levels
- **ScenarioSubmission**: Student submissions and progress tracking
- **Requirement**: Requirements with type classification
- **Feedback**: Instructor feedback system
- **Notification**: User notification system

### Key Relationships
- Students can work on multiple scenarios
- Each submission contains multiple requirements
- Admins provide feedback on submissions
- Notifications keep users informed

## 🔐 User Roles & Permissions

### Student Role
- Browse and select scenarios
- Add requirements (functional, non-functional, business)
- Submit scenarios for review
- View feedback and notifications
- Track learning progress

### Admin Role
- Create and manage scenarios
- Review student submissions
- Provide detailed feedback
- Monitor system analytics
- Manage user accounts

## 🎨 User Interface Features

### Responsive Design
- Mobile-first approach
- Cross-device compatibility
- Touch-friendly interactions
- Adaptive layouts

### Theme System
- Light/dark mode toggle
- Persistent preferences
- Smooth transitions
- Accessibility compliance

### Navigation
- Sidebar navigation (desktop)
- Mobile hamburger menu
- Breadcrumb navigation
- Context-aware routing

## 📊 Dashboard Features

### Student Dashboard
- Progress overview
- Active scenarios
- Recent activities
- Feedback notifications
- Learning statistics

### Admin Dashboard
- System statistics
- Recent submissions
- Pending reviews
- User analytics
- Quick actions

## 🔔 Notification System

### Real-time Notifications
- Unread notification indicators
- Notification badges
- Context-aware alerts
- User preference management

### Notification Types
- New feedback received
- Submission status updates
- System announcements
- Progress milestones

## 🛡 Security Features

### Authentication & Authorization
- CSRF protection
- Session security
- Role-based access control
- Password security

### Data Validation
- Input sanitization
- SQL injection prevention
- XSS protection
- File upload security

## 🧪 Testing

### Running Tests
```bash
python manage.py test
```

### Test Coverage
- Unit tests for models and views
- Integration tests for workflows
- User acceptance testing
- Cross-browser compatibility

## 🚀 Deployment

### Development
- Local development server
- SQLite database
- Debug mode enabled
- Static file serving

### Production
- Configure production database
- Set up static file collection
- Configure environment variables
- Enable security settings

## 📈 Performance Optimization

### Database Optimization
- Efficient query design
- Index optimization
- Query caching
- Connection pooling

### Frontend Optimization
- Asset minification
- Image optimization
- Lazy loading
- Caching strategies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Project Team** - Initial work
- **Requirements Engineering Lab** - Educational platform

## 🙏 Acknowledgments

- Django community for the excellent framework
- Tailwind CSS for the utility-first styling
- Font Awesome for the icon library
- Educational institutions for feedback and testing

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Version History

### v1.0.0 (Current)
- Initial release
- Core functionality implemented
- Student and admin interfaces
- Notification system
- Responsive design

### Planned Features
- Advanced analytics
- API endpoints
- Mobile application
- Integration with LMS systems

---

**RE VLab** - Transforming Requirements Engineering Education Through Virtual Laboratories
