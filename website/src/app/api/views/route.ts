import { kv } from "@vercel/kv";
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
    try {
        const currentViews = await kv.get<number>('views');
        
        // If it's the first visit, initialize the counter
        if (currentViews === null) {
            await kv.set('views', 1);
            return NextResponse.json({ views: 1 });
        }
        
        // Increment the view count
        const newViews = currentViews + 1;
        await kv.set('views', newViews);
        
        return NextResponse.json({ views: newViews });

    } catch (error) {
        console.error("Error with Vercel KV:", error);
        return new NextResponse(
            JSON.stringify({ message: "Failed to update views" }),
            { status: 500, headers: { 'Content-Type': 'application/json' } }
        );
    }
} 