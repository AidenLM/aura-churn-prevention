# Implementation Plan: AURA Customer Churn Prevention System

## Overview

This implementation plan breaks down the AURA dashboard into incremental coding tasks. The system will be built in phases: backend ML infrastructure first, then API layer, followed by frontend components, and finally integration and testing. Each task builds on previous work to ensure continuous progress with testable milestones.

## Tasks

- [x] 1. Set up project structure and development environment
  - Create Next.js 14+ project with TypeScript and App Router
  - Create FastAPI project with Python virtual environment
  - Configure Tailwind CSS with Jira/Atlassian color palette
  - Set up PostgreSQL database (local or managed)
  - Install dependencies: Framer Motion, Recharts, shadcn/ui, Zustand, XGBoost, SHAP, SQLAlchemy
  - Configure ESLint, Prettier, and Python linting tools
  - Create .env files for environment variables
  - Set up Git repository with .gitignore
  - _Requirements: All (foundational)_

- [x] 2. Implement database schema and models
  - [x] 2.1 Create PostgreSQL database schema
    - Write SQL migration for customers table with all required fields
    - Write SQL migration for predictions audit trail table
    - Write SQL migration for campaigns catalog table
    - Write SQL migration for users table
    - Create indexes for performance (customer_id, risk_level, timestamp)
    - _Requirements: 7.1, 7.5, 15.1_
  
  - [x] 2.2 Implement SQLAlchemy ORM models
    - Create Customer model with all fields and relationships
    - Create PredictionRecord model with JSON field for SHAP values
    - Create Campaign model for offer catalog
    - Create User model for authentication
    - _Requirements: 7.1, 15.1_
  
  - [ ]* 2.3 Write property test for customer data persistence
    - **Property 19: Customer Data Persistence Round-Trip**
    - **Validates: Requirements 7.1**
  
  - [ ]* 2.4 Write property test for referential integrity
    - **Property 22: Referential Integrity Enforcement**
    - **Validates: Requirements 7.5**


- [x] 3. Implement ML model infrastructure
  - [x] 3.1 Create ChurnPredictor service
    - Implement XGBoost model loading from disk
    - Implement predict() method with CustomerFeatures input
    - Implement predict_batch() for multiple customers
    - Add risk_level classification logic (Low/Medium/High thresholds)
    - _Requirements: 1.1, 1.2, 1.3_
  
  - [ ]* 3.2 Write property tests for ChurnPredictor
    - **Property 1: Risk Score Range Constraint**
    - **Property 2: Risk Level Classification Correctness**
    - **Property 3: Prediction Idempotence**
    - **Validates: Requirements 1.1, 1.2, 1.3**
  
  - [ ]* 3.3 Write property test for incomplete features handling
    - **Property 4: Incomplete Features Error Handling**
    - **Validates: Requirements 1.4**
  
  - [x] 3.4 Create ShapExplainer service
    - Initialize SHAP TreeExplainer with XGBoost model
    - Implement explain() method to generate SHAP values
    - Implement get_top_features() to extract top 5 features by importance
    - Add direction classification (positive/negative)
    - _Requirements: 2.1, 2.2_
  
  - [ ]* 3.5 Write property tests for SHAP explainer
    - **Property 5: SHAP Completeness**
    - **Property 6: Top Features Extraction**
    - **Validates: Requirements 2.1, 2.2**
  
  - [ ]* 3.6 Write property test for SHAP serialization
    - **Property 8: SHAP Serialization Round-Trip**
    - **Validates: Requirements 2.5**

- [x] 4. Implement offer recommendation engine
  - [x] 4.1 Create OfferOptimizer service
    - Load campaign catalog from database
    - Implement recommend() method with profile-based filtering
    - Implement rank_offers() to sort by expected effectiveness
    - Add Turkish rationale generation for recommendations
    - _Requirements: 14.1, 14.2, 14.3, 14.4_
  
  - [ ]* 4.2 Write property tests for offer optimizer
    - **Property 13: High-Risk Offer Recommendation**
    - **Property 45: Offer Profile Filtering**
    - **Property 46: Offer Ranking by Effectiveness**
    - **Property 47: Offer Details Completeness**
    - **Validates: Requirements 4.5, 14.2, 14.3, 14.4**

