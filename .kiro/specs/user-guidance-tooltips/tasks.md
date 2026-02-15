# Implementation Plan: User Guidance and Tooltips

## Overview

This implementation plan breaks down the tooltip system into incremental coding tasks. Each task builds on previous work, starting with core components and progressing to page integration, content population, and testing. The system will use Next.js 16, TypeScript, Tailwind CSS, and Lucide React icons.

## Tasks

- [x] 1. Create tooltip content store and type definitions
  - Create `lib/tooltips/content.ts` with TooltipContent interface
  - Define all tooltip content in Turkish for dashboard, calculator, customer detail, and simulation pages
  - Export tooltipContent object with all tooltip IDs and content
  - Include risk score, SHAP values, campaign recommendations, and metric explanations
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 5.3, 5.4, 6.2, 6.3, 6.4, 6.5, 9.1, 9.2_

- [x] 2. Implement core tooltip components
  - [x] 2.1 Create TooltipProvider context component
    - Implement `components/ui/tooltip/TooltipProvider.tsx`
    - Manage global tooltip state (open tooltip ID, position)
    - Provide context for tooltip visibility and positioning
    - _Requirements: 2.5_

  - [x] 2.2 Create Tooltip wrapper component
    - Implement `components/ui/tooltip/Tooltip.tsx`
    - Accept id, side, align, and delayDuration props
    - Combine trigger and content rendering
    - _Requirements: 1.5, 1.6_

  - [x] 2.3 Create TooltipTrigger component
    - Implement `components/ui/tooltip/TooltipTrigger.tsx`
    - Render Lucide React Info icon with consistent styling
    - Handle hover events (mouseenter, mouseleave) with 200ms delay
    - Handle keyboard events (focus, blur, Enter, Space, Escape)
    - Handle touch events for mobile (touchstart, touchend)
    - Add ARIA attributes (role, aria-label, aria-describedby, aria-expanded, tabIndex)
    - Ensure 44x44px minimum touch target size
    - Add visible focus indicator styling
    - _Requirements: 1.5, 1.6, 2.1, 2.2, 7.1, 7.2, 7.3, 7.4, 7.5, 8.1, 8.3, 11.1, 11.5_

  - [ ]* 2.4 Write property test for TooltipTrigger
    - **Property 2: Tooltip Display Timing**
    - **Validates: Requirements 2.1, 2.2**
    - Test that tooltips appear within 200ms on hover and disappear within 200ms on mouse leave
    - Use fast-check to generate random tooltip IDs
    - Run 100 iterations

  - [ ]* 2.5 Write property test for keyboard navigation
    - **Property 9: Keyboard Navigation**
    - **Validates: Requirements 7.1, 7.2, 7.3, 7.4**
    - Test Tab, Enter, Space, and Escape key interactions
    - Use fast-check to generate random tooltip IDs
    - Run 100 iterations

