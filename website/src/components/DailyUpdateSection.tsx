'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

// Helper to format date
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

const ToolIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-4 text-slate-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
    </svg>
);

const NewsIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-4 text-slate-400 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 12h6m-1 8h.01" />
    </svg>
);

const ToolListItem = ({ tool }: { tool: { name: string; url: string; description: string } }) => (
  <div className="py-5 flex items-start">
    <ToolIcon />
    <div>
      <a href={tool.url} target="_blank" rel="noopener noreferrer" className="text-lg font-semibold text-sky-600 hover:text-sky-500 dark:text-sky-400 dark:hover:text-sky-300 transition-colors">
        {tool.name}
      </a>
      <p className="text-slate-600 dark:text-slate-400 mt-1">{tool.description}</p>
    </div>
  </div>
);

const NewsListItem = ({ article }: { article: { title: string; url: string; source: string } }) => (
  <div className="py-5 flex items-start">
    <NewsIcon />
    <div>
      <a href={article.url} target="_blank" rel="noopener noreferrer" className="text-lg font-semibold text-sky-600 hover:text-sky-500 dark:text-sky-400 dark:hover:text-sky-300 transition-colors">
        {article.title}
      </a>
      <p className="text-sm font-medium text-slate-500 dark:text-slate-400 mt-1">{article.source}</p>
    </div>
  </div>
);

export const DailyUpdateSection = ({ day, initiallyOpen = false }: { day: any, initiallyOpen: boolean }) => {
    const [isOpen, setIsOpen] = useState(initiallyOpen);

    return (
        <div className="mb-6 overflow-hidden rounded-xl border border-slate-200 dark:border-slate-800 bg-white/50 dark:bg-slate-900/50 shadow-lg backdrop-blur-sm">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="w-full flex justify-between items-center p-5 bg-white/30 dark:bg-slate-900/30 hover:bg-slate-100/50 dark:hover:bg-slate-800/50 transition-colors"
            >
                <h2 className="text-xl font-bold text-slate-800 dark:text-slate-200">
                    {formatDate(day.date)}
                </h2>
                <motion.span animate={{ rotate: isOpen ? 180 : 0 }} transition={{ duration: 0.3 }}>
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                </motion.span>
            </button>
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