# Requirements Document: AURA Customer Churn Prevention System

## Introduction

The AURA Customer Churn Prevention System is an AI-powered dashboard designed for telecom companies to predict customer churn, provide actionable insights through machine learning explainability, and recommend targeted retention campaigns. The system combines a modern Next.js frontend with a FastAPI backend serving XGBoost models, delivering real-time risk assessments and ROI-optimized campaign recommendations. All content is localized in Turkish with currency displayed in Turkish Lira (₺).

## Glossary

- **System**: The AURA Customer Churn Prevention System (frontend + backend)
- **Frontend**: Next.js 14+ application with TypeScript and Tailwind CSS
- **Backend**: FastAPI service with ML model serving capabilities
- **ML_Model**: XGBoost-based churn prediction model
- **SHAP_Explainer**: Model explainability component using SHAP values
- **Offer_Optimizer**: Component that recommends retention campaigns
- **ROI_Simulator**: Component that calculates campaign budget scenarios
- **Customer**: Telecom subscriber whose churn risk is being assessed
- **Risk_Score**: Numerical value (0-1) indicating churn probability
- **Risk_Level**: Categorical classification (Low/Medium/High) based on Risk_Score
- **Campaign**: Retention offer designed to prevent customer churn
- **Dashboard**: Web interface displaying analytics and customer insights
- **User**: Telecom company employee using the system

## Requirements

### Requirement 1: Customer Churn Prediction

**User Story:** As a retention manager, I want to predict which customers are likely to churn, so that I can proactively intervene with targeted campaigns.

#### Acceptance Criteria

1. WHEN the Backend receives a customer data request, THE ML_Model SHALL generate a Risk_Score between 0 and 1
2. WHEN a Risk_Score is calculated, THE System SHALL classify it into Risk_Level categories (Low: 0-0.3, Medium: 0.3-0.7, High: 0.7-1.0)
3. WHEN multiple customers are processed, THE ML_Model SHALL maintain prediction consistency for identical input features
4. WHEN customer features are incomplete, THE Backend SHALL return a descriptive error message indicating missing fields
5. THE ML_Model SHALL process prediction requests within 500ms for single customers

### Requirement 2: Model Explainability with SHAP

**User Story:** As a retention manager, I want to understand why a customer is predicted to churn, so that I can address the specific factors driving their risk.

#### Acceptance Criteria

1. WHEN a Risk_Score is generated, THE SHAP_Explainer SHALL produce feature importance values for all input features
2. WHEN SHAP values are calculated, THE System SHALL identify the top 5 features contributing most to the prediction
3. WHEN displaying SHAP results, THE Frontend SHALL visualize feature importance with directional indicators (positive/negative impact)
4. THE SHAP_Explainer SHALL generate explanations within 1 second of prediction completion
5. WHEN SHAP values are serialized, THE Backend SHALL format them as JSON with feature names and impact scores

### Requirement 3: Homepage Dashboard Display

**User Story:** As a user, I want to see an overview of churn metrics and system capabilities, so that I can quickly assess the current situation and navigate to detailed features.

#### Acceptance Criteria

1. WHEN the homepage loads, THE Frontend SHALL display a full-screen hero section with glassmorphism effects
2. WHEN the hero section renders, THE System SHALL animate floating orbs using the floatOrb animation
3. WHEN summary statistics are requested, THE Backend SHALL return current metrics (total customers, high-risk count, average risk, monthly churn rate)
4. WHEN dashboard gadgets load, THE Frontend SHALL render interactive Plotly charts showing risk distribution and top risky customers
5. WHEN the user scrolls, THE Frontend SHALL trigger reveal-on-scroll animations for feature cards
6. THE Frontend SHALL display all text content in Turkish language
7. THE Frontend SHALL format all currency values in Turkish Lira (₺) with proper thousand separators

### Requirement 4: Customer Detail View

**User Story:** As a retention manager, I want to view detailed information about a specific customer including their risk factors and recommended actions, so that I can make informed retention decisions.

#### Acceptance Criteria

1. WHEN a customer ID is provided, THE Backend SHALL retrieve complete customer profile data from PostgreSQL
2. WHEN customer data is loaded, THE Frontend SHALL display a sticky sidebar with 3 search modes (high-risk, random, manual ID)
3. WHEN displaying customer information, THE Frontend SHALL show avatar, name, ID, Risk_Level badge, plan details, tenure, and monthly bill
4. WHEN AI insights are generated, THE System SHALL produce natural language explanations of churn factors in Turkish
5. WHEN a customer has high risk, THE Offer_Optimizer SHALL recommend the most suitable retention campaign
6. WHEN the SHAP chart renders, THE Frontend SHALL display feature importance bars with color coding (red for negative, green for positive impact)
7. WHEN customer data is not found, THE System SHALL display a user-friendly error message in Turkish

