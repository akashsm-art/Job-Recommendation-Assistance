import { useState, useRef } from "react";
import type { DragEvent, ChangeEvent } from "react";
import { analyseResumeFile, semanticSearch } from "../Services/RagService";
import { applyToJob } from "../Services/JobService";
import type { SemanticSearchResult } from "../types/rag";

function ResumeAnalyser() {
    const [file, setFile] = useState<File | null>(null);
    const [analysis, setAnalysis] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [isDragOver, setIsDragOver] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    // Matching Jobs Flow
    const [matchingJobs, setMatchingJobs] = useState<SemanticSearchResult[]>([]);
    const [loadingMatches, setLoadingMatches] = useState(false);
    const [showMatches, setShowMatches] = useState(false);
    const [appliedJobs, setAppliedJobs] = useState<Set<number>>(new Set());
    const [applyingId, setApplyingId] = useState<number | null>(null);
    const [applyMsg, setApplyMsg] = useState<{ id: number; msg: string; ok: boolean } | null>(null);

    const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        setIsDragOver(true);
    };

    const handleDragLeave = () => {
        setIsDragOver(false);
    };

    const handleDrop = (e: DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        setIsDragOver(false);
        setError("");
        
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            const droppedFile = e.dataTransfer.files[0];
            validateAndSetFile(droppedFile);
        }
    };

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        setError("");
        if (e.target.files && e.target.files.length > 0) {
            validateAndSetFile(e.target.files[0]);
        }
    };

    const validateAndSetFile = (selectedFile: File) => {
        const allowedTypes = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"];
        const ext = selectedFile.name.split('.').pop()?.toLowerCase();
        
        if (allowedTypes.includes(selectedFile.type) || ["pdf", "docx", "txt"].includes(ext || "")) {
            setFile(selectedFile);
        } else {
            setError("Unsupported file format. Please upload a .pdf, .docx, or .txt file.");
            setFile(null);
        }
    };

    const handleAnalyse = async () => {
        if (!file) return;
        setLoading(true);
        setAnalysis("");
        setError("");
        setMatchingJobs([]);
        setShowMatches(false);
        try {
            const result = await analyseResumeFile(file);
            setAnalysis(result.analysis);
        } catch (err: any) {
            setError(err.response?.data?.detail || "Failed to analyse resume. Please check if the backend is running and valid.");
        } finally {
            setLoading(false);
        }
    };

    const triggerFileSelect = () => {
        fileInputRef.current?.click();
    };

    // Parse Markdown response into structured sections
    const parseAnalysisMarkdown = (text: string) => {
        const sections: {
            overall?: string;
            strengths: string[];
            improvements: string[];
            suggestions: string[];
            ats?: string;
            jobs: string[];
        } = {
            strengths: [],
            improvements: [],
            suggestions: [],
            jobs: []
        };

        const lines = text.split("\n");
        let currentSection: "overall" | "strengths" | "improvements" | "suggestions" | "ats" | "jobs" | null = null;

        for (let line of lines) {
            const trimmed = line.trim();
            if (!trimmed) continue;

            // Section header matching
            if (trimmed.toLowerCase().includes("overall impression")) {
                currentSection = "overall";
                continue;
            } else if (trimmed.toLowerCase().includes("strength")) {
                currentSection = "strengths";
                continue;
            } else if (trimmed.toLowerCase().includes("improvement") || trimmed.toLowerCase().includes("weakness")) {
                currentSection = "improvements";
                continue;
            } else if (trimmed.toLowerCase().includes("suggestion")) {
                currentSection = "suggestions";
                continue;
            } else if (trimmed.toLowerCase().includes("ats compatibility") || trimmed.toLowerCase().includes("estimated ats")) {
                currentSection = "ats";
                const matches = trimmed.match(/(high|medium|low)/i);
                if (matches) {
                    sections.ats = matches[0].toUpperCase();
                }
                continue;
            } else if (trimmed.toLowerCase().includes("recommended job") || trimmed.toLowerCase().includes("job titles")) {
                currentSection = "jobs";
                continue;
            }

            // Add to section
            if (currentSection === "overall") {
                sections.overall = (sections.overall || "") + " " + trimmed.replace(/^[#*-:\s]+/, "");
            } else if (currentSection === "strengths") {
                if (trimmed.match(/^[0-9#*-:\s]+/) || trimmed.startsWith("-") || trimmed.startsWith("*")) {
                    sections.strengths.push(trimmed.replace(/^[0-9#*-:\s.]+/, ""));
                }
            } else if (currentSection === "improvements") {
                if (trimmed.match(/^[0-9#*-:\s]+/) || trimmed.startsWith("-") || trimmed.startsWith("*")) {
                    sections.improvements.push(trimmed.replace(/^[0-9#*-:\s.]+/, ""));
                }
            } else if (currentSection === "suggestions") {
                if (trimmed.match(/^[0-9#*-:\s]+/) || trimmed.startsWith("-") || trimmed.startsWith("*")) {
                    sections.suggestions.push(trimmed.replace(/^[0-9#*-:\s.]+/, ""));
                }
            } else if (currentSection === "ats") {
                if (!sections.ats) {
                    const matches = trimmed.match(/(high|medium|low)/i);
                    if (matches) {
                        sections.ats = matches[0].toUpperCase();
                    } else {
                        sections.ats = trimmed.replace(/^[#*-:\s]+/, "");
                    }
                }
            } else if (currentSection === "jobs") {
                if (trimmed.match(/^[0-9#*-:\s]+/) || trimmed.startsWith("-") || trimmed.startsWith("*")) {
                    sections.jobs.push(trimmed.replace(/^[0-9#*-:\s.]+/, ""));
                } else {
                    const roles = trimmed.replace(/^[#*-:\s]+/, "").split(",");
                    if (roles.length > 1) {
                        sections.jobs.push(...roles.map(r => r.trim()).filter(Boolean));
                    } else {
                        sections.jobs.push(trimmed.replace(/^[#*-:\s]+/, ""));
                    }
                }
            }
        }

        if (sections.strengths.length === 0 && sections.improvements.length === 0 && sections.suggestions.length === 0) {
            return null;
        }

        return sections;
    };

    const sections = analysis ? parseAnalysisMarkdown(analysis) : null;

    const handleFindMatchingJobs = async () => {
        if (!sections || sections.jobs.length === 0) return;
        const searchQuery = sections.jobs.join(", ");
        setLoadingMatches(true);
        setShowMatches(true);
        try {
            const data = await semanticSearch(searchQuery);
            setMatchingJobs(data.results || []);
        } catch (err) {
            console.error("Error searching matching jobs:", err);
        } finally {
            setLoadingMatches(false);
        }
    };

    const handleApplyJob = async (jobId: number) => {
        if (jobId === null) return;
        setApplyingId(jobId);
        setApplyMsg(null);
        try {
            await applyToJob(jobId);
            setAppliedJobs(prev => new Set([...prev, jobId]));
            setApplyMsg({ id: jobId, msg: "Applied! 🎉", ok: true });
            setTimeout(() => setApplyMsg(null), 3000);
        } catch (err: any) {
            setApplyMsg({ id: jobId, msg: err?.response?.data?.detail || "Failed to apply", ok: false });
            setTimeout(() => setApplyMsg(null), 4000);
        } finally {
            setApplyingId(null);
        }
    };

    return (
        <div className="page-container" style={{ marginTop: '2rem', maxWidth: '1200px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
                <div style={{ padding: '0.75rem', background: 'var(--accent-bg)', borderRadius: '15px' }}>
                    <svg style={{ width: '32px', height: '32px', color: 'var(--accent)' }} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                    </svg>
                </div>
                <div>
                    <h2>Resume AI Analyser</h2>
                    <p style={{ margin: 0, opacity: 0.8 }}>Upload your resume file (.pdf, .docx, .txt) to receive instant feedback on skills, gaps, and roles</p>
                </div>
            </div>

            <div className="split-pane" style={{ display: 'grid', gridTemplateColumns: '1fr 1.5fr', gap: '2rem', alignItems: 'start' }}>
                {/* Left Pane - Upload zone */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                        <h3 style={{ margin: 0 }}>Resume File</h3>
                        
                        <div 
                            className={`drop-zone ${isDragOver ? 'dragover' : ''}`}
                            onDragOver={handleDragOver}
                            onDragLeave={handleDragLeave}
                            onDrop={handleDrop}
                            onClick={triggerFileSelect}
                        >
                            <span className="drop-zone-icon">📁</span>
                            <span className="drop-zone-text">
                                {file ? file.name : "Drag & Drop your resume here"}
                            </span>
                            <span className="drop-zone-subtext">
                                {file ? `${(file.size / 1024 / 1024).toFixed(2)} MB` : "or click to browse (.pdf, .docx, .txt)"}
                            </span>
                            <input 
                                type="file" 
                                ref={fileInputRef}
                                onChange={handleFileChange}
                                accept=".pdf,.docx,.txt"
                                style={{ display: 'none' }}
                            />
                        </div>

                        {error && (
                            <div style={{ color: 'var(--danger)', fontSize: '0.9rem', textAlign: 'center' }}>
                                ⚠️ {error}
                            </div>
                        )}
                        
                        <button
                            className="btn-primary"
                            onClick={handleAnalyse}
                            disabled={loading || !file}
                            style={{ width: '100%' }}
                        >
                            {loading ? "Analysing Resume..." : "Run AI Resume Review"}
                        </button>
                    </div>
                </div>

                {/* Right Pane - Results */}
                <div>
                    <div className="card" style={{ minHeight: '400px', display: 'flex', flexDirection: 'column' }}>
                        <h3 style={{ borderBottom: '1px solid var(--border)', paddingBottom: '0.75rem', marginBottom: '1.25rem', color: 'var(--accent)', margin: 0 }}>
                            📋 AI Feedback Report
                        </h3>
                        
                        {!analysis && !loading && (
                            <div style={{ margin: 'auto', textAlign: 'center', opacity: 0.6, padding: '2rem' }}>
                                <span style={{ fontSize: '2.5rem', display: 'block', marginBottom: '0.5rem' }}>🔍</span>
                                <p>Upload your resume details on the left panel to generate a career feedback report.</p>
                            </div>
                        )}

                        {loading && (
                            <div style={{ margin: 'auto', textAlign: 'center', opacity: 0.8 }}>
                                <div className="typing-indicator" style={{ justifyContent: 'center', marginBottom: '1rem' }}>
                                    <div className="typing-dot" style={{ width: '10px', height: '10px', background: 'var(--accent)' }}></div>
                                    <div className="typing-dot" style={{ width: '10px', height: '10px', background: 'var(--accent)' }}></div>
                                    <div className="typing-dot" style={{ width: '10px', height: '10px', background: 'var(--accent)' }}></div>
                                </div>
                                <p style={{ fontWeight: 600, color: 'var(--accent)' }}>Llama-3.3 is reading your resume...</p>
                            </div>
                        )}

                        {analysis && sections && (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                                {/* ATS Compatibility */}
                                {sections.ats && (
                                    <div style={{
                                        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                                        padding: '1rem', borderRadius: '12px', background: 'rgba(255,255,255,0.03)',
                                        border: '1px solid var(--border)'
                                    }}>
                                        <div>
                                            <h4 style={{ margin: 0 }}>Estimated ATS Compatibility</h4>
                                            <p style={{ margin: 0, fontSize: '0.8rem', opacity: 0.6 }}>Based on keyword optimization and formatting checks</p>
                                        </div>
                                        <span className={`badge ${sections.ats === "HIGH" ? "badge-success" : sections.ats === "MEDIUM" ? "badge-warning" : "badge-danger"}`}
                                            style={{ padding: '0.5rem 1rem', fontSize: '0.9rem', fontWeight: 'bold' }}>
                                            {sections.ats}
                                        </span>
                                    </div>
                                )}

                                {/* Overall impression */}
                                {sections.overall && (
                                    <div style={{ padding: '1rem', borderRadius: '12px', background: 'var(--accent-bg)', borderLeft: '4px solid var(--accent)' }}>
                                        <h4 style={{ margin: '0 0 0.5rem 0', color: 'var(--accent)' }}>Summary</h4>
                                        <p style={{ margin: 0, fontSize: '0.9rem', lineHeight: 1.5 }}>{sections.overall}</p>
                                    </div>
                                )}

                                {/* Strengths */}
                                {sections.strengths.length > 0 && (
                                    <div>
                                        <h4 style={{ color: '#2ed573', margin: '0 0 0.5rem 0' }}>🟢 Key Strengths</h4>
                                        <ul style={{ margin: 0, paddingLeft: '1.25rem', fontSize: '0.9rem', lineHeight: 1.6 }}>
                                            {sections.strengths.map((s, idx) => <li key={idx}>{s}</li>)}
                                        </ul>
                                    </div>
                                )}

                                {/* Areas for Improvement */}
                                {sections.improvements.length > 0 && (
                                    <div>
                                        <h4 style={{ color: '#ff9f40', margin: '0 0 0.5rem 0' }}>🟠 Areas for Improvement</h4>
                                        <ul style={{ margin: 0, paddingLeft: '1.25rem', fontSize: '0.9rem', lineHeight: 1.6 }}>
                                            {sections.improvements.map((s, idx) => <li key={idx}>{s}</li>)}
                                        </ul>
                                    </div>
                                )}

                                {/* Actionable Suggestions */}
                                {sections.suggestions.length > 0 && (
                                    <div>
                                        <h4 style={{ color: 'var(--accent)', margin: '0 0 0.5rem 0' }}>💡 Actionable Suggestions</h4>
                                        <ul style={{ margin: 0, paddingLeft: '1.25rem', fontSize: '0.9rem', lineHeight: 1.6 }}>
                                            {sections.suggestions.map((s, idx) => <li key={idx}>{s}</li>)}
                                        </ul>
                                    </div>
                                )}

                                {/* Job Recommendations */}
                                {sections.jobs.length > 0 && (
                                    <div>
                                        <h4 style={{ margin: '0 0 0.75rem 0' }}>💼 Suggested Job Titles</h4>
                                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                                            {sections.jobs.map((s, idx) => (
                                                <span key={idx} className="badge badge-primary" style={{ padding: '0.35rem 0.75rem', fontSize: '0.8rem' }}>
                                                    {s}
                                                </span>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Find Matching Jobs Action */}
                                {sections.jobs.length > 0 && (
                                    <div style={{ borderTop: '1px solid var(--border)', paddingTop: '1.5rem', marginTop: '0.5rem' }}>
                                        <button 
                                            className="btn-primary" 
                                            onClick={handleFindMatchingJobs}
                                            style={{ width: '100%', padding: '0.75rem', fontSize: '1rem', fontWeight: 'bold' }}
                                        >
                                            🔍 Find Matching Jobs In Jobcart
                                        </button>
                                    </div>
                                )}
                            </div>
                        )}

                        {/* Fallback to raw text if parsing failed */}
                        {analysis && !sections && (
                            <div style={{ flex: 1, overflowY: 'auto', paddingRight: '0.5rem' }}>
                                <div style={{ fontSize: '0.95rem', lineHeight: '1.7', whiteSpace: 'pre-line' }}>
                                    {analysis}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>

            {/* Matches Display Section */}
            {showMatches && (
                <div className="card" style={{ marginTop: '2rem' }}>
                    <h3 style={{ borderBottom: '1px solid var(--border)', paddingBottom: '0.75rem', marginBottom: '1.5rem' }}>
                        🎯 AI Vector Search Results
                    </h3>

                    {loadingMatches && (
                        <div style={{ textAlign: 'center', padding: '2rem' }}>
                            <p>Searching for company vacancies...</p>
                        </div>
                    )}

                    {!loadingMatches && matchingJobs.length === 0 && (
                        <div style={{ textAlign: 'center', padding: '2rem', opacity: 0.6 }}>
                            <p>No direct matching vacancies found. Try updating your resume keywords.</p>
                        </div>
                    )}

                    {!loadingMatches && matchingJobs.length > 0 && (
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem' }}>
                            {matchingJobs.map((job, idx) => (
                                <div key={idx} style={{ 
                                    padding: '1.25rem', 
                                    background: 'var(--bg)', 
                                    border: '1px solid var(--border)', 
                                    borderRadius: '12px',
                                    display: 'flex',
                                    flexDirection: 'column',
                                    justifyContent: 'space-between',
                                    gap: '0.75rem'
                                }}>
                                    <div>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                                            <h4 style={{ margin: 0 }}>{job.title}</h4>
                                            <span style={{ fontSize: '0.8rem', fontWeight: 'bold', color: 'var(--success)' }}>
                                                {Math.round(job.score * 100)}% Match
                                            </span>
                                        </div>
                                        {job.salary !== null && (
                                            <p style={{ margin: '0.25rem 0', color: 'var(--accent)', fontWeight: 600, fontSize: '0.85rem' }}>
                                                💵 INR {job.salary.toLocaleString()}
                                            </p>
                                        )}
                                        <p style={{ 
                                            margin: '0.5rem 0 0 0', 
                                            fontSize: '0.8rem', 
                                            opacity: 0.8,
                                            display: '-webkit-box',
                                            WebkitLineClamp: 3,
                                            WebkitBoxOrient: 'vertical',
                                            overflow: 'hidden'
                                        }}>
                                            {job.description}
                                        </p>
                                    </div>

                                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderTop: '1px solid rgba(255,255,255,0.04)', paddingTop: '0.75rem', marginTop: '0.5rem' }}>
                                        {job.job_id !== null ? (
                                            appliedJobs.has(job.job_id) ? (
                                                <button disabled style={{
                                                    background: 'rgba(46, 213, 115, 0.15)', color: '#2ed573',
                                                    border: '1px solid rgba(46, 213, 115, 0.3)',
                                                    cursor: 'default', fontWeight: 600, padding: '0.35rem 1rem', fontSize: '0.85rem'
                                                }}>
                                                    ✅ Applied
                                                </button>
                                            ) : (
                                                <button
                                                    className="btn-primary"
                                                    onClick={() => job.job_id !== null && handleApplyJob(job.job_id)}
                                                    disabled={applyingId === job.job_id}
                                                    style={{ padding: '0.35rem 1.25rem', fontSize: '0.85rem', fontWeight: 600 }}
                                                >
                                                    {applyingId === job.job_id ? "Applying…" : "🚀 Apply"}
                                                </button>
                                            )
                                        ) : (
                                            <span style={{ fontSize: '0.85rem', opacity: 0.5 }}>Info Only</span>
                                        )}

                                        {applyMsg && applyMsg.id === job.job_id && (
                                            <span style={{ 
                                                fontSize: '0.8rem', 
                                                fontWeight: 600, 
                                                color: applyMsg.ok ? '#2ed573' : '#ff4757' 
                                            }}>
                                                {applyMsg.msg}
                                            </span>
                                        )}
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default ResumeAnalyser;
