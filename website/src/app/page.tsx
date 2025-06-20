import { content } from '@/data/content';
import { Inter } from "next/font/google";
import { DailyUpdateSection } from '@/components/DailyUpdateSection';

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  const { daily_updates } = content;

  // Group all updates by a clean date string (e.g., "Fri Jun 20 2025")
  const updatesByDate = daily_updates.reduce((acc, update) => {
    const dateKey = new Date(update.date).toDateString();
    if (!acc[dateKey]) {
      acc[dateKey] = { date: update.date, news: [], tools: [] };
    }
    if (update.type === 'news') {
      acc[dateKey].news.push(...update.data);
    } else if (update.type === 'tools') {
      acc[dateKey].tools.push(...update.data);
    }
    return acc;
  }, {} as Record<string, { date: string; news: any[]; tools: any[] }>);

  // Convert the grouped object back into a sorted array for rendering
  const sortedDailyUpdates = Object.values(updatesByDate)
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

  return (
    <main
      className={`min-h-screen bg-slate-100 dark:bg-slate-950 text-slate-800 dark:text-slate-200 flex flex-col items-center p-4 sm:p-6 md:p-8 ${inter.className}`}
    >
      <div className="max-w-4xl w-full">
        <header className="text-center my-12 md:my-16">
          <h1 className="text-5xl sm:text-6xl font-extrabold tracking-tight text-slate-900 dark:text-slate-100">
            AI Insights Daily
          </h1>
          <p className="text-lg text-slate-600 dark:text-slate-400 mt-4 max-w-2xl mx-auto">
            Your daily digest of trending AI tools and news, updated automatically.
          </p>
        </header>

        <div className="w-full">
          {sortedDailyUpdates.map((day, index) => (
            <DailyUpdateSection key={index} day={day} initiallyOpen={index === 0} />
          ))}
        </div>

        <footer className="text-center my-16 text-sm">
            <p className="text-slate-500 dark:text-slate-400">
                Maintained by Auto-News AI &copy; {new Date().getFullYear()}
            </p>
             <a href="https://github.com/viraj89/ai-resources-and-tools" target="_blank" rel="noopener noreferrer" className="text-slate-500 hover:text-sky-500 dark:hover:text-sky-400 transition-colors mt-2 block">
                View Source on GitHub
            </a>
            <p className="text-xs text-slate-400 dark:text-slate-500 mt-4 max-w-lg mx-auto">
                Disclaimer: This content is aggregated automatically. Information may be outdated or inaccurate. Please verify all information and use at your own risk.
            </p>
        </footer>
      </div>
    </main>
  );
}