### Requirement 5: Risk Calculator for Hypothetical Scenarios

**User Story:** As a retention manager, I want to calculate churn risk for hypothetical customer profiles, so that I can understand how different factors influence churn probability.

#### Acceptance Criteria

1. WHEN the risk calculator form is submitted, THE Backend SHALL validate all required input fields
2. WHEN valid inputs are provided, THE ML_Model SHALL generate a Risk_Score for the hypothetical customer
3. WHEN risk is calculated, THE SHAP_Explainer SHALL produce feature importance for the hypothetical profile
4. WHEN the risk is high (>0.7), THE Offer_Optimizer SHALL recommend an appropriate campaign
5. WHEN inputs are invalid, THE Frontend SHALL display field-specific validation errors in Turkish
6. THE Frontend SHALL organize input fields into 3 columns (profile, usage, risk indicators)
7. THE System SHALL calculate risk in real-time as the user modifies inputs

### Requirement 6: Campaign Simulation and ROI Forecasting

**User Story:** As a marketing manager, I want to simulate campaign budgets and forecast ROI, so that I can optimize retention spending and maximize customer lifetime value.

#### Acceptance Criteria

1. WHEN a risk threshold is selected, THE ROI_Simulator SHALL calculate the number of customers above that threshold
2. WHEN a campaign budget is entered, THE ROI_Simulator SHALL compute cost per customer, expected retention rate, and projected revenue
3. WHEN simulation results are generated, THE System SHALL display targeted customer count, total cost, ROI percentage, and net gain in Turkish Lira
4. WHEN the risk threshold slider moves, THE Frontend SHALL update calculations in real-time
5. THE ROI_Simulator SHALL use configurable parameters (campaign cost per customer, retention success rate, average customer lifetime value)
6. WHEN budget exceeds available resources, THE System SHALL display a warning message
7. THE Frontend SHALL visualize customer base coverage with a progress bar

### Requirement 7: Data Persistence and Retrieval

**User Story:** As a system administrator, I want customer data to be stored reliably and retrieved efficiently, so that the system can serve predictions quickly and maintain data integrity.

#### Acceptance Criteria

1. WHEN customer data is stored, THE Backend SHALL persist it to PostgreSQL with proper schema validation
2. WHEN customer data is queried, THE Backend SHALL retrieve records within 200ms for single customer lookups
3. WHEN bulk data is requested, THE Backend SHALL support pagination with configurable page sizes
4. WHEN database operations fail, THE Backend SHALL log errors and return appropriate HTTP status codes
5. THE Backend SHALL maintain referential integrity between customer profiles and prediction history
6. WHEN customer data is updated, THE System SHALL invalidate cached predictions for that customer

### Requirement 8: Frontend Responsiveness and Accessibility

**User Story:** As a user on any device, I want the dashboard to be responsive and accessible, so that I can use the system effectively regardless of screen size or assistive technology needs.

#### Acceptance Criteria

1. WHEN the viewport width is ≤968px, THE Frontend SHALL switch to mobile layout with stacked components
2. WHEN the viewport width is >968px, THE Frontend SHALL display desktop layout with multi-column grids
3. THE Frontend SHALL implement WCAG AA compliance for color contrast ratios
4. WHEN animations are disabled in user preferences, THE Frontend SHALL respect prefers-reduced-motion media query
5. WHEN keyboard navigation is used, THE Frontend SHALL provide visible focus indicators on all interactive elements
6. THE Frontend SHALL provide alt text for all images and aria-labels for icon buttons
7. WHEN screen readers are active, THE Frontend SHALL announce dynamic content updates

### Requirement 9: API Communication and Error Handling

**User Story:** As a developer, I want robust API communication with proper error handling, so that the system gracefully handles failures and provides clear feedback to users.

#### Acceptance Criteria

1. WHEN the Frontend makes API requests, THE System SHALL include proper authentication headers
2. WHEN API requests fail due to network issues, THE Frontend SHALL display retry options with user-friendly messages in Turkish
3. WHEN the Backend returns validation errors, THE Frontend SHALL map error messages to specific form fields
4. WHEN the Backend is unavailable, THE Frontend SHALL display a maintenance message
5. THE Backend SHALL return standardized JSON error responses with error codes and Turkish messages
6. WHEN API responses exceed 3 seconds, THE Frontend SHALL display loading indicators
7. THE System SHALL log all API errors with timestamps and request context for debugging

### Requirement 10: Performance Optimization

**User Story:** As a user, I want the dashboard to load quickly and respond smoothly, so that I can work efficiently without delays.

#### Acceptance Criteria