- [x] 5. Implement ROI simulation engine
  - [x] 5.1 Create ROISimulator service
    - Implement simulate() method with risk threshold and budget inputs
    - Calculate targeted_customers based on risk distribution
    - Calculate cost_per_customer, total_cost, expected_retention_rate
    - Calculate projected_revenue, roi, net_gain, coverage_percentage
    - _Requirements: 6.1, 6.2, 6.5_
  
  - [ ]* 5.2 Write property tests for ROI simulator
    - **Property 16: ROI Customer Count Calculation**
    - **Property 17: ROI Calculation Completeness**
    - **Property 18: ROI Parameter Sensitivity**
    - **Validates: Requirements 6.1, 6.2, 6.5**

- [x] 6. Checkpoint - Backend ML services complete
  - Ensure all ML service tests pass
  - Verify models can be loaded and make predictions
  - Ask the user if questions arise


- [x] 7. Implement data access layer
  - [x] 7.1 Create CustomerRepository
    - Implement get_by_id() to retrieve customer by ID
    - Implement get_high_risk_customers() with limit parameter
    - Implement get_random_customer() for demo purposes
    - Implement get_summary_stats() for dashboard metrics
    - Implement save_prediction() for audit trail
    - Add pagination support for bulk queries
    - _Requirements: 4.1, 7.1, 7.3, 15.1_
  
  - [ ]* 7.2 Write property tests for repository
    - **Property 10: Customer Profile Completeness**
    - **Property 20: Pagination Correctness**
    - **Validates: Requirements 4.1, 7.3**
  
  - [x] 7.3 Implement caching layer
    - Add Redis or in-memory cache for customer data
    - Implement 5-minute TTL for cached responses
    - Implement cache invalidation on customer updates
    - _Requirements: 10.4, 7.6_
  
  - [ ]* 7.4 Write property tests for caching
    - **Property 33: Response Caching Behavior**
    - **Property 23: Cache Invalidation on Update**
    - **Validates: Requirements 10.4, 7.6**

- [ ] 8. Implement authentication and authorization
  - [ ] 8.1 Create authentication service
    - Implement JWT token generation with user_id, role, exp claims
    - Implement JWT token validation middleware
    - Implement password hashing with bcrypt
    - Add role-based access control decorator
    - _Requirements: 13.1, 13.2, 13.3, 13.5_
  
  - [ ]* 8.2 Write property tests for authentication
    - **Property 41: JWT Token Generation**
    - **Property 42: JWT Token Validation**
    - **Property 43: Role-Based Access Control**
    - **Validates: Requirements 13.2, 13.3, 13.5**
  
  - [ ] 8.3 Implement audit logging
    - Create logging service for authentication attempts
    - Create logging service for API errors
    - Create logging service for predictions and recommendations
    - _Requirements: 13.7, 9.7, 15.1, 15.2_
  
  - [ ]* 8.4 Write property tests for audit logging
    - **Property 44: Authentication Audit Logging**
    - **Property 31: API Error Logging**
    - **Property 48: Prediction Audit Trail Completeness**
    - **Property 49: Offer Recommendation Logging**
    - **Validates: Requirements 13.7, 9.7, 15.1, 15.2**

