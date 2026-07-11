import { useState } from "react";
import { getCareerRoadmap, type CareerRoadmapResponse } from "../Services/AiService";

function CareerRoadmap() {
    const [targetRole, setTargetRole] = useState("AI Engineer");
    const [useLlm, setUseLlm] = useState(false);
    
    const [loading, setLoading] = useState(false);
    const [roadmap, setRoadmap] = useState<CareerRoadmapResponse | null>(null);
    const [error, setError] = useState("");

    const handleGenerate = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        setRoadmap(null);

        try {
            const res = await getCareerRoadmap({ target_role: targetRole, use_llm: useLlm });
            setRoadmap(res);
        } catch (err: any) {
            setError("Failed to generate career roadmap. Please make sure the backend is online.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page-container" style={{ marginTop: '2rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
                <div style={{ padding: '0.75rem', background: 'var(--accent-bg)', borderRadius: '15px' }}>
                    <svg style={{ width: '32px', height: '32px', color: 'var(--accent)' }} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7"></path>
                    </svg>
                </div>
                <div>
                    <h2>AI Career Roadmap</h2>
                    <p style={{ margin: 0, opacity: 0.8 }}>Map out custom learning pathways and project-based milestones tailored for transitions</p>
                </div>
            </div>

            <div className="card">
                <h3>Select Target Career Goal</h3>
                <form onSubmit={handleGenerate} style={{ display: 'flex', gap: '1rem', alignItems: 'flex-end', marginTop: '1rem', background: 'transparent', border: 'none', boxShadow: 'none', padding: 0 }}>
                    <div className="form-group" style={{ flex: 1, marginBottom: 0 }}>
                        <label>What role are you targeting?</label>
                        <select 
                            value={targetRole} 
                            onChange={(e) => setTargetRole(e.target.value)}
                            style={{ marginBottom: 0 }}
                        >
                            <option value="AI Engineer">AI / Machine Learning Engineer</option>
                            <option value="Full Stack Developer">Full Stack Web Developer</option>
                            <option value="DevOps Engineer">DevOps / Cloud Platform Engineer</option>
                            <option value="Data Scientist">Data Scientist / Analyst</option>
                        </select>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
                        <input 
                            type="checkbox" 
                            id="use-llm-roadmap" 
                            checked={useLlm} 
                            onChange={(e) => setUseLlm(e.target.checked)}
                            style={{ width: 'auto', marginBottom: 0 }}
                        />
                        <label htmlFor="use-llm-roadmap" style={{ marginBottom: 0, cursor: 'pointer', whiteSpace: 'nowrap' }}>AI Custom (Slower)</label>
                    </div>

                    <button type="submit" className="btn-primary" disabled={loading} style={{ height: '42px', padding: '0.5rem 2rem' }}>
                        {loading ? "Generating..." : "Plan Path"}
                    </button>
                </form>
            </div>

            {error && (
                <div className="card" style={{ borderLeft: '4px solid var(--danger)' }}>
                    <p style={{ color: 'var(--danger)', margin: 0 }}>⚠️ {error}</p>
                </div>
            )}

            {loading && (
                <div className="card" style={{ textAlign: 'center', padding: '4rem' }}>
                    <div className="typing-indicator" style={{ justifyContent: 'center', marginBottom: '1rem' }}>
                        <div className="typing-dot" style={{ width: '10px', height: '10px', backgroundColor: 'var(--accent)' }}></div>
                        <div className="typing-dot" style={{ width: '10px', height: '10px', backgroundColor: 'var(--accent)' }}></div>
                        <div className="typing-dot" style={{ width: '10px', height: '10px', backgroundColor: 'var(--accent)' }}></div>
                    </div>
                    <p style={{ fontWeight: 600, color: 'var(--accent)' }}>Mapping curriculum, learning stages, and certification goals...</p>
                </div>
            )}

            {roadmap && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                    <div className="card" style={{ background: 'var(--accent-bg)', borderColor: 'rgba(99, 102, 241, 0.15)' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
                            <div>
                                <span style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em', opacity: 0.8 }}>Target Curriculum</span>
                                <h2 style={{ fontSize: '1.5rem', margin: '0.25rem 0' }}>{roadmap.title}</h2>
                                <span style={{ fontSize: '0.9rem', opacity: 0.8 }}>Timeline: <strong>{roadmap.estimated_duration}</strong></span>
                            </div>
                            <div style={{ textAlign: 'right' }}>
                                <span style={{ fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em', opacity: 0.8 }}>Profile Readiness</span>
                                <h1 style={{ fontSize: '2.5rem', margin: 0, color: 'var(--accent)' }}>{roadmap.overall_readiness}%</h1>
                            </div>
                        </div>
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem', position: 'relative', paddingLeft: '1rem' }}>
                        {roadmap.phases.map((phase, idx) => (
                            <div key={idx} className="card" style={{ margin: 0, position: 'relative' }}>
                                <div style={{ 
                                    position: 'absolute', 
                                    left: '-2rem', 
                                    top: '2rem', 
                                    width: '32px', 
                                    height: '32px', 
                                    background: 'var(--accent-gradient)', 
                                    color: 'white', 
                                    borderRadius: '50%', 
                                    display: 'flex', 
                                    alignItems: 'center', 
                                    justifyContent: 'center', 
                                    fontWeight: 'bold',
                                    fontSize: '0.9rem',
                                    boxShadow: 'var(--shadow-sm)'
                                }}>
                                    {phase.phase}
                                </div>

                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', borderBottom: '1px solid var(--border)', paddingBottom: '0.75rem' }}>
                                    <h3 style={{ margin: 0 }}>{phase.title}</h3>
                                    <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                                        <span className="badge badge-info">{phase.adjusted_duration || phase.duration}</span>
                                        <span className="badge badge-success">{phase.status}</span>
                                    </div>
                                </div>

                                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem', marginTop: '1rem' }}>
                                    <div>
                                        <strong style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-h)' }}>🎯 Target Skills</strong>
                                        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem' }}>
                                            {phase.skills.map((skill, sIdx) => (
                                                <span key={sIdx} className="badge badge-primary" style={{ textTransform: 'none', fontSize: '0.75rem' }}>
                                                    {skill}
                                                </span>
                                            ))}
                                        </div>
                                    </div>

                                    <div>
                                        <strong style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-h)' }}>📚 Suggested Resources</strong>
                                        <ul style={{ paddingLeft: '1.25rem', margin: 0, fontSize: '0.9rem' }}>
                                            {phase.resources.map((res, rIdx) => (
                                                <li key={rIdx} style={{ opacity: 0.85 }}>{res}</li>
                                            ))}
                                        </ul>
                                    </div>
                                </div>

                                <div style={{ marginTop: '1.5rem', background: 'var(--bg)', padding: '1rem', borderRadius: '10px' }}>
                                    <strong style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-h)' }}>💻 Hands-On Project Assignment:</strong>
                                    <ul style={{ paddingLeft: '1.25rem', margin: 0, fontSize: '0.9rem' }}>
                                        {phase.projects.map((proj, pIdx) => (
                                            <li key={pIdx} style={{ opacity: 0.85 }}>{proj}</li>
                                        ))}
                                    </ul>
                                </div>

                                <div style={{ marginTop: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.85rem', opacity: 0.8 }}>
                                    <span>🏁 Phase Milestone: <strong>{phase.milestone}</strong></span>
                                    <span>Stage Completion: <strong>{phase.completion_pct}%</strong></span>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="card">
                        <h3>💡 Mentorship & Action Guidelines</h3>
                        <ul style={{ paddingLeft: '1.25rem', display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '1rem' }}>
                            {roadmap.tips.map((tip, idx) => (
                                <li key={idx} style={{ opacity: 0.85 }}>{tip}</li>
                            ))}
                        </ul>
                    </div>
                </div>
            )}
        </div>
    );
}

export default CareerRoadmap;
