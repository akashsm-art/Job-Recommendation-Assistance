import { useState, useEffect } from "react";
import { getCompanies } from "../Services/CompanyService";
import { getJobs } from "../Services/JobService";
import { 
    rankCandidates, detectDuplicates, scanAuthenticity, getPoolSummary, 
    type CandidateRankInfo, type DuplicateDetectionResponse, type ResumeAuthenticityResponse, type RecruiterPoolSummaryResponse 
} from "../Services/AiService";
import type { Company } from "../types/company";
import type { Job } from "../types/job";

function RecruiterPortal() {
    const [, setCompanies] = useState<Company[]>([]);
    const [jobs, setJobs] = useState<Job[]>([]);
    const [selectedJobId, setSelectedJobId] = useState<number | "">("");

    const [rankedCandidates, setRankedCandidates] = useState<CandidateRankInfo[]>([]);

    const [loadingPool, setLoadingPool] = useState(false);
    const [poolSummary, setPoolSummary] = useState<RecruiterPoolSummaryResponse | null>(null);

    // Duplicate detection states
    const [dupText1, setDupText1] = useState("");
    const [dupText2, setDupText2] = useState("");
    const [loadingDup, setLoadingDup] = useState(false);
    const [dupResult, setDupResult] = useState<DuplicateDetectionResponse | null>(null);

    // Authenticity states
    const [authText, setAuthText] = useState("");
    const [loadingAuth, setLoadingAuth] = useState(false);
    const [authResult, setAuthResult] = useState<ResumeAuthenticityResponse | null>(null);

    const [activeSection, setActiveSection] = useState<"ranking" | "duplicates" | "authenticity">("ranking");
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchRecruiterData = async () => {
            try {
                const comps = await getCompanies();
                setCompanies(comps);
                const allJobs = await getJobs();
                setJobs(allJobs);
            } catch (err) {
                console.error("Error loading recruiter companies/jobs:", err);
            }
        };
        fetchRecruiterData();
    }, []);

    const handleRankCandidates = async (jobId: number) => {
        setLoadingPool(true);
        setError("");
        setRankedCandidates([]);
        setPoolSummary(null);

        try {
            const candidates = await rankCandidates(jobId);
            setRankedCandidates(candidates);
            const pool = await getPoolSummary(jobId);
            setPoolSummary(pool);
        } catch (err) {
            setError("Failed to fetch applicant data or matching details.");
            console.error(err);
        } finally {
            setLoadingPool(false);
        }
    };

    const handleDetectDuplicates = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!dupText1.trim() || !dupText2.trim()) return;

        setLoadingDup(true);
        setDupResult(null);
        try {
            const res = await detectDuplicates(dupText1, dupText2);
            setDupResult(res);
        } catch (err) {
            console.error(err);
            alert("Duplicate check failed.");
        } finally {
            setLoadingDup(false);
        }
    };

    const handleScanAuthenticity = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!authText.trim()) return;

        setLoadingAuth(true);
        setAuthResult(null);
        try {
            const res = await scanAuthenticity(authText);
            setAuthResult(res);
        } catch (err) {
            console.error(err);
            alert("Authenticity scan failed.");
        } finally {
            setLoadingAuth(false);
        }
    };

    return (
        <div className="page-container" style={{ marginTop: '2rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
                <div style={{ padding: '0.75rem', background: 'var(--accent-bg)', borderRadius: '15px' }}>
                    <svg style={{ width: '32px', height: '32px', color: 'var(--accent)' }} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                    </svg>
                </div>
                <div>
                    <h2>AI Recruiter Portal</h2>
                    <p style={{ margin: 0, opacity: 0.8 }}>Access advanced candidate ranking, duplication detection, and resume authenticity reviews</p>
                </div>
            </div>

            <div style={{ display: 'flex', borderBottom: '1px solid var(--border)', marginBottom: '1.5rem', gap: '1.5rem' }}>
                <button 
                    type="button"
                    style={{ border: 'none', background: 'none', padding: '0.5rem 0', borderRadius: 0, color: activeSection === "ranking" ? "var(--accent)" : "var(--text)", borderBottom: activeSection === "ranking" ? "2px solid var(--accent)" : "none", fontWeight: 700 }}
                    onClick={() => setActiveSection("ranking")}
                >
                    📊 Candidate Ranking
                </button>
                <button 
                    type="button"
                    style={{ border: 'none', background: 'none', padding: '0.5rem 0', borderRadius: 0, color: activeSection === "duplicates" ? "var(--accent)" : "var(--text)", borderBottom: activeSection === "duplicates" ? "2px solid var(--accent)" : "none", fontWeight: 700 }}
                    onClick={() => setActiveSection("duplicates")}
                >
                    👥 Duplicate Checker
                </button>
                <button 
                    type="button"
                    style={{ border: 'none', background: 'none', padding: '0.5rem 0', borderRadius: 0, color: activeSection === "authenticity" ? "var(--accent)" : "var(--text)", borderBottom: activeSection === "authenticity" ? "2px solid var(--accent)" : "none", fontWeight: 700 }}
                    onClick={() => setActiveSection("authenticity")}
                >
                    🛡️ Fake Resume Scanner
                </button>
            </div>

            {/* Ranking Section */}
            {activeSection === "ranking" && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                    <div className="card">
                        <h3>Select Active Job Post</h3>
                        <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
                            <select 
                                value={selectedJobId} 
                                onChange={(e) => {
                                    const val = e.target.value === "" ? "" : Number(e.target.value);
                                    setSelectedJobId(val);
                                    if (val !== "") handleRankCandidates(val);
                                }}
                                style={{ marginBottom: 0, flex: 1 }}
                            >
                                <option value="">-- Choose Job --</option>
                                {jobs.map((job) => (
                                    <option key={job.id} value={job.id}>{job.title} ({job.location || "Onsite"})</option>
                                ))}
                            </select>
                        </div>
                    </div>

                    {error && (
                        <div className="card" style={{ borderLeft: '4px solid var(--danger)' }}>
                            <p style={{ color: 'var(--danger)', margin: 0 }}>⚠️ {error}</p>
                        </div>
                    )}

                    {loadingPool && (
                        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                            <div className="typing-indicator" style={{ justifyContent: 'center', marginBottom: '1rem' }}>
                                <div className="typing-dot" style={{ width: '10px', height: '10px', backgroundColor: 'var(--accent)' }}></div>
                                <div className="typing-dot" style={{ width: '10px', height: '10px', backgroundColor: 'var(--accent)' }}></div>
                                <div className="typing-dot" style={{ width: '10px', height: '10px', backgroundColor: 'var(--accent)' }}></div>
                            </div>
                            <p style={{ fontWeight: 600, color: 'var(--accent)' }}>Calculating candidate fit weights and vector scores...</p>
                        </div>
                    )}

                    {poolSummary && (
                        <div className="card" style={{ background: 'var(--accent-bg)', borderColor: 'rgba(99, 102, 241, 0.15)' }}>
                            <h4 style={{ color: 'var(--accent)', marginBottom: '0.5rem' }}>🎯 Candidate Pool Summary Report</h4>
                            <p style={{ fontSize: '0.95rem', margin: 0, fontWeight: 600 }}>{poolSummary.summary}</p>
                            <p style={{ fontSize: '0.9rem', margin: '0.5rem 0 0 0', opacity: 0.85 }}>
                                Recruiter Action Plan: <strong>{poolSummary.recommendation}</strong>
                            </p>
                        </div>
                    )}

                    {rankedCandidates.length > 0 && (
                        <div className="card">
                            <h3>Ranked Candidates</h3>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1.25rem' }}>
                                {rankedCandidates.map((c, idx) => (
                                    <div key={idx} style={{ 
                                        padding: '1.25rem', 
                                        background: 'var(--bg)', 
                                        border: '1px solid var(--border)', 
                                        borderRadius: '12px',
                                        display: 'flex',
                                        flexDirection: 'column',
                                        gap: '0.5rem'
                                    }}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                            <span style={{ fontWeight: 700, color: 'var(--text-h)' }}>
                                                🏆 Rank #{c.rank} — {c.name}
                                            </span>
                                            <div style={{ display: 'flex', gap: '0.5rem' }}>
                                                <span className="badge badge-success">{c.tier}</span>
                                                <span className="badge badge-primary">{c.match_score}% Match</span>
                                            </div>
                                        </div>
                                        <p style={{ margin: 0, fontSize: '0.85rem', opacity: 0.8 }}>Email: {c.email}</p>
                                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '0.5rem', fontSize: '0.8rem', marginTop: '0.25rem' }}>
                                            <span>Technical Fit: <strong>{c.technical_match}%</strong></span>
                                            <span>Experience Fit: <strong>{c.experience_match}%</strong></span>
                                            <span>Education Fit: <strong>{c.education_match}%</strong></span>
                                        </div>
                                        <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.85rem', fontStyle: 'italic' }}>
                                            💡 Reason: {c.rank_reason}
                                        </p>
                                        {c.matching_skills.length > 0 && (
                                            <div style={{ display: 'flex', gap: '0.25rem', flexWrap: 'wrap', marginTop: '0.25rem' }}>
                                                {c.matching_skills.map((s, sIdx) => (
                                                    <span key={sIdx} className="badge badge-success" style={{ fontSize: '0.7rem', textTransform: 'none' }}>
                                                        {s}
                                                    </span>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* Duplicates Section */}
            {activeSection === "duplicates" && (
                <div className="card">
                    <h3>Compare Two Resumes (AI Copy Check)</h3>
                    <form onSubmit={handleDetectDuplicates} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1.25rem', background: 'transparent', border: 'none', boxShadow: 'none', padding: 0 }}>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                            <div className="form-group">
                                <label>Resume Text 1</label>
                                <textarea 
                                    value={dupText1} 
                                    onChange={(e) => setDupText1(e.target.value)} 
                                    placeholder="Paste first candidate resume text..."
                                    style={{ height: '220px', resize: 'none' }}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>Resume Text 2</label>
                                <textarea 
                                    value={dupText2} 
                                    onChange={(e) => setDupText2(e.target.value)} 
                                    placeholder="Paste second candidate resume text..."
                                    style={{ height: '220px', resize: 'none' }}
                                    required
                                />
                            </div>
                        </div>

                        <button type="submit" className="btn-primary" disabled={loadingDup}>
                            {loadingDup ? "Comparing..." : "Check Vector Similarity"}
                        </button>
                    </form>

                    {dupResult && (
                        <div style={{ marginTop: '2rem', padding: '1.5rem', background: 'var(--bg)', borderRadius: '12px', border: '1px solid var(--border)' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <h4>Comparison Verdict: {dupResult.verdict}</h4>
                                <span className={`badge ${dupResult.is_duplicate ? "badge-danger" : "badge-success"}`}>
                                    {dupResult.similarity_score}% Similar
                                </span>
                            </div>
                            <div style={{ display: 'flex', gap: '1.5rem', fontSize: '0.9rem', marginTop: '1rem' }}>
                                <span>Vector Cosine Match: <strong>{dupResult.cosine_similarity}%</strong></span>
                                <span>Text/Keyword Overlap: <strong>{dupResult.text_overlap_pct}%</strong></span>
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* Authenticity Section */}
            {activeSection === "authenticity" && (
                <div className="card">
                    <h3>Resume Authenticity Scanner</h3>
                    <p style={{ fontSize: '0.9rem', opacity: 0.8 }}>Check for skill stuffing, missing contact data, unrealistic claims, or dates in the future.</p>
                    
                    <form onSubmit={handleScanAuthenticity} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1.25rem', background: 'transparent', border: 'none', boxShadow: 'none', padding: 0 }}>
                        <textarea 
                            value={authText} 
                            onChange={(e) => setAuthText(e.target.value)} 
                            placeholder="Paste candidate resume text to audit..."
                            style={{ height: '180px', resize: 'none' }}
                            required
                        />
                        <button type="submit" className="btn-primary" disabled={loadingAuth}>
                            {loadingAuth ? "Scanning..." : "Audit Resume Content"}
                        </button>
                    </form>

                    {authResult && (
                        <div style={{ marginTop: '2rem', padding: '1.5rem', background: 'var(--bg)', borderRadius: '12px', border: '1px solid var(--border)' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                                <h4>Scan Verdict: {authResult.verdict}</h4>
                                <span className={`badge ${authResult.authenticity_score >= 85 ? "badge-success" : (authResult.authenticity_score >= 60 ? "badge-warning" : "badge-danger")}`}>
                                    Score: {authResult.authenticity_score}/100
                                </span>
                            </div>

                            <div style={{ marginBottom: '1rem' }}>
                                <strong style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-h)' }}>Red Flags & Inconsistencies Detected:</strong>
                                {authResult.flags.length === 0 ? (
                                    <p style={{ fontSize: '0.9rem', color: 'var(--success)' }}>🟢 No issues detected.</p>
                                ) : (
                                    <ul style={{ paddingLeft: '1.25rem', fontSize: '0.9rem', color: 'var(--danger)', display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                                        {authResult.flags.map((flag, idx) => (
                                            <li key={idx}>{flag}</li>
                                        ))}
                                    </ul>
                                )}
                            </div>

                            <div>
                                <strong style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-h)' }}>Recommendations:</strong>
                                <ul style={{ paddingLeft: '1.25rem', fontSize: '0.9rem', display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                                    {authResult.recommendations.map((rec, idx) => (
                                        <li key={idx} style={{ opacity: 0.85 }}>{rec}</li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default RecruiterPortal;
