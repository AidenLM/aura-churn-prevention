'use client';

import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';

/**
 * Position interface for tooltip placement
 */
export interface Position {
  x: number;
  y: number;
  side: 'top' | 'right' | 'bottom' | 'left';
}

/**
 * Tooltip context state
 */
interface TooltipContextState {
  openTooltipId: string | null;
  position: Position | null;
  openTooltip: (id: string, position: Position) => void;
  closeTooltip: () => void;
  isTooltipOpen: (id: string) => boolean;
}

/**
 * Tooltip context with default values
 */
const TooltipContext = createContext<TooltipContextState | undefined>(undefined);

/**
 * TooltipProvider props
 */
export interface TooltipProviderProps {
  children: ReactNode;
  delayDuration?: number;
  skipDelayDuration?: number;
}

/**
 * TooltipProvider component
 * 
 * Manages global tooltip state to ensure only one tooltip is visible at a time.
 * Provides context for tooltip visibility and positioning.
 * 
 * @param children - Child components
 * @param delayDuration - Delay before showing tooltip (ms) - default 200ms
 * @param skipDelayDuration - Delay when moving between tooltips (ms) - default 300ms
 */
export function TooltipProvider({
  children,
  delayDuration = 200,
  skipDelayDuration = 300,
}: TooltipProviderProps) {
  const [openTooltipId, setOpenTooltipId] = useState<string | null>(null);
  const [position, setPosition] = useState<Position | null>(null);

  /**
   * Open a tooltip with the given ID and position
   * Automatically closes any currently open tooltip (ensures only one tooltip at a time)
   */
  const openTooltip = useCallback((id: string, newPosition: Position) => {
    setOpenTooltipId(id);
    setPosition(newPosition);
  }, []);

  /**
   * Close the currently open tooltip
   */
  const closeTooltip = useCallback(() => {
    setOpenTooltipId(null);
    setPosition(null);
  }, []);

  /**
   * Check if a specific tooltip is currently open
   */
  const isTooltipOpen = useCallback(
    (id: string) => openTooltipId === id,
    [openTooltipId]
  );

  const contextValue: TooltipContextState = {
    openTooltipId,
    position,
    openTooltip,
    closeTooltip,
    isTooltipOpen,
  };

  return (
    <TooltipContext.Provider value={contextValue}>
      {children}
    </TooltipContext.Provider>
  );
}

/**
 * Hook to access tooltip context
 * 
 * @throws Error if used outside of TooltipProvider
 */
export function useTooltipContext() {
  const context = useContext(TooltipContext);
  
  if (context === undefined) {
    throw new Error('useTooltipContext must be used within a TooltipProvider');
  }
  
  return context;
}