1. WHEN the homepage loads, THE Frontend SHALL achieve First Contentful Paint within 1.5 seconds
2. WHEN charts are rendered, THE Frontend SHALL lazy load visualization libraries to reduce initial bundle size
3. WHEN animations run, THE Frontend SHALL use only transform and opacity properties for GPU acceleration
4. THE Backend SHALL implement response caching for frequently accessed customer data with 5-minute TTL
5. WHEN multiple API requests are needed, THE Frontend SHALL batch requests where possible
6. THE Frontend SHALL implement code splitting for route-based lazy loading
7. WHEN images are displayed, THE Frontend SHALL use Next.js Image component with automatic optimization

### Requirement 11: Data Visualization and Charts

**User Story:** As a retention manager, I want interactive visualizations of churn data, so that I can identify patterns and trends quickly.

#### Acceptance Criteria

1. WHEN risk distribution data is available, THE Frontend SHALL render a histogram showing customer count by Risk_Level
2. WHEN top risky customers are displayed, THE Frontend SHALL render a bar chart with customer names and Risk_Scores
3. WHEN SHAP values are visualized, THE Frontend SHALL render a horizontal bar chart with feature names and importance values
4. THE Frontend SHALL support chart interactions (hover tooltips, click to filter)
5. WHEN chart data updates, THE Frontend SHALL animate transitions smoothly
6. THE Frontend SHALL use consistent color schemes across all charts (red for high risk, yellow for medium, green for low)
7. WHEN charts are rendered, THE Frontend SHALL ensure they are responsive and scale to container width

### Requirement 12: Turkish Localization

**User Story:** As a Turkish-speaking user, I want all interface text and messages in Turkish, so that I can use the system in my native language.

#### Acceptance Criteria

1. THE Frontend SHALL display all UI labels, buttons, and headings in Turkish
2. THE Backend SHALL return all error messages and AI insights in Turkish
3. THE System SHALL format dates using Turkish locale (DD.MM.YYYY)
4. THE System SHALL format numbers using Turkish conventions (comma for thousands, period for decimals)
5. THE System SHALL display currency with Turkish Lira symbol (₺) positioned correctly
6. WHEN validation errors occur, THE System SHALL provide Turkish error messages
7. THE Frontend SHALL use Turkish month and day names in date pickers

### Requirement 13: Authentication and Authorization

**User Story:** As a system administrator, I want to control access to the dashboard, so that only authorized personnel can view sensitive customer data.

#### Acceptance Criteria

1. WHEN a user accesses the dashboard, THE System SHALL require authentication
2. WHEN authentication succeeds, THE Backend SHALL issue a JWT token with expiration
3. WHEN API requests are made, THE Backend SHALL validate JWT tokens and reject invalid requests
4. WHEN tokens expire, THE Frontend SHALL redirect users to login page
5. THE System SHALL support role-based access control (admin, manager, analyst)
6. WHEN unauthorized access is attempted, THE Backend SHALL return 403 Forbidden status
7. THE System SHALL log all authentication attempts for security auditing

### Requirement 14: Offer Recommendation Engine

**User Story:** As a retention manager, I want the system to recommend the most effective retention offer for each high-risk customer, so that I can maximize retention success rates.

#### Acceptance Criteria

1. WHEN a customer has Risk_Level of High, THE Offer_Optimizer SHALL recommend one of the available campaigns
2. WHEN selecting an offer, THE Offer_Optimizer SHALL consider customer profile (tenure, plan type, monthly bill)
3. WHEN multiple offers are suitable, THE Offer_Optimizer SHALL rank them by expected effectiveness
4. THE Offer_Optimizer SHALL provide offer details (discount percentage, duration, estimated cost)
5. WHEN offer recommendations are displayed, THE Frontend SHALL show the rationale in Turkish
6. THE Backend SHALL support configurable offer catalog with campaign parameters
7. WHEN no suitable offer exists, THE System SHALL recommend manual review

### Requirement 15: Prediction History and Audit Trail

**User Story:** As a compliance officer, I want to track all predictions and recommendations made by the system, so that I can audit decisions and ensure regulatory compliance.

#### Acceptance Criteria

1. WHEN a prediction is made, THE Backend SHALL store the prediction record with timestamp, customer ID, Risk_Score, and SHAP values
2. WHEN an offer is recommended, THE Backend SHALL log the recommendation with rationale
3. WHEN prediction history is queried, THE Backend SHALL return records sorted by timestamp descending
4. THE Backend SHALL retain prediction history for at least 2 years
5. WHEN audit reports are generated, THE System SHALL export data in CSV format
6. THE Backend SHALL track which user made each prediction request
7. WHEN data is archived, THE System SHALL maintain referential integrity with customer records