- [x] 9. Implement FastAPI endpoints
  - [x] 9.1 Create dashboard endpoints
    - Implement GET /api/dashboard/summary
    - Return summary statistics (total customers, high-risk count, average risk, churn rate)
    - Return risk distribution data
    - Return top risky customers list
    - _Requirements: 3.3_
  
  - [x] 9.2 Create customer endpoints
    - Implement GET /api/customers/{customerId}
    - Implement GET /api/customers/high-risk with pagination
    - Implement GET /api/customers/random
    - Integrate ChurnPredictor and ShapExplainer
    - Integrate OfferOptimizer for high-risk customers
    - Generate Turkish AI insights
    - _Requirements: 4.1, 4.4, 4.5_
  
  - [x] 9.3 Create prediction endpoints
    - Implement POST /api/predict/calculate
    - Validate input with Pydantic models
    - Return risk score, SHAP values, AI analysis, and offer recommendation
    - _Requirements: 5.1, 5.2_
  
  - [x] 9.4 Create simulation endpoints
    - Implement POST /api/simulation/roi
    - Integrate ROISimulator service
    - Return all ROI metrics with Turkish Lira formatting
    - _Requirements: 6.1, 6.2, 6.3_
  
  - [ ]* 9.5 Write unit tests for API endpoints
    - Test request validation with invalid inputs
    - Test successful responses with mock data
    - Test error handling for database failures
    - _Requirements: 1.4, 5.1, 7.4_


- [ ] 10. Implement error handling and localization
  - [ ] 10.1 Create error handling middleware
    - Implement global exception handler for FastAPI
    - Return standardized JSON error responses
    - Map validation errors to field names
    - Add Turkish error messages for all error types
    - _Requirements: 9.5, 12.2_
  
  - [ ]* 10.2 Write property tests for error handling
    - **Property 30: Standardized Error Response Format**
    - **Property 38: Turkish Backend Responses**
    - **Validates: Requirements 9.5, 12.2**
  
  - [ ] 10.3 Implement Turkish localization utilities
    - Create date formatting function (DD.MM.YYYY)
    - Create number formatting function (Turkish separators)
    - Create currency formatting function (₺ symbol)
    - Create Turkish month/day name mappings
    - _Requirements: 12.3, 12.4, 12.5_
  
  - [ ]* 10.4 Write property tests for localization
    - **Property 39: Turkish Date Formatting**
    - **Property 40: Turkish Number Formatting**
    - **Property 9: Turkish Currency Formatting**
    - **Validates: Requirements 12.3, 12.4, 3.7**

- [ ] 11. Checkpoint - Backend API complete
  - Ensure all API endpoints are functional
  - Test with Postman or curl
  - Verify Turkish localization in responses
  - Ask the user if questions arise

- [ ] 12. Set up Next.js frontend structure
  - [ ] 12.1 Create app directory structure
    - Create app/(auth)/login page
    - Create app/(dashboard)/page.tsx for homepage
    - Create app/(dashboard)/customers/[id]/page.tsx for customer detail
    - Create app/(dashboard)/calculator/page.tsx for risk calculator
    - Create app/(dashboard)/simulation/page.tsx for campaign simulation
    - Create app/api routes for backend proxy
    - _Requirements: 3.1, 4.1, 5.1, 6.1_
  
  - [ ] 12.2 Configure Tailwind CSS
    - Add Jira/Atlassian color palette to tailwind.config.js
    - Add custom animations (floatOrb, fadeInUp, slideInRight/Left, pulse)
    - Add glassmorphism utility classes
    - Configure responsive breakpoints (mobile ≤968px)
    - _Requirements: 3.1, 8.1, 8.2_
  
  - [ ] 12.3 Set up Zustand state management
    - Create app store with user, summaryStats, currentCustomer state
    - Add actions for setUser, setSummaryStats, setCurrentCustomer
    - Add loading and error state management
    - _Requirements: All (state management)_

- [ ] 13. Implement shared UI components
  - [ ] 13.1 Create base components with shadcn/ui
    - Install and configure shadcn/ui
    - Create Button component with variants
    - Create Input component with validation states
    - Create Card component with glassmorphism
    - Create Badge component for risk levels
    - Create Avatar component for customer photos
    - _Requirements: 3.1, 4.3_
  
  - [ ] 13.2 Create Turkish localization utilities
    - Create useTranslation hook for Turkish strings
    - Create formatCurrency function with ₺ symbol
    - Create formatDate function (DD.MM.YYYY)
    - Create formatNumber function (Turkish separators)
    - _Requirements: 3.6, 3.7, 12.1, 12.3, 12.4_
  
  - [ ]* 13.3 Write property tests for formatting utilities
    - **Property 9: Turkish Currency Formatting**
    - **Property 39: Turkish Date Formatting**
    - **Property 40: Turkish Number Formatting**
    - **Validates: Requirements 3.7, 12.3, 12.4**


