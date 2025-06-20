'use client';

import { useEffect, useState } from "react";
import useSWR from "swr";

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export default function VisitorCounter() {
    const { data, error } = useSWR("/api/views", fetcher);
    const [views, setViews] = useState(0);

    useEffect(() => {
        if (data) {
            setViews(data.views);
        }
    }, [data]);

    if (error) return <div className="text-sm text-red-500">Failed to load views</div>;
    if (!data) return <div className="text-sm text-gray-500">Loading views...</div>;

    return (
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
            Unique Visitors: {views.toLocaleString()}
        </p>
    );
} 