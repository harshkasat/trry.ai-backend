"use client"
import { useState } from 'react';
import { Button } from "@/components/ui/button"

export default function Hero() {
  const [url, setUrl] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://127.0.0.1:8000/add_url/?url=${url}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      if (response.ok) {
        alert('URL submitted successfully!');
        setUrl('');
      } else {
        alert('Failed to submit URL');
      }
    } catch (error) {
      console.error('Error submitting URL:', error);
      alert('An error occurred while submitting the URL');
    }
  };
  

  return (
    <section className="text-center py-20">
      <h1 className="text-4xl md:text-6xl font-bold mb-4">
        Find bugs before your users do
      </h1>
      <p className="text-xl text-gray-400 mb-8">
        Our agents navigate your website just like real users to find and report bugs.
      </p>
      <div className="inline-block bg-gray-800 rounded-full px-4 py-2 text-sm mb-8">
        Backed by <span className="text-orange-500 font-bold">Z</span> Combinator
      </div>
      <form onSubmit={handleSubmit} className="max-w-md mx-auto flex gap-2">
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter your website URL"
          required
          className="w-full px-4 py-2 rounded-md text-black"
        />
        <Button 
          type="submit" 
          variant="outline" 
          className="text-white border-white hover:bg-white hover:text-black rounded-md"
        >
          Submit
        </Button>
      </form>
    </section>
  );
}

