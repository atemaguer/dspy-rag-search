import React, { useState } from "react";

const SearchBox = () => {
  const [searchTerm, setSearchTerm] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(searchTerm);
  };

  const handleInputChange = (e) => {
    setSearchTerm(e.target.data);
  };

  const handleEnterPress = (e) => {
    if (e.key === "Enter") {
      console.log("Enter key pressed:", e.target.value);
    }
  };
  return (
    <div className="container mx-auto">
      <input
        className="w-full h-14 outline-none text-2xl px-4 rounded font-normal text-slate-700"
        type="search"
        value={searchTerm}
        onChange={handleInputChange}
        placeholder="Search..."
        onSubmit={handleSubmit}
        onKeyDown={handleEnterPress}
      />
    </div>
  );
};

export default SearchBox;
