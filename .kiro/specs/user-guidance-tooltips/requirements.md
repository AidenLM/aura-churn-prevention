# Requirements Document

## Introduction

This document specifies requirements for adding user guidance and tooltips to the AURA Customer Churn Prevention System dashboard. The system currently displays technical ML predictions, risk scores, SHAP values, and campaign recommendations that are difficult for non-technical users (telecom employees and competition judges) to understand. This feature will add contextual help through info icons and tooltips that explain technical concepts, metrics, and calculations in clear Turkish language.

## Glossary

- **Tooltip_System**: The UI component system that displays contextual help information
- **Info_Icon**: A clickable/hoverable icon (ℹ️) that triggers tooltip display
- **Risk_Score**: A numerical value (0-100) indicating customer churn probability
- **SHAP_Value**: SHapley Additive exPlanations - ML model feature importance values
- **Campaign_Recommendation**: AI-generated retention strategy suggestions
- **Dashboard_Page**: The main overview page showing aggregate metrics
- **Customer_Detail_Page**: Individual customer analysis page
- **Risk_Calculator_Page**: Interactive risk prediction tool page
- **ROI_Simulation_Page**: Return on investment projection page
- **Hover_Event**: Mouse cursor positioned over an element for a specified duration
- **Keyboard_Navigation**: Using Tab, Enter, and Escape keys to navigate UI
- **Screen_Reader**: Assistive technology that reads UI content aloud

## Requirements

### Requirement 1: Info Icon Display

**User Story:** As a telecom employee, I want to see info icons next to technical terms and metrics, so that I know where I can get additional explanations.

#### Acceptance Criteria

1. WHEN the Dashboard_Page loads, THE Tooltip_System SHALL display Info_Icons next to risk distribution metrics, churn rate, and aggregate statistics
2. WHEN the Customer_Detail_Page loads, THE Tooltip_System SHALL display Info_Icons next to risk score, SHAP values, AI insights, and campaign recommendations
3. WHEN the Risk_Calculator_Page loads, THE Tooltip_System SHALL display Info_Icons next to each input field, risk score result, and SHAP analysis section
4. WHEN the ROI_Simulation_Page loads, THE Tooltip_System SHALL display Info_Icons next to ROI metrics, retention rate, and projected revenue
5. THE Info_Icon SHALL be visually consistent across all pages using the ℹ️ symbol or equivalent icon
6. THE Info_Icon SHALL be positioned immediately adjacent to the term or metric it explains

### Requirement 2: Tooltip Display on Hover

**User Story:** As a competition judge, I want to hover over info icons to see explanations, so that I can quickly understand technical concepts without navigating away.

#### Acceptance Criteria

1. WHEN a Hover_Event occurs on an Info_Icon, THE Tooltip_System SHALL display the associated tooltip within 200ms
2. WHEN the mouse cursor leaves the Info_Icon or tooltip area, THE Tooltip_System SHALL hide the tooltip within 200ms
3. WHEN a tooltip is displayed, THE Tooltip_System SHALL position it to avoid overlapping critical UI elements
4. WHEN a tooltip would extend beyond viewport boundaries, THE Tooltip_System SHALL reposition it to remain fully visible
5. THE Tooltip_System SHALL display only one tooltip at a time

### Requirement 3: Risk Score Explanations

**User Story:** As a telecom employee, I want to understand how risk scores are calculated, so that I can trust and act on the predictions.

#### Acceptance Criteria

1. WHEN a user views the Risk_Score tooltip, THE Tooltip_System SHALL explain that risk scores range from 0-100 with higher values indicating greater churn probability
2. WHEN a user views the Risk_Score tooltip, THE Tooltip_System SHALL describe the ML model inputs used (tenure, monthly charges, contract type, etc.)
3. WHEN a user views the Risk_Score tooltip, THE Tooltip_System SHALL explain the model's accuracy and validation metrics in simple terms
4. THE Risk_Score tooltip SHALL be written in Turkish language
5. THE Risk_Score tooltip SHALL use non-technical language understandable by business users

### Requirement 4: SHAP Value Explanations

**User Story:** As a competition judge, I want to understand what SHAP values represent, so that I can evaluate the model's interpretability.

#### Acceptance Criteria

1. WHEN a user views the SHAP_Value tooltip, THE Tooltip_System SHALL explain that SHAP values show how much each factor increases or decreases churn risk
2. WHEN a user views the SHAP_Value tooltip, THE Tooltip_System SHALL describe positive values as risk-increasing factors and negative values as risk-decreasing factors
3. WHEN a user views the SHAP_Value tooltip, THE Tooltip_System SHALL provide a simple example (e.g., "Month-to-month contract: +15 means this increases risk by 15 points")
4. THE SHAP_Value tooltip SHALL be written in Turkish language
5. THE SHAP_Value tooltip SHALL avoid mathematical formulas and focus on practical interpretation

### Requirement 5: Campaign Recommendation Explanations

**User Story:** As a telecom employee, I want to understand how campaign recommendations are determined, so that I can implement them effectively.

#### Acceptance Criteria

1. WHEN a user views a Campaign_Recommendation tooltip, THE Tooltip_System SHALL explain the logic behind the recommendation based on customer risk factors
2. WHEN a user views a Campaign_Recommendation tooltip, THE Tooltip_System SHALL describe expected outcomes (e.g., "reduces churn probability by X%")
3. WHEN a user views a Campaign_Recommendation tooltip, THE Tooltip_System SHALL indicate the recommendation's priority level and reasoning
4. THE Campaign_Recommendation tooltip SHALL be written in Turkish language
5. THE Campaign_Recommendation tooltip SHALL include actionable context for implementation

