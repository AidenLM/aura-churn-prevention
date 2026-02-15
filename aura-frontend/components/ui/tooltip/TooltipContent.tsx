'use client';

import React, { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
import { useTooltipContext } from './TooltipProvider';
import { getTooltipContent } from '@/lib/tooltips/content';

/**
 * TooltipContent component props
 */
export interface TooltipContentProps {
  /** Unique tooltip identifier */
  id: string;
  /** Preferred tooltip side */
  side?: 'top' | 'right' | 'bottom' | 'left';
  /** Tooltip alignment */
  align?: 'start' | 'center' | 'end';
}

/**
 * TooltipContent Component
 * 
 * Displays the tooltip popup with content from the content store.
 * Handles positioning, animations, and accessibility.
 * Renders in a portal to avoid z-index issues.
 * 
 * Requirements:
 * - Max width: 300px
 * - Font size: 14px
 * - Proper contrast ratio (4.5:1)
 * - Smooth animations (fade + scale)
 * - Close button for mobile
 * - ARIA attributes
 * - Viewport boundary handling
 */
export function TooltipContent({
  id,
  side = 'top',
  align = 'center',
}: TooltipContentProps) {
  const { position, closeTooltip } = useTooltipContext();
  const contentRef = useRef<HTMLDivElement>(null);
  const [adjustedPosition, setAdjustedPosition] = useState(position);
  const [isMounted, setIsMounted] = useState(false);
  const [isTouchDevice, setIsTouchDevice] = useState(false);

  // Get tooltip content from store
  const tooltipData = getTooltipContent(id);

  /**
   * Detect touch device
   */
  useEffect(() => {
    setIsTouchDevice('ontouchstart' in window || navigator.maxTouchPoints > 0);
    setIsMounted(true);
  }, []);

  /**
   * Adjust position to stay within viewport boundaries
   */
  useEffect(() => {
    if (!position || !contentRef.current) {
      return;
    }

    const rect = contentRef.current.getBoundingClientRect();
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    const margin = 8; // Minimum distance from viewport edge

    let { x, y, side: currentSide } = position;

    // Adjust horizontal position
    if (currentSide === 'top' || currentSide === 'bottom') {
      // Center alignment
      x = x - rect.width / 2;
      
      // Check left boundary
      if (x < margin) {
        x = margin;
      }
      
      // Check right boundary
      if (x + rect.width > viewportWidth - margin) {
        x = viewportWidth - rect.width - margin;
      }
    }

    // Adjust vertical position
    if (currentSide === 'left' || currentSide === 'right') {
      // Center alignment
      y = y - rect.height / 2;
      
      // Check top boundary
      if (y < margin) {
        y = margin;
      }
      
      // Check bottom boundary
      if (y + rect.height > viewportHeight - margin) {
        y = viewportHeight - rect.height - margin;
      }
    }

    // Adjust for top/bottom sides
    if (currentSide === 'top') {
      y = y - rect.height;
      
      // If tooltip goes above viewport, flip to bottom
      if (y < margin) {
        y = position.y + margin;
        currentSide = 'bottom';
      }
    } else if (currentSide === 'bottom') {
      // If tooltip goes below viewport, flip to top
      if (y + rect.height > viewportHeight - margin) {
        y = position.y - rect.height - margin;
        currentSide = 'top';
      }
    }

    // Adjust for left/right sides
    if (currentSide === 'left') {
      x = x - rect.width;
      
      // If tooltip goes left of viewport, flip to right
      if (x < margin) {
        x = position.x + margin;
        currentSide = 'right';
      }
    } else if (currentSide === 'right') {
      // If tooltip goes right of viewport, flip to left
      if (x + rect.width > viewportWidth - margin) {
        x = position.x - rect.width - margin;
        currentSide = 'left';
      }
    }

    setAdjustedPosition({ x, y, side: currentSide });
  }, [position]);

  /**
   * Handle click outside to close (for touch devices)
   */
  useEffect(() => {
    if (!isTouchDevice) return;

    const handleClickOutside = (event: MouseEvent) => {
      if (contentRef.current && !contentRef.current.contains(event.target as Node)) {
        closeTooltip();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isTouchDevice, closeTooltip]);

  /**
   * Check for reduced motion preference
   */
  const prefersReducedMotion = 
    typeof window !== 'undefined' && 
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /**
   * Animation configuration
   */
  const animationConfig = prefersReducedMotion
    ? {
        initial: { opacity: 1 },
        animate: { opacity: 1 },
        exit: { opacity: 0 },
        transition: { duration: 0 },
      }
    : {
        initial: { opacity: 0, scale: 0.95 },
        animate: { opacity: 1, scale: 1 },
        exit: { opacity: 0, scale: 0.95 },
        transition: { duration: 0.15 },
      };

  // Don't render on server or if not mounted
  if (!isMounted || !adjustedPosition) {
    return null;
  }

  const tooltipElement = (
    <AnimatePresence>
      <motion.div
        ref={contentRef}
        role="tooltip"
        id={id}
        aria-hidden={false}
        className="fixed z-50 max-w-[300px] text-sm p-4 bg-[#172B4D]/95 text-white 
          rounded-lg shadow-lg backdrop-blur-sm"
        style={{
          left: `${adjustedPosition.x}px`,
          top: `${adjustedPosition.y}px`,
        }}
        {...animationConfig}
      >
        {/* Close button for touch devices */}
        {isTouchDevice && (
          <button
            type="button"
            onClick={closeTooltip}
            className="absolute top-2 right-2 p-1 rounded hover:bg-white/20 
              transition-colors focus:outline-none focus:ring-2 focus:ring-white/50"
            aria-label="Kapat"
          >
            <X className="w-4 h-4" />
          </button>
        )}

        {/* Tooltip title */}
        {tooltipData.title && (
          <div className="font-semibold mb-2 pr-6">
            {tooltipData.title}
          </div>
        )}

        {/* Tooltip content */}
        <div className="text-white/90 leading-relaxed">
          {tooltipData.content}
        </div>

        {/* Arrow pointer */}
        <div
          className="absolute w-2 h-2 bg-[#172B4D] rotate-45"
          style={{
            ...(adjustedPosition.side === 'top' && {
              bottom: '-4px',
              left: '50%',
              transform: 'translateX(-50%) rotate(45deg)',
            }),
            ...(adjustedPosition.side === 'bottom' && {
              top: '-4px',
              left: '50%',
              transform: 'translateX(-50%) rotate(45deg)',
            }),
            ...(adjustedPosition.side === 'left' && {
              right: '-4px',
              top: '50%',
              transform: 'translateY(-50%) rotate(45deg)',
            }),
            ...(adjustedPosition.side === 'right' && {
              left: '-4px',
              top: '50%',
              transform: 'translateY(-50%) rotate(45deg)',
            }),
          }}
        />
      </motion.div>
    </AnimatePresence>
  );

  // Render in portal to avoid z-index issues
  return createPortal(tooltipElement, document.body);
}
