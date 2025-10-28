import React from "react";

const HomePage = () => {
  return (
    <main className="flex flex-col items-center justify-center text-center py-20 px-6">
      {/* Hero Section */}
      <section className="max-w-5xl">
        <h1 className="text-5xl md:text-6xl font-extrabold bg-gradient-to-r from-indigo-500 to-teal-400 text-transparent bg-clip-text mb-6">
          Analyze Your Website’s Agentic Readiness
        </h1>
        <p className="text-lg md:text-xl text-gray-600 mb-8">
          AgentLens helps you evaluate how ready your site is for AI Agents.  
          Understand, optimize, and future-proof your digital presence.
        </p>

        {/* Input Section */}
        <div className="flex flex-col md:flex-row justify-center items-center gap-3">
          <input
            type="text"
            placeholder="Enter your website URL..."
            className="w-full md:w-96 px-4 py-3 rounded-xl border border-gray-300 focus:ring-2 focus:ring-indigo-400 outline-none transition"
          />
          <button className="px-6 py-3 bg-indigo-500 text-white rounded-xl font-semibold hover:bg-indigo-600 transition-all shadow-lg">
            Scan Now
          </button>
        </div>
      </section>

      {/* Features Section */}
      <section className="grid md:grid-cols-3 gap-8 mt-24 max-w-6xl">
        {[
          {
            title: "AI Metadata Analysis",
            desc: "We detect schema.org, JSON-LD, and agent-ready metadata structures.",
            icon: "🤖",
          },
          {
            title: "API & Data Readiness",
            desc: "Checks your APIs and endpoints for structured data accessibility.",
            icon: "🔗",
          },
          {
            title: "Accessibility Insights",
            desc: "Ensure your content is understandable for both humans and AI agents.",
            icon: "✨",
          },
        ].map((feature, idx) => (
          <div
            key={idx}
            className="p-6 bg-white rounded-2xl shadow-md hover:shadow-xl transition"
          >
            <div className="text-4xl mb-4">{feature.icon}</div>
            <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
            <p className="text-gray-600">{feature.desc}</p>
          </div>
        ))}
      </section>

      {/* CTA Section */}
      <section className="mt-24 text-center">
        <h2 className="text-3xl font-bold mb-4 text-gray-800">
          Ready to check your Agentic Readiness?
        </h2>
        <button className="px-8 py-3 bg-teal-500 text-white rounded-xl font-semibold hover:bg-teal-600 transition shadow-md">
          Get Started for Free
        </button>
      </section>
    </main>
  );
};

export default HomePage;
