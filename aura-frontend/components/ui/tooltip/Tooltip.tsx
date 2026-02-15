'use client';

import React, { ReactNode } from 'react';
import { useTooltipContext } from './TooltipProvider';
import { TooltipTrigger } from './TooltipTrigger';
import { TooltipContent } from './TooltipContent';

/**
 * Tooltip wrapper component props
 */
export interface TooltipProps {
  /** Unique identifier for tooltip content lookup */
  id: string;
  /** Trigger element (typically an info icon) */
  children: ReactNode;
  /** Preferred side for tooltip placement */
  side?: 'top' | 'right' | 'bottom' | 'left';
  /** Alignment of tooltip relative to trigger */
  align?: 'start' | 'center' | 'end';
  /** Override provider delay duration (ms) */
  delayDuration?: number;
  /** Optional CSS class for trigger wrapper */
  className?: string;
}

/**
 * Tooltip Component
 * 
 * Wrapper component that combines trigger and content rendering.
 * Manages tooltip ID and positioning preferences.
 * Integrates with TooltipProvider context for state management.
 * 
 * Example usage:
 * ```tsx
 * <Tooltip id="risk-score" side="right">
 *   <InfoIcon className="w-4 h-4 text-gray-400" />
 * </Tooltip>
 * ```
 * 
 * @param id - Unique tooltip identifier for content lookup
 * @param children - Trigger element to render
 * @param side - Preferred tooltip placement (default: 'top')
 * @param align - Tooltip alignment (default: 'center')
 * @param delayDuration - Hover delay override (default: from provider)
 * @param className - Optional CSS class for trigger wrapper
 */
export function Tooltip({
  id,
  children,
  side = 'top',
  align = 'center',
  delayDuration,
  className,
}: TooltipProps) {
  const { isTooltipOpen } = useTooltipContext();
  const isOpen = isTooltipOpen(id);

  return (
    <>
      <TooltipTrigger
        tooltipId={id}
        side={side}
        align={align}
        delayDuration={delayDuration}
        className={className}
      >
        {children}
      </TooltipTrigger>
      
      {isOpen && (
        <TooltipContent
          id={id}
          side={side}
          align={align}
        />
      )}
    </>
  );
}
