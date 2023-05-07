import React from "react";

import SearchBox from "@/components/Search";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center">
      <div className="flex items-center flex-col flex-grow">
        <h1 className="text-2xl font-semibold mb-6">
          Welcome to My Landing Page
        </h1>
        <SearchBox />
        <p></p>
      </div>
    </div>
  );
}