- [ ] 14. Implement homepage (Ana Sayfa)
  - [x] 14.1 Create hero section component
    - Implement full-screen (100vh) hero with dark blue gradient
    - Add animated floating orbs with Framer Motion (floatOrb animation)
    - Create two-column layout (text left, chat mockup right)
    - Add stats badge with pulsing green dot
    - Add CTA buttons with hover effects
    - _Requirements: 3.1, 3.2_
  
  - [x] 14.2 Create summary statistics section
    - Fetch data from /api/dashboard/summary
    - Create 4 metric cards (total customers, high-risk count, average risk, churn rate)
    - Add fadeInUp animations on scroll
    - Format numbers with Turkish conventions
    - _Requirements: 3.3, 3.7_
  
  - [ ] 14.3 Create dashboard gadgets with charts
    - Implement risk distribution histogram with Recharts/Plotly
    - Implement top risky customers bar chart
    - Add chart interactions (hover tooltips)
    - Use consistent color scheme (red/yellow/green for risk levels)
    - _Requirements: 3.4, 11.1, 11.2, 11.6_
  
  - [ ] 14.4 Create feature cards section
    - Create 4 feature cards with gradient backgrounds
    - Add hover effects and icons
    - Implement reveal-on-scroll animations with Intersection Observer
    - _Requirements: 3.5_
  
  - [ ]* 14.5 Write unit tests for homepage components
    - Test summary stats rendering with mock data
    - Test chart rendering with mock data
    - Test animations trigger on scroll
    - _Requirements: 3.3, 3.4_

- [ ] 15. Implement customer detail page (Müşteri Detayı)
  - [x] 15.1 Create sticky sidebar with search modes
    - Implement 3 search modes: high-risk filter, random selection, manual ID input
    - Add mode switching UI
    - Fetch customer data based on selected mode
    - _Requirements: 4.2_
  
  - [x] 15.2 Create customer header component
    - Display avatar, name, customer ID
    - Display risk badge with color coding (red/yellow/green)
    - Add slideInRight animation
    - _Requirements: 4.3_
  
  - [x] 15.3 Create customer info cards
    - Create plan details card (type, monthly charge)
    - Create tenure card with icon
    - Create monthly bill card with Turkish Lira formatting
    - Add glassmorphism effects
    - _Requirements: 4.3, 3.7_
  
  - [x] 15.4 Create AI insights section
    - Fetch AI insights from backend
    - Display natural language explanation in Turkish
    - Add icon and styling
    - _Requirements: 4.4_
  
  - [x] 15.5 Create SHAP chart component
    - Implement horizontal bar chart with Recharts
    - Color code bars (red for negative, green for positive impact)
    - Display feature names in Turkish
    - Add hover tooltips with exact values
    - _Requirements: 4.6, 11.3_
  
  - [x] 15.6 Create recommended offer card
    - Display campaign name, discount, duration
    - Display estimated cost in Turkish Lira
    - Display rationale in Turkish
    - Show only for high-risk customers
    - _Requirements: 4.5_
  
  - [ ]* 15.7 Write property tests for customer detail rendering
    - **Property 11: Customer Display Field Completeness**
    - **Property 14: SHAP Color Coding**
    - **Validates: Requirements 4.3, 4.6**


