/**
 * DailyUpdateSection Component
 * 
 * A collapsible section component that displays daily AI tools and news updates.
 * This component provides an interactive interface for browsing content
 * with smooth animations and responsive design.
 * 
 * Key Features:
 * - Collapsible sections with smooth animations using Framer Motion
 * - Separate display of tools and news with distinct styling
 * - Responsive design with dark/light mode support
 * - Accessible button interactions
 * - Icon-based visual hierarchy
 * 
 * The component uses client-side state management for the collapsible
 * functionality and integrates with the parent page for data flow.
 * 
 * Author: AI Insights Daily Team
 * Version: 3.1.0
 * Last Updated: June 2025
 */

'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

/**
 * Format date string to a human-readable format
 * 
 * Converts ISO date strings to a more user-friendly format
 * (e.g., "January 27, 2025" instead of "2025-01-27")
 * 
 * @param dateString - ISO date string to format
 * @returns Formatted date string
 */
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

/**
 * Tool Icon Component
 * 
 * SVG icon representing AI tools and applications.
 * Uses consistent styling with other icons in the component.
 */
const ToolIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-4 text-slate-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
    </svg>
);

/**
 * News Icon Component
 * 
 * SVG icon representing news articles and updates.
 * Maintains visual consistency with the ToolIcon component.
 */
const NewsIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-4 text-slate-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 12h6m-1 8h.01" />
    </svg>
);

/**
 * Tool List Item Component
 * 
 * Renders individual AI tool entries with consistent styling.
 * Includes the tool name as a clickable link, description,
 * and appropriate hover states for better UX.
 * 
 * @param tool - Tool object containing name, url, and description
 */
const ToolListItem = ({ tool }: { tool: { name: string; url: string; description: string } }) => (
  <div className="py-5 flex items-start">
    <ToolIcon />
    <div>
      <a 
        href={tool.url} 
        target="_blank" 
        rel="noopener noreferrer" 
        className="text-lg font-semibold text-sky-600 hover:text-sky-500 dark:text-sky-400 dark:hover:text-sky-300 transition-colors"
      >
        {tool.name}
      </a>
      <p className="text-slate-600 dark:text-slate-400 mt-1">{tool.description}</p>
    </div>
  </div>
);

/**
 * News List Item Component
 * 
 * Renders individual news article entries with consistent styling.
 * Includes the article title as a clickable link, source attribution,
 * and appropriate hover states for better UX.
 * 
 * @param article - Article object containing title, url, and source
 */
const NewsListItem = ({ article }: { article: { title: string; url: string; source: string } }) => (
  <div className="py-5 flex items-start">
    <NewsIcon />
    <div>
      <a 
        href={article.url} 
        target="_blank" 
        rel="noopener noreferrer" 
        className="text-lg font-semibold text-sky-600 hover:text-sky-500 dark:text-sky-400 dark:hover:text-sky-300 transition-colors"
      >
        {article.title}
      </a>
      <p className="text-sm font-medium text-slate-500 dark:text-slate-400 mt-1">{article.source}</p>
    </div>
  </div>
);

/**
 * DailyUpdateSection Component
 * 
 * Main component that renders a collapsible section for daily updates.
 * This component manages its own open/closed state and provides
 * smooth animations for expanding and collapsing content.
 * 
 * The component separates tools and news into distinct sections
 * for better organization and readability. It uses Framer Motion
 * for smooth animations and provides a responsive design that
 * works well on all device sizes.
 * 
 * @param day - Object containing date, tools array, and news array
 * @param initiallyOpen - Boolean to determine if section starts expanded
 */
export const DailyUpdateSection = ({ day, initiallyOpen = false }: { day: any, initiallyOpen: boolean }) => {
    // State management for collapsible functionality
    const [isOpen, setIsOpen] = useState(initiallyOpen);

    return (
        <div className="mb-6 overflow-hidden rounded-xl border border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 shadow-lg backdrop-blur-sm">
            {/* 
              Collapsible Header Button
              Contains the date and toggle arrow icon.
              Uses motion animation for the rotating arrow effect.
            */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="w-full flex justify-between items-center p-5 bg-white/30 dark:bg-slate-900/30 hover:bg-slate-100/50 dark:hover:bg-slate-800/50 transition-colors"
            >
                <h2 className="text-xl font-bold text-slate-800 dark:text-slate-200">
                    {formatDate(day.date)}
                </h2>
                {/* Animated arrow icon that rotates when section is opened/closed */}
                <motion.span animate={{ rotate: isOpen ? 180 : 0 }} transition={{ duration: 0.3 }}>
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                </motion.span>
            </button>
            
            {/* 
              Animated Content Area
              Uses Framer Motion's AnimatePresence for smooth enter/exit animations.
              The content slides down when opened and slides up when closed.
            */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        transition={{ duration: 0.3, ease: 'easeInOut' }}
                        className="overflow-hidden"
                    >
                        <div className="p-6 border-t border-slate-200 dark:border-slate-800">
                            {/* 
                              Tools Section
                              Displays AI tools and applications discovered on this date.
                              Only renders if there are tools available.
                            */}
                            {day.tools.length > 0 && (
                                <section className="mb-10">
                                    <h3 className="text-2xl font-semibold text-slate-700 dark:text-slate-300 mb-2">
                                        Latest Tools & Apps
                                    </h3>
                                    <div className="flex flex-col divide-y divide-slate-200 dark:divide-slate-800">
                                        {day.tools.map((tool: any, toolIndex: number) => (
                                            <ToolListItem key={toolIndex} tool={tool} />
                                        ))}
                                    </div>
                                </section>
                            )}
                            
                            {/* 
                              News Section
                              Displays news articles and updates from this date.
                              Only renders if there are news items available.
                            */}
                            {day.news.length > 0 && (
                                <section>
                                    <h3 className="text-2xl font-semibold text-slate-700 dark:text-slate-300 mb-2">
                                        News & Articles
                                    </h3>
                                    <div className="flex flex-col divide-y divide-slate-200 dark:divide-slate-800">
                                        {day.news.map((article: any, articleIndex: number) => (
                                            <NewsListItem key={articleIndex} article={article} />
                                        ))}
                                    </div>
                                </section>
                            )}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
}; 