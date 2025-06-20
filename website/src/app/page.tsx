import content from "@/data/content.json";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

// Helper to format date
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

// Component for a single tool
const ToolCard = ({ tool }: { tool: { name: string; url: string; description: string } }) => (
  <div className="p-4 border border-gray-200 rounded-lg transition-all hover:shadow-md hover:border-gray-300 dark:border-gray-700 dark:hover:border-gray-600">
    <a href={tool.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline dark:text-blue-400 font-semibold">
      {tool.name}
    </a>
    <p className="text-gray-600 dark:text-gray-400 mt-1 text-sm">{tool.description}</p>
  </div>
);

// Component for a single news article
const NewsCard = ({ article }: { article: { title:string; url: string; source: string } }) => (
  <div className="p-4 border border-gray-200 rounded-lg transition-all hover:shadow-md hover:border-gray-300 dark:border-gray-700 dark:hover:border-gray-600">
    <a href={article.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline dark:text-blue-400 font-semibold">
      {article.title}
    </a>
    <p className="text-gray-600 dark:text-gray-400 mt-1 text-sm">Source: {article.source}</p>
  </div>
);

// Component for a daily update section
const DailyUpdate = ({ update }: { update: any }) => (
  <section className="mb-12">
    <div className="relative">
      <div className="absolute left-0 top-0 h-full w-px bg-gray-200 dark:bg-gray-700 -translate-x-8" />
      <div className="absolute left-0 top-2 w-4 h-4 rounded-full bg-gray-300 dark:bg-gray-600 -translate-x-10" />
      <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-2">
        {formatDate(update.date)}
      </h2>
      <h3 className="text-xl font-semibold text-gray-700 dark:text-gray-300 mb-4">{update.title}</h3>
    </div>

    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {update.type === "tools" && update.data.map((tool: any, index: number) => (
        <ToolCard key={index} tool={tool} />
      ))}
      {update.type === "news" && update.data.map((article: any, index: number) => (
        <NewsCard key={index} article={article} />
      ))}
    </div>
  </section>
);


export default function Home() {
  const { daily_updates } = content;

  return (
    <main
      className={`flex min-h-screen flex-col items-center justify-between p-8 md:p-16 lg:p-24 ${inter.className}`}
    >
      <div className="max-w-5xl w-full">
        <header className="text-center mb-16">
          <h1 className="text-5xl font-extrabold text-gray-900 dark:text-white tracking-tight">
            Auto-News AI
          </h1>
          <p className="text-lg text-gray-500 dark:text-gray-400 mt-2">
            Your daily digest of trending AI tools and news, updated automatically.
          </p>
        </header>

        <div className="relative">
          <div className="absolute left-4 top-0 h-full w-px bg-gray-200 dark:bg-gray-700" />
          {daily_updates.map((update, index) => (
            <DailyUpdate key={index} update={update} />
          ))}
        </div>
      </div>
    </main>
  );
}