- [ ] 16. Implement risk calculator page (Risk Hesapla)
  - [ ] 16.1 Create 3-column form layout
    - Create profile column (tenure, plan type, monthly charge)
    - Create usage column (data usage, voice minutes, SMS count)
    - Create risk indicators column (complaints, support calls, payment delays, contract type)
    - Add Turkish labels for all fields
    - _Requirements: 5.6_
  
  - [ ] 16.2 Implement form validation
    - Add client-side validation for required fields
    - Add validation for numeric ranges
    - Display field-specific errors in Turkish
    - Highlight invalid fields with red borders
    - _Requirements: 5.5_
  
  - [ ] 16.3 Implement risk calculation
    - Submit form to POST /api/predict/calculate
    - Display loading indicator during calculation
    - Display risk score with animated progress ring
    - Display risk level badge
    - _Requirements: 5.2_
  
  - [ ] 16.4 Display SHAP analysis and AI insights
    - Render SHAP chart with feature importance
    - Display AI analysis text in Turkish
    - Show offer recommendation for high-risk scenarios
    - _Requirements: 5.3, 5.4_
  
  - [ ]* 16.5 Write property test for form validation
    - **Property 15: Risk Calculator Input Validation**
    - **Validates: Requirements 5.1, 5.5**

- [x] 17. Implement campaign simulation page (Kampanya Simülasyonu)
  - [x] 17.1 Create simulation input controls
    - Create risk threshold slider (0-1) with labels
    - Create campaign budget input with Turkish Lira formatting
    - Add real-time value display
    - _Requirements: 6.1, 6.2_
  
  - [x] 17.2 Implement simulation calculation
    - Submit params to POST /api/simulation/roi
    - Display loading indicator
    - Handle errors gracefully
    - _Requirements: 6.2_
  
  - [x] 17.3 Create results panel
    - Display 4 key metrics cards (targeted customers, total cost, ROI %, net gain)
    - Format currency values in Turkish Lira
    - Add animations on result update
    - _Requirements: 6.3_
  
  - [x] 17.4 Create coverage visualization
    - Implement progress bar showing customer base coverage percentage
    - Add color coding (green for good coverage, yellow for moderate, red for low)
    - Display percentage label
    - _Requirements: 6.7_
  
  - [ ]* 17.5 Write property tests for ROI display
    - **Property 17: ROI Calculation Completeness**
    - **Validates: Requirements 6.2, 6.3**

- [ ] 18. Checkpoint - Frontend pages complete
  - Test all pages in browser
  - Verify Turkish localization throughout
  - Verify responsive design on mobile and desktop
  - Ask the user if questions arise


- [ ] 19. Implement accessibility features
  - [ ] 19.1 Add WCAG AA color contrast compliance
    - Audit all color combinations
    - Adjust colors to meet 4.5:1 ratio for normal text
    - Adjust colors to meet 3:1 ratio for large text
    - _Requirements: 8.3_
  
  - [ ]* 19.2 Write property test for color contrast
    - **Property 24: WCAG AA Color Contrast**
    - **Validates: Requirements 8.3**
  
  - [ ] 19.3 Implement keyboard navigation
    - Add visible focus indicators to all interactive elements
    - Ensure logical tab order
    - Add keyboard shortcuts for common actions
    - _Requirements: 8.5_
  
  - [ ]* 19.4 Write property test for focus indicators
    - **Property 25: Keyboard Focus Indicators**
    - **Validates: Requirements 8.5**
  
  - [ ] 19.5 Add ARIA attributes
    - Add alt text to all images
    - Add aria-labels to icon buttons
    - Add aria-live regions for dynamic content
    - Add role attributes where needed
    - _Requirements: 8.6, 8.7_
  
  - [ ]* 19.6 Write property tests for accessibility attributes
    - **Property 26: Image Accessibility Attributes**
    - **Property 27: Dynamic Content Announcements**
    - **Validates: Requirements 8.6, 8.7**
  
  - [ ] 19.7 Implement reduced motion support
    - Add prefers-reduced-motion media query
    - Disable animations when user prefers reduced motion
    - Maintain functionality without animations
    - _Requirements: 8.4_

- [x] 20. Implement responsive design
  - [x] 20.1 Create mobile layouts (≤968px)
    - Stack hero section columns vertically
    - Make sidebar collapsible
    - Stack form columns vertically
    - Adjust chart sizes for mobile
    - _Requirements: 8.1_
  
  - [x] 20.2 Create desktop layouts (>968px)
    - Multi-column grids for dashboard
    - Side-by-side layouts for customer detail
    - 3-column form for risk calculator
    - _Requirements: 8.2_
  
  - [ ]* 20.3 Write unit tests for responsive behavior
    - Test layout changes at breakpoint
    - Test mobile navigation
    - _Requirements: 8.1, 8.2_

