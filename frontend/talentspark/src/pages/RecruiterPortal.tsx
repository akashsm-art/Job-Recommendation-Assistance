import { useState, useEffect } from "react";
import { getCompanies } from "../Services/CompanyService";
import { getMyJobs, getJobApplicants, updateApplicationStatus, type ApplicationData } from "../Services/JobService";
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

    const [activeSection, setActiveSection] = useState<"ranking" | "applicants" | "duplicates" | "authenticity">("ranking");
    const [error, setError] = useState("");

    // Applicants management states
    const [selectedApplicantJobId, setSelectedApplicantJobId] = useState<number | "">("");
    const [applicants, setApplicants] = useState<ApplicationData[]>([]);
    const [loadingApplicants, setLoadingApplicants] = useState(false);
    const [actionMsg, setActionMsg] = useState<{ id: number; msg: string; ok: boolean } | null>(null);

    const handleFetchApplicants = async (jobId: number) => {
        setLoadingApplicants(true);
        setError("");
        try {
            const data = await getJobApplicants(jobId);
            setApplicants(data);
        } catch (err: any) {
            setError(err?.response?.data?.detail || "Failed to fetch applicants for this job.");
            setApplicants([]);
        } finally {
            setLoadingApplicants(false);
        }
    };

    const handleStatusChange = async (appId: number, newStatus: string) => {
        setActionMsg(null);
        try {
            await updateApplicationStatus(appId, newStatus);
            setApplicants(prev => prev.map(a => a.id === appId ? { ...a, status: newStatus } : a));
            setActionMsg({ id: appId, msg: `Successfully marked as ${newStatus}!`, ok: true });
            setTimeout(() => setActionMsg(null), 3000);
        } catch (err: any) {
            const msg = err?.response?.data?.detail || "Failed to update status";
            setActionMsg({ id: appId, msg, ok: false });
            setTimeout(() => setActionMsg(null), 4000);
        }
    };

    useEffect(() => {
        const fetchRecruiterData = async () => {
            try {
                const comps = await getCompanies();
                setCompanies(comps);
                const allJobs = await getMyJobs();
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

            <div style={{ display: 'flex', borderBottom: '1px solid var(--border)', marginBottom: '1.5rem', gap: '1.5rem', flexWrap: 'wrap' }}>
                <button 
                    type="button"
                    style={{ border: 'none', background: 'none', padding: '0.5rem 0', borderRadius: 0, color: activeSection === "ranking" ? "var(--accent)" : "var(--text)", borderBottom: activeSection === "ranking" ? "2px solid var(--accent)" : "none", fontWeight: 700 }}
                    onClick={() => setActiveSection("ranking")}
                >
                    📊 Candidate Ranking
                </button>
                <button 
                    type="button"
                    style={{ border: 'none', background: 'none', padding: '0.5rem 0', borderRadius: 0, color: activeSection === "applicants" ? "var(--accent)" : "var(--text)", borderBottom: activeSection === "applicants" ? "2px solid var(--accent)" : "none", fontWeight: 700 }}
                    onClick={() => setActiveSection("applicants")}
                >
                    📋 Job Applicants
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

            {/* Applicants Section */}
            {activeSection === "applicants" && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                    <div className="card">
                        <h3>Job Applicants</h3>
                        <p style={{ margin: 0, opacity: 0.7, fontSize: '0.85rem', marginBottom: '1rem' }}>
                            Select a job to view candidates who applied.
                        </p>
                        <select
                            value={selectedApplicantJobId}
                            onChange={(e) => {
                                const val = e.target.value === "" ? "" : Number(e.target.value);
                                setSelectedApplicantJobId(val);
                                if (val !== "") handleFetchApplicants(val);
                            }}
                            style={{ marginBottom: 0 }}
                        >
                            <option value="">-- Select Job Post --</option>
                            {jobs.map((job) => (
                                <option key={job.id} value={job.id}>{job.title}</option>
                            ))}
                        </select>
                    </div>

                    {loadingApplicants && (
                        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                            <p>Loading applicants list…</p>
                        </div>
                    )}

                    {!loadingApplicants && selectedApplicantJobId && applicants.length === 0 && (
                        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                            <p style={{ opacity: 0.6 }}>No applicants have applied to this job yet.</p>
                        </div>
                    )}

                    {!loadingApplicants && applicants.length > 0 && (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                            {applicants.map((app) => (
                                <div key={app.id} className="card" style={{
                                    borderLeft: `4px solid ${app.status === 'accepted' ? '#2ed573' : app.status === 'rejected' ? '#ff4757' : 'var(--accent)'}`,
                                    display: 'flex',
                                    flexDirection: 'column',
                                    gap: '0.75rem',
                                }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', flexWrap: 'wrap', gap: '0.5rem' }}>
                                        <div>
                                            <h4 style={{ margin: 0 }}>Candidate ID: #{app.user_id}</h4>
                                            <span style={{ fontSize: '0.8rem', opacity: 0.6 }}>
                                                Applied at: {app.applied_at ? new Date(app.applied_at).toLocaleString() : "N/A"}
                                            </span>
                                        </div>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                            {app.match_score !== null && (
                                                <span className="badge badge-primary" style={{ fontWeight: 'bold' }}>
                                                    {Math.round(app.match_score * 100)}% Match
                                                </span>
                                            )}
                                            <span style={{
                                                fontSize: '0.8rem',
                                                padding: '0.2rem 0.6rem',
                                                borderRadius: '12px',
                                                background: app.status === 'accepted' ? 'rgba(46, 213, 115, 0.15)' : app.status === 'rejected' ? 'rgba(255, 71, 87, 0.15)' : 'rgba(255,255,255,0.06)',
                                                color: app.status === 'accepted' ? '#2ed573' : app.status === 'rejected' ? '#ff4757' : 'inherit',
                                                fontWeight: 600,
                                                textTransform: 'capitalize',
                                            }}>
                                                {app.status.replace(/_/g, " ")}
                                            </span>
                                        </div>
                                    </div>

                                    {app.cover_letter && (
                                        <div style={{ padding: '0.75rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px' }}>
                                            <strong style={{ display: 'block', fontSize: '0.8rem', marginBottom: '0.25rem', opacity: 0.7 }}>Cover Letter:</strong>
                                            <p style={{ margin: 0, fontSize: '0.85rem', whiteSpace: 'pre-wrap' }}>{app.cover_letter}</p>
                                        </div>
                                    )}

                                    {app.resume_snapshot && (
                                        <div style={{ padding: '0.75rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px' }}>
                                            <strong style={{ display: 'block', fontSize: '0.8rem', marginBottom: '0.25rem', opacity: 0.7 }}>Resume Text:</strong>
                                            <div style={{ 
                                                maxHeight: '120px', 
                                                overflowY: 'auto', 
                                                fontSize: '0.8rem', 
                                                fontFamily: 'monospace', 
                                                opacity: 0.8,
                                                whiteSpace: 'pre-wrap'
                                            }}>
                                                {app.resume_snapshot}
                                            </div>
                                        </div>
                                    )}

                                    {/* Action Buttons */}
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '0.5rem', flexWrap: 'wrap', gap: '0.5rem' }}>
                                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                                            <button
                                                className="btn-success"
                                                onClick={() => handleStatusChange(app.id, "accepted")}
                                                disabled={app.status === "accepted"}
                                                style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
                                            >
                                                ✅ Accept
                                            </button>
                                            <button
                                                className="btn-danger"
                                                onClick={() => handleStatusChange(app.id, "rejected")}
                                                disabled={app.status === "rejected"}
                                                style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
                                            >
                                                ❌ Reject
                                            </button>
                                        </div>
                                        {actionMsg && actionMsg.id === app.id && (
                                            <span style={{ 
                                                fontSize: '0.85rem', 
                                                fontWeight: 600, 
                                                color: actionMsg.ok ? '#2ed573' : '#ff4757' 
                                            }}>
                                                {actionMsg.msg}
                                            </span>
                                        )}
                                    </div>
                                </div>
                            ))}
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