- [x] 3. Implement tooltip content and positioning
  - [x] 3.1 Create TooltipContent component
    - Implement `components/ui/tooltip/TooltipContent.tsx`
    - Fetch content from tooltip content store by ID
    - Render tooltip with title and content
    - Apply Tailwind styling: max-w-[300px], text-sm, p-4, bg-[#172B4D]/95, text-white, rounded-lg, shadow-lg
    - Add backdrop blur effect
    - Include arrow pointer (8px triangle)
    - Add close button for mobile (hidden on desktop)
    - Use Framer Motion for fade-in/fade-out animations (150ms)
    - Add role="tooltip" and aria-hidden attributes
    - _Requirements: 2.3, 10.1, 10.2, 10.3, 10.4, 10.5, 8.4, 11.3_

  - [x] 3.2 Create position calculator utility
    - Implement `lib/tooltips/position.ts`
    - Create calculateTooltipPosition function
    - Calculate position based on trigger element, preferred side, and alignment
    - Check viewport boundaries and reposition if needed
    - Try alternative sides if overflow detected: opposite → adjacent
    - Ensure 8px offset from trigger and 8px minimum from viewport edges
    - Return final position and actual side used
    - _Requirements: 2.3, 2.4, 11.4_

  - [ ]* 3.3 Write property test for viewport boundary handling
    - **Property 3: Viewport Boundary Handling**
    - **Validates: Requirements 2.4, 11.4**
    - Test tooltips positioned near viewport edges remain fully visible
    - Use fast-check to generate random trigger positions
    - Run 100 iterations

  - [ ]* 3.4 Write property test for single tooltip display
    - **Property 4: Single Tooltip Display**
    - **Validates: Requirements 2.5**
    - Test that only one tooltip is visible at a time
    - Use fast-check to generate sequences of tooltip trigger events
    - Run 100 iterations

- [x] 4. Implement tooltip hook and utilities
  - [x] 4.1 Create useTooltip custom hook
    - Implement `lib/tooltips/useTooltip.ts`
    - Manage tooltip open/close state
    - Handle hover delay (200ms) and skip delay (300ms)
    - Calculate position when tooltip opens
    - Provide refs for trigger and content elements
    - Clean up event listeners on unmount
    - Implement debouncing for rapid hover events
    - _Requirements: 2.1, 2.2, 12.5_

  - [x] 4.2 Create tooltip configuration
    - Implement `lib/tooltips/config.ts`
    - Define TooltipConfig interface and defaultTooltipConfig
    - Set delayDuration: 200ms, skipDelayDuration: 300ms, maxWidth: 300px, offset: 8px
    - _Requirements: 2.1, 10.3_

  - [x] 4.3 Implement error handling utilities
    - Create getTooltipContent function with fallback for missing content
    - Log warnings for missing tooltip IDs
    - Return fallback content: "Bu alan için açıklama henüz eklenmemiş"
    - _Requirements: 9.4, 9.5_

  - [ ]* 4.4 Write unit tests for error handling
    - Test missing tooltip content shows fallback
    - Test warning is logged for invalid tooltip ID
    - Test positioning failure falls back to center
    - _Requirements: 9.4, 9.5_

- [x] 5. Checkpoint - Ensure core tooltip system works
  - Ensure all tests pass, ask the user if questions arise.

- [x] 6. Integrate tooltips into Dashboard page
  - [x] 6.1 Add TooltipProvider to dashboard layout
    - Wrap dashboard page content with TooltipProvider
    - _Requirements: 1.1_

  - [x] 6.2 Add info icons to dashboard metrics
    - Add Tooltip components next to: risk distribution, churn rate, total customers, high risk count, monthly revenue
    - Use tooltip IDs: 'risk-distribution', 'churn-rate', 'total-customers', 'high-risk-count', 'monthly-revenue'
    - Position icons immediately adjacent to metric labels
    - _Requirements: 1.1, 1.5, 1.6_

  - [ ]* 6.3 Write unit tests for dashboard tooltips
    - Test that all expected info icons are present on dashboard
    - Test that clicking each icon displays correct content
    - _Requirements: 1.1_

- [x] 7. Integrate tooltips into Calculator page
  - [x] 7.1 Add TooltipProvider to calculator page
    - Wrap calculator page content with TooltipProvider
    - _Requirements: 1.3_

  - [x] 7.2 Add info icons to calculator input fields
    - Add Tooltip components next to: tenure, contract type, monthly charges, payment method, phone service, internet service, and all other input fields
    - Use tooltip IDs from calculatorTooltips mapping
    - Position icons in label elements next to field names
    - _Requirements: 1.3, 1.5, 1.6_

  - [x] 7.3 Add info icons to calculator results
    - Add Tooltip components next to: risk score result, SHAP analysis section
    - Use tooltip IDs: 'risk-score', 'shap-values'
    - _Requirements: 1.3_

  - [ ]* 7.4 Write unit tests for calculator tooltips
    - Test that all input fields have info icons
    - Test that result sections have info icons
    - _Requirements: 1.3_

- [x] 8. Integrate tooltips into Customer Detail page
  - [x] 8.1 Add TooltipProvider to customer detail page
    - Wrap customer detail page content with TooltipProvider
    - _Requirements: 1.2_

  - [x] 8.2 Add info icons to customer detail sections
    - Add Tooltip components next to: risk score, SHAP values, AI insights, campaign recommendations
    - Use tooltip IDs from customerDetailTooltips mapping
    - _Requirements: 1.2, 1.5, 1.6_

  - [ ]* 8.3 Write unit tests for customer detail tooltips
    - Test that all expected sections have info icons
    - _Requirements: 1.2_

- [x] 9. Integrate tooltips into ROI Simulation page
  - [x] 9.1 Add TooltipProvider to simulation page
    - Wrap simulation page content with TooltipProvider
    - _Requirements: 1.4_

  - [x] 9.2 Add info icons to simulation metrics
    - Add Tooltip components next to: ROI, retention rate, projected revenue, campaign cost, customer lifetime value
    - Use tooltip IDs from simulationTooltips mapping
    - _Requirements: 1.4, 1.5, 1.6_

  - [ ]* 9.3 Write unit tests for simulation tooltips
    - Test that all metrics have info icons
    - _Requirements: 1.4_

- [x] 10. Checkpoint - Ensure all pages have tooltips
  - Ensure all tests pass, ask the user if questions arise.

- [x] 11. Implement accessibility features
  - [x] 11.1 Add screen reader support
    - Ensure all tooltips have proper ARIA attributes
    - Test with NVDA/JAWS/VoiceOver screen readers
    - Add aria-live="polite" for dynamic content
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

  - [x] 11.2 Implement reduced motion support
    - Detect prefers-reduced-motion media query
    - Disable animations if preference is set
    - Use instant show/hide instead of transitions
    - _Requirements: 12.3_

  - [ ]* 11.3 Write property test for accessibility attributes
    - **Property 11: Accessibility Attributes**
    - **Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5**
    - Test all info icons have required ARIA attributes
    - Use fast-check to generate random tooltip IDs
    - Run 100 iterations

  - [ ]* 11.4 Write property test for focus indicators
    - **Property 10: Focus Indicator Visibility**
    - **Validates: Requirements 7.5**
    - Test all info icons show visible focus indicator when focused
    - Run 100 iterations

- [x] 12. Implement mobile-specific features
  - [x] 12.1 Add touch event handling
    - Implement touch event listeners in TooltipTrigger
    - Handle tap to show, tap outside to hide
    - _Requirements: 11.1, 11.2_

  - [x] 12.2 Add close button for mobile
    - Show close button (X icon) on touch devices
    - Hide close button on desktop via CSS media query
    - _Requirements: 11.3_

  - [x] 12.3 Ensure touch target sizes
    - Verify all info icons are at least 44x44px on mobile
    - Add padding if needed to meet minimum size
    - _Requirements: 11.5_

  - [ ]* 12.4 Write property test for touch interactions
    - **Property 13: Touch Interaction**
    - **Validates: Requirements 11.1, 11.2**
    - Test tap to show and tap outside to hide
    - Use fast-check to generate random tooltip IDs
    - Run 100 iterations

  - [ ]* 12.5 Write property test for touch target size
    - **Property 12: Touch Target Size**
    - **Validates: Requirements 11.5**
    - Test all info icons meet 44x44px minimum on mobile
    - Run 100 iterations

- [x] 13. Implement performance optimizations
  - [x] 13.1 Add DOM element reuse
    - Implement tooltip portal with single DOM container
    - Reuse tooltip content element for all tooltips
    - Update content and position instead of creating new elements
    - _Requirements: 12.4_

  - [x] 13.2 Optimize initialization
    - Lazy load tooltip content store
    - Ensure initialization completes within 100ms
    - _Requirements: 12.1_

  - [ ]* 13.3 Write property test for layout stability
    - **Property 5: No Layout Shift**
    - **Validates: Requirements 12.3**
    - Test that tooltip display/hide causes zero CLS
    - Use fast-check to generate random tooltip sequences
    - Run 100 iterations

  - [ ]* 13.4 Write property test for DOM element reuse
    - **Property 17: DOM Element Reuse**
    - **Validates: Requirements 12.4**
    - Test that DOM node count remains stable across multiple tooltip displays
    - Run 100 iterations

  - [ ]* 13.5 Write property test for hover debouncing
    - **Property 18: Hover Debouncing**
    - **Validates: Requirements 12.5**
    - Test rapid hover events don't cause flickering
    - Run 100 iterations

- [x] 14. Implement styling and visual consistency
  - [x] 14.1 Create tooltip Tailwind styles
    - Define consistent styles in Tailwind config or CSS module
    - Ensure 4.5:1 contrast ratio (white text on dark background)
    - Set font-size: 14px, max-width: 300px
    - Apply consistent padding, border-radius, shadow
    - _Requirements: 10.1, 10.2, 10.3, 10.4_

  - [x] 14.2 Add multi-paragraph formatting
    - Add CSS for spacing between paragraphs and lists in tooltip content
    - Use prose classes or custom spacing utilities
    - _Requirements: 10.5_

  - [ ]* 14.3 Write property test for style consistency
    - **Property 15: Style Consistency**
    - **Validates: Requirements 10.1, 10.2, 10.3, 10.4**
    - Test all tooltips have consistent styling
    - Check contrast ratio, font size, max width, padding
    - Run 100 iterations

  - [ ]* 14.4 Write property test for multi-paragraph formatting
    - **Property 16: Multi-Paragraph Formatting**
    - **Validates: Requirements 10.5**
    - Test tooltips with multiple paragraphs have proper spacing
    - Run 100 iterations

- [ ] 15. Add comprehensive property tests
  - [ ]* 15.1 Write property test for info icon consistency
    - **Property 1: Info Icon Consistency**
    - **Validates: Requirements 1.5, 1.6**
    - Test all info icons use same component and styling
    - Run 100 iterations

  - [ ]* 15.2 Write property test for Turkish language content
    - **Property 6: Turkish Language Content**
    - **Validates: Requirements 3.4, 4.4, 5.4, 6.5**
    - Test all tooltip content is in Turkish
    - Run 100 iterations

  - [ ]* 15.3 Write property test for UTF-8 encoding
    - **Property 7: UTF-8 Encoding Support**
    - **Validates: Requirements 9.2**
    - Test Turkish characters render correctly
    - Run 100 iterations

  - [ ]* 15.4 Write property test for metric tooltip structure
    - **Property 8: Metric Tooltip Structure**
    - **Validates: Requirements 6.1**
    - Test metric tooltips contain definition, calculation, and significance
    - Run 100 iterations

  - [ ]* 15.5 Write property test for close button on mobile
    - **Property 14: Close Button on Mobile**
    - **Validates: Requirements 11.3**
    - Test tooltips on touch devices have close button
    - Run 100 iterations

- [x] 16. Final checkpoint - Comprehensive testing
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties with 100 iterations each
- Unit tests validate specific examples and edge cases
- All tooltip content must be in Turkish language
- Accessibility compliance (WCAG 2.1 AA) is required
- Performance target: tooltips display within 200ms, no layout shifts