- [ ] 21. Implement API communication layer
  - [ ] 21.1 Create API client utilities
    - Create fetch wrapper with authentication headers
    - Implement request/response interceptors
    - Add retry logic for transient failures
    - Add timeout handling
    - _Requirements: 9.1, 9.2_
  
  - [ ]* 21.2 Write property test for auth headers
    - **Property 28: Authentication Header Presence**
    - **Validates: Requirements 9.1**
  
  - [ ] 21.3 Implement error handling
    - Map backend validation errors to form fields
    - Display user-friendly Turkish error messages
    - Show retry UI for network errors
    - Show maintenance page for backend unavailability
    - _Requirements: 9.2, 9.3, 9.4_
  
  - [ ]* 21.4 Write property test for error mapping
    - **Property 29: Validation Error Field Mapping**
    - **Validates: Requirements 9.3**
  
  - [ ] 21.5 Implement loading states
    - Show loading indicators for API calls >3 seconds
    - Show skeleton loaders for data fetching
    - Disable form submissions during loading
    - _Requirements: 9.6_


- [ ] 22. Implement performance optimizations
  - [ ] 22.1 Configure Next.js optimizations
    - Enable code splitting for routes
    - Configure lazy loading for chart libraries
    - Optimize images with Next.js Image component
    - Enable SSR for initial page load
    - _Requirements: 10.2, 10.6, 10.7_
  
  - [ ]* 22.2 Write property test for Image component usage
    - **Property 34: Next.js Image Component Usage**
    - **Validates: Requirements 10.7**
  
  - [ ] 22.3 Optimize animations
    - Ensure all animations use only transform and opacity
    - Add will-change hints for animated elements
    - Implement animation throttling
    - _Requirements: 10.3_
  
  - [ ]* 22.4 Write property test for animation properties
    - **Property 32: Animation Property Restriction**
    - **Validates: Requirements 10.3**
  
  - [ ] 22.5 Implement request batching
    - Batch multiple API requests where possible
    - Implement request deduplication
    - Add request caching on frontend
    - _Requirements: 10.5_

- [ ] 23. Implement authentication UI
  - [ ] 23.1 Create login page
    - Create login form with username and password
    - Add form validation
    - Handle authentication errors
    - Redirect to dashboard on success
    - _Requirements: 13.1_
  
  - [ ] 23.2 Implement token management
    - Store JWT token in httpOnly cookie or localStorage
    - Add token to all API requests
    - Handle token expiration
    - Redirect to login on 401 errors
    - _Requirements: 13.2, 13.3, 13.4_
  
  - [ ] 23.3 Implement protected routes
    - Create authentication guard for dashboard routes
    - Redirect unauthenticated users to login
    - Preserve intended destination for post-login redirect
    - _Requirements: 13.1_
  
  - [ ]* 23.4 Write unit tests for authentication flow
    - Test login form submission
    - Test token storage and retrieval
    - Test redirect on authentication failure
    - _Requirements: 13.1, 13.4_

- [ ] 24. Implement audit trail and reporting
  - [ ] 24.1 Create prediction history endpoint
    - Implement GET /api/predictions/history with pagination
    - Sort by timestamp descending
    - Filter by customer_id, date range, risk_level
    - _Requirements: 15.3_
  
  - [ ]* 24.2 Write property test for history ordering
    - **Property 50: Prediction History Ordering**
    - **Validates: Requirements 15.3**
  
  - [ ] 24.3 Implement CSV export functionality
    - Create GET /api/predictions/export endpoint
    - Generate CSV with all prediction fields
    - Include proper headers and escaping
    - _Requirements: 15.5_
  
  - [ ]* 24.4 Write property test for CSV export
    - **Property 51: CSV Export Validity**
    - **Validates: Requirements 15.5**
  
  - [ ] 24.5 Implement user tracking
    - Add user_id to all prediction records
    - Add user_id to all offer recommendation logs
    - _Requirements: 15.6_
  
  - [ ]* 24.6 Write property test for user tracking
    - **Property 52: Prediction User Tracking**
    - **Validates: Requirements 15.6**