### Requirement 6: Metric Explanations

**User Story:** As a competition judge, I want to understand what each metric represents, so that I can evaluate the system's business value.

#### Acceptance Criteria

1. WHEN a user views a metric tooltip on Dashboard_Page, THE Tooltip_System SHALL explain the metric's definition, calculation method, and business significance
2. WHEN a user views the churn rate tooltip, THE Tooltip_System SHALL explain it as the percentage of customers who discontinued service in a given period
3. WHEN a user views the retention rate tooltip, THE Tooltip_System SHALL explain it as the percentage of customers who continued service
4. WHEN a user views the ROI tooltip, THE Tooltip_System SHALL explain it as the financial return from retention campaigns relative to campaign costs
5. THE metric tooltips SHALL be written in Turkish language

### Requirement 7: Keyboard Accessibility

**User Story:** As a user with mobility limitations, I want to access tooltips using keyboard navigation, so that I can use the system without a mouse.

#### Acceptance Criteria

1. WHEN a user presses Tab key, THE Tooltip_System SHALL move focus to the next Info_Icon in document order
2. WHEN an Info_Icon has keyboard focus and user presses Enter or Space, THE Tooltip_System SHALL display the associated tooltip
3. WHEN a tooltip is displayed and user presses Escape, THE Tooltip_System SHALL hide the tooltip and return focus to the Info_Icon
4. WHEN a tooltip is displayed and user presses Tab, THE Tooltip_System SHALL hide the current tooltip and move focus to the next focusable element
5. THE Info_Icon SHALL display a visible focus indicator when focused via keyboard

### Requirement 8: Screen Reader Support

**User Story:** As a visually impaired user, I want tooltips to be announced by screen readers, so that I can access the same information as sighted users.

#### Acceptance Criteria

1. WHEN a Screen_Reader encounters an Info_Icon, THE Tooltip_System SHALL provide an accessible label indicating help is available
2. WHEN a Screen_Reader user activates an Info_Icon, THE Tooltip_System SHALL announce the tooltip content
3. THE Info_Icon SHALL use appropriate ARIA attributes (aria-label, aria-describedby, or aria-expanded)
4. THE Tooltip_System SHALL use semantic HTML or ARIA roles to identify tooltips
5. THE Tooltip_System SHALL ensure tooltip content is included in the accessibility tree

### Requirement 9: Tooltip Content Management

**User Story:** As a system administrator, I want tooltip content to be easily maintainable, so that I can update explanations without code changes.

#### Acceptance Criteria

1. THE Tooltip_System SHALL store tooltip content in a centralized configuration file or data structure
2. THE Tooltip_System SHALL support Turkish language content with proper UTF-8 encoding
3. WHEN tooltip content is updated in the configuration, THE Tooltip_System SHALL reflect changes without requiring code recompilation
4. THE Tooltip_System SHALL validate that all required tooltips have content defined
5. THE Tooltip_System SHALL log warnings when referenced tooltip content is missing

### Requirement 10: Tooltip Visual Design

**User Story:** As a telecom employee, I want tooltips to be visually clear and readable, so that I can quickly absorb the information.

#### Acceptance Criteria

1. THE Tooltip_System SHALL display tooltips with sufficient contrast ratio (minimum 4.5:1) for text readability
2. THE Tooltip_System SHALL use a font size of at least 14px for tooltip content
3. THE Tooltip_System SHALL limit tooltip width to a maximum of 300px to maintain readability
4. THE Tooltip_System SHALL apply consistent padding, border, and background styling across all tooltips
5. WHEN a tooltip contains multiple paragraphs or lists, THE Tooltip_System SHALL format them with appropriate spacing

### Requirement 11: Mobile Responsiveness

**User Story:** As a mobile user, I want to access tooltips on touch devices, so that I can use the system on tablets and smartphones.

#### Acceptance Criteria

1. WHEN a user taps an Info_Icon on a touch device, THE Tooltip_System SHALL display the associated tooltip
2. WHEN a tooltip is displayed on a touch device and user taps outside the tooltip area, THE Tooltip_System SHALL hide the tooltip
3. WHEN a tooltip is displayed on a touch device, THE Tooltip_System SHALL include a close button for explicit dismissal
4. THE Tooltip_System SHALL prevent tooltip content from extending beyond the viewport on mobile devices
5. THE Tooltip_System SHALL ensure Info_Icons have a minimum touch target size of 44x44 pixels

### Requirement 12: Performance

**User Story:** As a system user, I want tooltips to load instantly, so that they don't disrupt my workflow.

#### Acceptance Criteria

1. WHEN a page loads, THE Tooltip_System SHALL initialize all tooltip configurations within 100ms
2. WHEN a Hover_Event triggers a tooltip, THE Tooltip_System SHALL display it within 200ms
3. THE Tooltip_System SHALL not cause page layout shifts when tooltips appear or disappear
4. THE Tooltip_System SHALL reuse tooltip DOM elements rather than creating new ones for each display
5. WHEN multiple rapid hover events occur, THE Tooltip_System SHALL debounce tooltip display to prevent flickering
