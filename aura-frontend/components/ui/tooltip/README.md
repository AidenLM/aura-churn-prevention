# Tooltip System

A comprehensive tooltip system for the AURA Customer Churn Prevention System that provides contextual help through info icons and tooltips.

## Components

### TooltipProvider

Context provider that manages global tooltip state. Wrap your application or page with this component.

```tsx
import { TooltipProvider } from '@/components/ui/tooltip';

function App() {
  return (
    <TooltipProvider delayDuration={200}>
      {/* Your app content */}
    </TooltipProvider>
  );
}
```

**Props:**
- `delayDuration` (optional): Delay before showing tooltip in ms (default: 200)
- `skipDelayDuration` (optional): Delay when moving between tooltips in ms (default: 300)

### Tooltip

Main wrapper component that combines trigger and content. This is the primary component you'll use.

```tsx
import { Tooltip } from '@/components/ui/tooltip';
import { Info } from 'lucide-react';

function MyComponent() {
  return (
    <div className="flex items-center gap-2">
      <span>Risk Score</span>
      <Tooltip id="risk-score" side="right">
        <Info className="w-4 h-4 text-gray-400" />
      </Tooltip>
    </div>
  );
}
```

**Props:**
- `id` (required): Unique identifier for tooltip content lookup
- `children` (required): Trigger element (typically an info icon)
- `side` (optional): Preferred placement - 'top' | 'right' | 'bottom' | 'left' (default: 'top')
- `align` (optional): Alignment - 'start' | 'center' | 'end' (default: 'center')
- `delayDuration` (optional): Override provider delay
- `className` (optional): Additional CSS classes for trigger wrapper

## Usage Examples

### Basic Usage

```tsx
import { TooltipProvider, Tooltip } from '@/components/ui/tooltip';
import { Info } from 'lucide-react';

export default function Dashboard() {
  return (
    <TooltipProvider>
      <div className="p-4">
        <h1 className="flex items-center gap-2">
          Dashboard
          <Tooltip id="dashboard-info">
            <Info className="w-4 h-4 text-gray-400" />
          </Tooltip>
        </h1>
      </div>
    </TooltipProvider>
  );
}
```

### Multiple Tooltips

```tsx
<TooltipProvider>
  <div className="space-y-4">
    <div className="flex items-center gap-2">
      <span>Risk Score</span>
      <Tooltip id="risk-score" side="right">
        <Info className="w-4 h-4 text-gray-400" />
      </Tooltip>
    </div>
    
    <div className="flex items-center gap-2">
      <span>SHAP Values</span>
      <Tooltip id="shap-values" side="right">
        <Info className="w-4 h-4 text-gray-400" />
      </Tooltip>
    </div>
    
    <div className="flex items-center gap-2">
      <span>Churn Rate</span>
      <Tooltip id="churn-rate" side="top">
        <Info className="w-4 h-4 text-gray-400" />
      </Tooltip>
    </div>
  </div>
</TooltipProvider>
```

### Custom Positioning

```tsx
{/* Tooltip on the right side */}
<Tooltip id="risk-score" side="right" align="start">
  <Info className="w-4 h-4" />
</Tooltip>

{/* Tooltip on the bottom */}
<Tooltip id="campaign-recommendation" side="bottom" align="center">
  <Info className="w-4 h-4" />
</Tooltip>

{/* Tooltip on the left */}
<Tooltip id="roi" side="left" align="end">
  <Info className="w-4 h-4" />
</Tooltip>
```

## Tooltip Content

Tooltip content is managed centrally in `lib/tooltips/content.ts`. All content is in Turkish.

### Available Tooltip IDs

**Risk Tooltips:**
- `risk-score` - Risk score explanation
- `risk-distribution` - Risk distribution explanation
- `high-risk-count` - High risk customer count

**SHAP Tooltips:**
- `shap-values` - SHAP values explanation

**Campaign Tooltips:**
- `campaign-recommendation` - Campaign recommendation explanation
- `ai-insights` - AI insights explanation

**Metric Tooltips:**
- `churn-rate` - Churn rate explanation
- `retention-rate` - Retention rate explanation
- `roi` - ROI explanation
- `total-customers` - Total customers explanation
- `monthly-revenue` - Monthly revenue explanation
- `projected-revenue` - Projected revenue explanation
- `campaign-cost` - Campaign cost explanation
- `customer-lifetime-value` - CLV explanation

**Field Tooltips:**
- `tenure` - Customer tenure
- `contract-type` - Contract type
- `monthly-charges` - Monthly charges
- `payment-method` - Payment method
- `phone-service` - Phone service
- `internet-service` - Internet service
- And many more...

See `lib/tooltips/content.ts` for the complete list.

## Features

### Accessibility
- ✅ Keyboard navigation (Tab, Enter, Space, Escape)
- ✅ Screen reader support with ARIA attributes
- ✅ Visible focus indicators
- ✅ Minimum 44x44px touch targets

### Interactions
- ✅ Hover with 200ms delay
- ✅ Keyboard focus
- ✅ Touch support for mobile
- ✅ Click outside to close on mobile

### Visual
- ✅ Smooth animations (fade + scale)
- ✅ Reduced motion support
- ✅ Viewport boundary detection
- ✅ Automatic repositioning
- ✅ Arrow pointer
- ✅ Close button on mobile

### Performance
- ✅ Portal rendering to avoid z-index issues
- ✅ Single tooltip at a time
- ✅ No layout shifts
- ✅ Debounced hover events

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Requirements Validation

This implementation satisfies:
- Requirements 1.5, 1.6: Consistent info icon positioning
- Requirements 2.1-2.5: Tooltip display and interaction
- Requirements 7.1-7.5: Keyboard accessibility
- Requirements 8.1-8.5: Screen reader support
- Requirements 10.1-10.5: Visual design
- Requirements 11.1-11.5: Mobile responsiveness
- Requirements 12.1-12.5: Performance
