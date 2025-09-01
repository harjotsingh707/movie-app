# Movie Database App

## Overview

A Flask-based web application that provides movie search functionality using The Movie Database (TMDb) API. Users can search for movies by title and view detailed information about each film, including ratings, release dates, and descriptions. The application features a clean, responsive interface built with Bootstrap and includes error handling for API requests.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templating with Flask for server-side rendering
- **UI Framework**: Bootstrap 5 with dark theme for responsive design
- **JavaScript Enhancement**: Vanilla JavaScript for form handling, loading states, and user interactions
- **CSS Architecture**: Custom CSS layered on top of Bootstrap for movie-specific styling (cards, posters, ratings)

### Backend Architecture
- **Web Framework**: Flask with simple route-based architecture
- **Request Handling**: RESTful approach with GET/POST methods for search functionality
- **Error Handling**: Try-catch blocks for API failures with user-friendly error messages
- **Session Management**: Flask sessions with configurable secret key for flash messages

### Data Flow
- **Search Process**: Form submission → Flask route → TMDb API call → JSON response processing → template rendering
- **Image Handling**: TMDb image URLs constructed with base URL and poster paths
- **State Management**: Form data persistence and error state handling through Flask's request context

### Security Considerations
- **Environment Variables**: API keys and secrets stored as environment variables
- **Request Validation**: Input sanitization and query parameter validation
- **Timeout Protection**: HTTP request timeouts to prevent hanging requests

## External Dependencies

### Third-Party APIs
- **The Movie Database (TMDb) API**: Primary data source for movie information, ratings, and poster images
  - Search endpoint: `/search/movie`
  - Image service: `https://image.tmdb.org/t/p/w500`
  - Requires API key authentication

### Frontend Libraries
- **Bootstrap 5**: CSS framework from CDN for responsive design and components
- **Font Awesome 6.4.0**: Icon library for UI elements
- **Replit Bootstrap Agent Theme**: Custom dark theme variant

### Python Dependencies
- **Flask**: Web framework for routing and templating
- **Requests**: HTTP library for TMDb API communication
- **Standard Library**: `os` for environment variables, `logging` for debugging

### Development Environment
- **Static Assets**: CSS and JavaScript files served through Flask's static file handling
- **Template Structure**: Base template with block inheritance for consistent layout
- **Environment Configuration**: Development vs production settings through environment variables