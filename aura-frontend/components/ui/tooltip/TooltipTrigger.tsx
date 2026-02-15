'use client';

import React, { ReactNode, useRef, useState, useEffect } from 'react';
import { useTooltipContext, Position } from './TooltipProvider';

/**
 * TooltipTrigger component props
 */
export interface TooltipTriggerProps {
  /** Unique tooltip identifier */
  tooltipId: string;
  /** Trigger element (info icon) */
  children: ReactNode;
  /** Preferred tooltip side */
  side?: 'top' | 'right' | 'bottom' | 'left';
  /** Tooltip alignment */
  align?: 'start' | 'center' | 'end';
  /** Hover delay duration (ms) */
  delayDuration?: number;
  /** Optional CSS class */
  className?: string;
  /** Optional ARIA label */
  ariaLabel?: string;
}

/**
 * TooltipTrigger Component
 * 
 * Renders the trigger element (info icon) that displays tooltip on interaction.
 * Handles mouse hover, keyboard focus, and touch events.
 * Provides accessibility attributes for screen readers.
 * 
 * Requirements:
 * - Display info icon with consistent styling
 * - Handle hover events with 200ms delay
 * - Handle keyboard navigation (Tab, Enter, Space, Escape)
 * - Handle touch events for mobile
 * - Minimum 44x44px touch target
 * - Visible focus indicator
 * - ARIA attributes for accessibility
 */
export function TooltipTrigger({
  tooltipId,
  children,
  side = 'top',
  align = 'center',
  delayDuration = 200,
  className = '',
  ariaLabel = 'Daha fazla bilgi',
}: TooltipTriggerProps) {
  const { openTooltip, closeTooltip, isTooltipOpen } = useTooltipContext();
  const triggerRef = useRef<HTMLButtonElement>(null);
  const [hoverTimeout, setHoverTimeout] = useState<NodeJS.Timeout | null>(null);
  const isOpen = isTooltipOpen(tooltipId);

  /**
   * Calculate tooltip position based on trigger element
   */
  const calculatePosition = (): Position => {
    if (!triggerRef.current) {
      return { x: 0, y: 0, side };
    }

    const rect = triggerRef.current.getBoundingClientRect();
    const offset = 8; // Distance from trigger

    let x = 0;
    let y = 0;

    // Calculate position based on preferred side
    switch (side) {
      case 'top':
        x = rect.left + rect.width / 2;
        y = rect.top - offset;
        break;
      case 'bottom':
        x = rect.left + rect.width / 2;
        y = rect.bottom + offset;
        break;
      case 'left':
        x = rect.left - offset;
        y = rect.top + rect.height / 2;
        break;
      case 'right':
        x = rect.right + offset;
        y = rect.top + rect.height / 2;
        break;
    }

    return { x, y, side };
  };

  /**
   * Handle mouse enter - show tooltip after delay
   */
  const handleMouseEnter = () => {
    const timeout = setTimeout(() => {
      const position = calculatePosition();
      openTooltip(tooltipId, position);
    }, delayDuration);
    
    setHoverTimeout(timeout);
  };

  /**
   * Handle mouse leave - hide tooltip and clear delay
   */
  const handleMouseLeave = () => {
    if (hoverTimeout) {
      clearTimeout(hoverTimeout);
      setHoverTimeout(null);
    }
    closeTooltip();
  };

  /**
   * Handle keyboard focus - show tooltip
   */
  const handleFocus = () => {
    const position = calculatePosition();
    openTooltip(tooltipId, position);
  };

  /**
   * Handle keyboard blur - hide tooltip
   */
  const handleBlur = () => {
    closeTooltip();
  };

  /**
   * Handle keyboard events (Enter, Space, Escape)
   */
  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      if (isOpen) {
        closeTooltip();
      } else {
        const position = calculatePosition();
        openTooltip(tooltipId, position);
      }
    } else if (event.key === 'Escape' && isOpen) {
      event.preventDefault();
      closeTooltip();
      triggerRef.current?.focus();
    }
  };

  /**
   * Handle touch events for mobile
   */
  const handleTouchStart = (event: React.TouchEvent) => {
    event.preventDefault();
    if (isOpen) {
      closeTooltip();
    } else {
      const position = calculatePosition();
      openTooltip(tooltipId, position);
    }
  };

  /**
   * Clean up timeout on unmount
   */
  useEffect(() => {
    return () => {
      if (hoverTimeout) {
        clearTimeout(hoverTimeout);
      }
    };
  }, [hoverTimeout]);

  return (
    <button
      ref={triggerRef}
      type="button"
      role="button"
      aria-label={ariaLabel}
      aria-describedby={isOpen ? tooltipId : undefined}
      aria-expanded={isOpen}
      tabIndex={0}
      className={`inline-flex items-center justify-center min-w-[44px] min-h-[44px] p-2 
        rounded-full hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 
        focus:ring-offset-2 transition-colors ${className}`}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onFocus={handleFocus}
      onBlur={handleBlur}
      onKeyDown={handleKeyDown}
      onTouchStart={handleTouchStart}
    >
      {children}
    </button>
  );
}
