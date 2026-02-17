"use client";
import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any[]>([]);
  const [k, setK] = useState(5);

  const search = async () => {
    if (!query) return;

    const res = await fetch(
      `http://127.0.0.1:8000/hybrid_search?query=${query}&k=${k}`
    );

    const data = await res.json();
    setResults(Array.isArray(data) ? data : []);
  };

  return (
    <div className="container">

      <h1>NCO Semantic Search</h1>
      <p className="subtitle">
        AI-powered occupation search
      </p>

      <div className="searchbar">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search occupation..."
        />
        <button onClick={search}>Search</button>
      </div>

      <div className="k-toggle">
        Show:
        {[5, 10, 20, 50].map((num) => (
          <button
            key={num}
            onClick={() => setK(num)}
            className={`kbtn ${k === num ? "active" : ""}`}
          >
            {num}
          </button>
        ))}
      </div>

      {results.length > 0 && (
        <div className="card">

          <h3>Occupation Titles</h3>
          <p className="result-count">
            {results.length} results found
          </p>

          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Occupation Title</th>
                  <th>NCO 2015</th>
                  <th>NCO 2004</th>
                  <th>Division</th>
                  <th>Subdivision</th>
                  <th>Group</th>
                </tr>
              </thead>

              <tbody>
                {results.map((r, i) => (
                  <tr key={i}>
                    <td>{i + 1}</td>
                    <td className="title">{r.occupation_title}</td>
                    <td>{r.nco_2015}</td>
                    <td>{r.nco_2004}</td>
                    <td>{r.division}</td>
                    <td>{r.subdivision}</td>
                    <td>{r.group}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

        </div>
      )}
    </div>
  );
}
