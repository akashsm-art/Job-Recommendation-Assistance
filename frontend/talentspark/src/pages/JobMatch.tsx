import { useState } from "react";
import { matchJobs, embedJobs, semanticSearch } from "../Services/RagService";
import type { JobMatchResult, SemanticSearchResult } from "../types/rag";

function MatchScoreDial({ score }: { score: number }) {
    const radius = 24;
    const circumference = 2 * Math.PI * radius;
    const strokeDashoffset = circumference - (score / 100) * circumference;

    return (
        <div className="match-dial">
            <svg className="match-dial-svg" viewBox="0 0 60 60">
                <defs>
                    <linearGradient id="match-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#6366f1" />
                        <stop offset="100%" stopColor="#a855f7" />
                    </linearGradient>
                </defs>
                <circle className="match-dial-bg" cx="30" cy="30" r={radius} />
                <circle 
                    className="match-dial-progress" 
                    cx="30" 
                    cy="30" 
                    r={radius} 
                    strokeDasharray={circumference} 
                    strokeDashoffset={strokeDashoffset} 
                />
            </svg>
            <span className="match-dial-text" style={{ fontSize: '0.8rem', fontWeight: 'bold' }}>{Math.round(score)}%</span>
        </div>
    );
}

function JobMatch() {
    const [activeStep, setActiveStep] = useState(1);
    const [skills, setSkills] = useState("");
    const [experience, setExperience] = useState("");
    const [matches, setMatches] = useState<JobMatchResult[]>([]);
    const [searchQuery, setSearchQuery] = useState("");
    const [searchResults, setSearchResults] = useState<SemanticSearchResult[]>([]);
    const [loading, setLoading] = useState(false);
    const [embedMsg, setEmbedMsg] = useState("");

    const handleEmbed = async () => {
        setLoading(true);
        setEmbedMsg("");
        try {
            const result = await embedJobs();
            setEmbedMsg(result.message);
        } catch {
            setEmbedMsg("Failed to embed jobs. Please check if Qdrant database parameters are online.");
        } finally {
            setLoading(false);
        }
    };

    const handleMatch = async () => {
        if (!skills.trim()) return;
        setLoading(true);
        setMatches([]);
        try {
            const result = await matchJobs(skills, experience);
            setMatches(result.matches);
        } catch {
            setMatches([]);
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = async () => {
        if (!searchQuery.trim()) return;
        setLoading(true);
        setSearchResults([]);
        try {
            const result = await semanticSearch(searchQuery);
            setSearchResults(result.results);
        } catch {
            setSearchResults([]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page-container" style={{ marginTop: '2rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2.5rem' }}>
                <div style={{ padding: '0.75rem', background: 'var(--accent-bg)', borderRadius: '15px' }}>
                    <svg style={{ width: '32px', height: '32px', color: 'var(--accent)' }} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                    </svg>
                </div>
                <div>
                    <h2>Smart Vector Search</h2>
                    <p style={{ margin: 0, opacity: 0.8 }}>Sync listings, run vector searches, and match your candidate profile automatically</p>
                </div>
            </div>

            {/* Stepper Header */}
            <div className="stepper-header">
                <div 
                    className={`step-node ${activeStep >= 1 ? 'active' : ''}`}
                    onClick={() => setActiveStep(1)}
                    style={{ cursor: 'pointer' }}
                    title="Database Sync"
                >
                    1
                </div>
                <div 
                    className={`step-node ${activeStep >= 2 ? 'active' : ''}`}
                    onClick={() => setActiveStep(2)}
                    style={{ cursor: 'pointer' }}
                    title="Semantic Search"
                >
                    2
                </div>
                <div 
                    className={`step-node ${activeStep >= 3 ? 'active' : ''}`}
                    onClick={() => setActiveStep(3)}
                    style={{ cursor: 'pointer' }}
                    title="Profile Matcher"
                >
                    3
                </div>
            </div>

            {/* Active Step Panel */}
            {activeStep === 1 && (
                <div className="card" style={{ textAlign: 'center', padding: '3rem 2rem' }}>
                    <span style={{ fontSize: '3.5rem', display: 'block', marginBottom: '1.25rem' }}>⚡</span>
                    <h3>Database Synchronization</h3>
                    <p style={{ maxWidth: '500px', margin: '0 auto 2rem auto', opacity: 0.8 }}>
                        Vectorize all available job descriptions using the BAAI/bge-small-en embedding model and index them inside Qdrant Cloud.
                    </p>
                    <button className="btn-primary" onClick={handleEmbed} disabled={loading} style={{ padding: '0.75rem 2rem' }}>
                        {loading ? "Syncing Vector Database..." : "Synchronize Database"}
                    </button>
                    {embedMsg && (
                        <div style={{ marginTop: '2rem', padding: '1rem', background: 'var(--success-bg)', border: '1px solid var(--success)', borderRadius: '12px', display: 'inline-block' }}>
                            <span style={{ color: 'var(--success)', fontWeight: 600 }}>✔ {embedMsg}</span>
                        </div>
                    )}
                </div>
            )}

            {activeStep === 2 && (
                <div className="card">
                    <div style={{ marginBottom: '1.5rem' }}>
                        <h3>Semantic Job Finder</h3>
                        <p style={{ margin: 0, opacity: 0.8 }}>Use natural language queries to search listings by roles, tech stack, or description details.</p>
                    </div>

                    <div style={{ display: 'flex', gap: '10px' }}>
                        <input
                            type="text"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            placeholder="Type a search query... e.g. 'Node.js developer with AWS'"
                            style={{ marginBottom: 0 }}
                            onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                        />
                        <button className="btn-primary" onClick={handleSearch} disabled={loading || !searchQuery.trim()} style={{ whiteSpace: 'nowrap' }}>
                            {loading ? "Searching..." : "Vector Search"}
                        </button>
                    </div>

                    {searchResults.length > 0 && (
                        <div style={{ marginTop: "2rem", display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                            <h4 style={{ color: 'var(--accent)', borderBottom: '1px solid var(--border)', paddingBottom: '0.5rem' }}>Search Results</h4>
                            <div className="grid-layout">
                                {searchResults.map((r, i) => (
                                    <div key={i} className="card" style={{ background: 'var(--bg)', border: '1px solid var(--border)', margin: 0, padding: '1.25rem', display: 'flex', gap: '1rem', alignItems: 'start' }}>
                                        <div style={{ flex: 1 }}>
                                            <strong style={{ color: "var(--text-h)", fontSize: '1.1rem', display: 'block', marginBottom: '0.25rem' }}>{r.title}</strong>
                                            <p style={{ fontSize: '0.9rem', opacity: 0.8, margin: '0.5rem 0' }}>{r.description}</p>
                                            <span style={{ fontWeight: 700, color: 'var(--accent)', fontSize: '0.85rem' }}>
                                                Salary: {isNaN(Number(r.salary)) ? r.salary : `$${Number(r.salary).toLocaleString()}`}
                                            </span>
                                        </div>
                                        <MatchScoreDial score={r.score * 100} />
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {!loading && searchResults.length === 0 && searchQuery.trim() && (
                        <p style={{ marginTop: '1.5rem', textAlign: 'center', opacity: 0.6 }}>No search results loaded yet. Press Vector Search.</p>
                    )}
                </div>
            )}

            {activeStep === 3 && (
                <div className="card">
                    <div style={{ marginBottom: '2rem' }}>
                        <h3>Candidate Profiler</h3>
                        <p style={{ margin: 0, opacity: 0.8 }}>Enter your current skillsets and core experiences to check for candidate-job matches.</p>
                    </div>

                    <label>List Core Skills</label>
                    <input
                        type="text"
                        value={skills}
                        onChange={(e) => setSkills(e.target.value)}
                        placeholder="e.g. TypeScript, React, PostgreSQL, Docker"
                    />

                    <label>Brief Experience History</label>
                    <input
                        type="text"
                        value={experience}
                        onChange={(e) => setExperience(e.target.value)}
                        placeholder="e.g. 4 years developing backend systems and deploying APIs"
                    />

                    <button className="btn-primary" onClick={handleMatch} disabled={loading || !skills.trim()} style={{ width: '100%', padding: '0.75rem' }}>
                        {loading ? "Running Similarity Algorithms..." : "Match Profile against Database"}
                    </button>

                    {matches.length > 0 && (
                        <div style={{ marginTop: "2.5rem" }}>
                            <h4 style={{ color: 'var(--accent)', borderBottom: '1px solid var(--border)', paddingBottom: '0.5rem', marginBottom: '1.25rem' }}>Matched Profiles</h4>
                            <div className="grid-layout">
                                {matches.map((m, i) => (
                                    <div key={i} className="card" style={{ background: 'var(--bg)', border: '1px solid var(--border)', margin: 0, padding: '1.25rem', display: 'flex', gap: '1rem', alignItems: 'start' }}>
                                        <div style={{ flex: 1 }}>
                                            <strong style={{ color: "var(--text-h)", fontSize: '1.1rem', display: 'block', marginBottom: '0.25rem' }}>{m.title}</strong>
                                            <p style={{ fontSize: '0.9rem', opacity: 0.8, margin: '0.5rem 0' }}>{m.description}</p>
                                            <span style={{ fontWeight: 700, color: 'var(--accent)', fontSize: '0.85rem' }}>
                                                Salary: {isNaN(Number(m.salary)) ? m.salary : `$${Number(m.salary).toLocaleString()}`}
                                            </span>
                                        </div>
                                        <MatchScoreDial score={m.match_score} />
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default JobMatch;