- [x] 25. Implement chart components
  - [x] 25.1 Create risk distribution histogram
    - Use Recharts or Plotly for histogram
    - Display customer count by risk level (Low/Medium/High)
    - Add hover tooltips with exact counts
    - Use consistent color scheme (red/yellow/green)
    - _Requirements: 11.1, 11.6_
  
  - [x] 25.2 Create top risky customers bar chart
    - Display customer names and risk scores
    - Sort by risk score descending
    - Add click interaction to navigate to customer detail
    - _Requirements: 11.2, 11.4_
  
  - [x] 25.3 Create SHAP feature importance chart
    - Implement horizontal bar chart
    - Color code by direction (red negative, green positive)
    - Display Turkish feature names
    - Add hover tooltips
    - _Requirements: 11.3_
  
  - [ ]* 25.4 Write property tests for chart rendering
    - **Property 35: Chart Color Consistency**
    - **Property 36: Chart Responsiveness**
    - **Validates: Requirements 11.6, 11.7**

- [ ] 26. Integration and end-to-end wiring
  - [x] 26.1 Connect frontend to backend API
    - Configure API base URL in environment variables
    - Test all API endpoints from frontend
    - Verify data flows correctly through all pages
    - _Requirements: All_
  
  - [x] 26.2 Seed database with sample data
    - Create seed script for customers table
    - Create seed script for campaigns catalog
    - Create seed script for users table
    - Generate diverse customer profiles for testing
    - _Requirements: 7.1_
  
  - [x] 26.3 Test complete user flows
    - Test homepage → customer detail flow
    - Test risk calculator flow
    - Test campaign simulation flow
    - Test authentication flow
    - _Requirements: All_
  
  - [ ]* 26.4 Write integration tests
    - Test end-to-end prediction flow
    - Test end-to-end offer recommendation flow
    - Test end-to-end ROI simulation flow
    - _Requirements: 1.1, 4.5, 6.2_

- [ ] 27. Final polish and deployment preparation
  - [ ] 27.1 Add error boundaries
    - Create error boundary components
    - Add fallback UI for component errors
    - Log errors to monitoring service
    - _Requirements: 9.2_
  
  - [x] 27.2 Implement loading states and skeletons
    - Add skeleton loaders for all data-fetching components
    - Add loading spinners for actions
    - Add progress indicators for multi-step processes
    - _Requirements: 9.6_
  
  - [ ] 27.3 Add Turkish content throughout
    - Verify all UI text is in Turkish
    - Verify all error messages are in Turkish
    - Verify all AI insights are in Turkish
    - _Requirements: 3.6, 12.1, 12.2_
  
  - [ ]* 27.4 Write property test for Turkish UI
    - **Property 37: Turkish UI Text**
    - **Validates: Requirements 3.6, 12.1**
  
  - [ ] 27.5 Configure deployment
    - Set up Vercel project for frontend
    - Set up Railway/Render for backend
    - Configure environment variables
    - Set up managed PostgreSQL database
    - Configure CORS for production
    - _Requirements: All (deployment)_

- [ ] 28. Final checkpoint - System complete
  - Run all tests (unit, property, integration)
  - Test on multiple browsers and devices
  - Verify accessibility with screen reader
  - Verify performance metrics
  - Ask the user if questions arise

## Notes

- Tasks marked with `*` are optional property-based and unit tests that can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation at major milestones
- Property tests validate universal correctness properties with minimum 100 iterations
- Unit tests validate specific examples, edge cases, and error conditions
- Turkish localization is critical throughout - all user-facing text must be in Turkish
- Accessibility compliance (WCAG AA) is mandatory for all UI components
- Performance optimizations should be implemented progressively
