import { useState, useEffect } from "react";
import { getDashboardStats } from "../Services/AiService";

type Props = {
    userRole: string;
    onNavigate: (page: string) => void;
}

function Dashboard({ userRole, onNavigate }: Props) {
    const [stats, setStats] = useState<Record<string, any>>({});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const data = await getDashboardStats();
                setStats(data);
            } catch (err) {
                console.error("Error loading dashboard stats:", err);
            } finally {
                setLoading(false);
            }
        };
        fetchStats();
    }, []);

    if (loading) {
        return (
            <div className="page-container" style={{ marginTop: '4rem', textAlign: 'center' }}>
                <p>Loading your dashboard analytics...</p>
            </div>
        );
    }

    return (
        <div className="page-container" style={{ marginTop: '2rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2.5rem' }}>
                <div>
                    <h1 style={{ fontSize: '2.25rem', marginBottom: '0.25rem' }}>Welcome to Jobcart</h1>
                    <p style={{ margin: 0, opacity: 0.8 }}>Here is your role-specific dashboard metrics summary ({userRole.toUpperCase()})</p>
                </div>
                <span className="badge badge-primary" style={{ fontSize: '0.85rem', padding: '0.5rem 1rem' }}>
                    Role: {userRole}
                </span>
            </div>

            {/* Candidate Dashboard View */}
            {userRole === "candidate" && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                    {/* Metrics Grid */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.5rem' }}>
                        <div className="card" style={{ margin: 0, display: 'flex', flexDirection: 'column', justifyItems: 'center', textAlign: 'center' }}>
                            <span style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>📊</span>
                            <span style={{ fontSize: '0.85rem', opacity: 0.7, textTransform: 'uppercase', letterSpacing: '0.05em' }}>ATS Score</span>
                            <h2 style={{ fontSize: '2rem', margin: '0.25rem 0', color: 'var(--accent)' }}>
                                {stats.ats_score ? `${stats.ats_score}%` : "N/A"}
                            </h2>
                            <p style={{ fontSize: '0.8rem', opacity: 0.8, margin: 0 }}>Average resume match weight</p>
                        </div>

                        <div className="card" style={{ margin: 0, display: 'flex', flexDirection: 'column', justifyItems: 'center', textAlign: 'center' }}>
                            <span style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🎯</span>
                            <span style={{ fontSize: '0.85rem', opacity: 0.7, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Applications</span>
                            <h2 style={{ fontSize: '2rem', margin: '0.25rem 0' }}>{stats.total_applications ?? 0}</h2>
                            <button 
                                className="auth-link" 
                                style={{ fontSize: '0.8rem', border: 'none', background: 'none', padding: 0, cursor: 'pointer', margin: 'auto' }}
                                onClick={() => onNavigate("home")}
                            >
                                View active jobs
                            </button>
                        </div>

                        <div className="card" style={{ margin: 0, display: 'flex', flexDirection: 'column', justifyItems: 'center', textAlign: 'center' }}>
                            <span style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🔖</span>
                            <span style={{ fontSize: '0.85rem', opacity: 0.7, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Saved Jobs</span>
                            <h2 style={{ fontSize: '2rem', margin: '0.25rem 0' }}>{stats.saved_jobs ?? 0}</h2>
                            <p style={{ fontSize: '0.8rem', opacity: 0.8, margin: 0 }}>Bookmarked for later</p>
                        </div>

                        <div className="card" style={{ margin: 0, display: 'flex', flexDirection: 'column', justifyItems: 'center', textAlign: 'center' }}>
                            <span style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>⚡</span>
                            <span style={{ fontSize: '0.85rem', opacity: 0.7, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Completion</span>
                            <h2 style={{ fontSize: '2rem', margin: '0.25rem 0', color: 'var(--success)' }}>
                                {stats.profile_completion ?? 0}%
                            </h2>
                            <p style={{ fontSize: '0.8rem', opacity: 0.8, margin: 0 }}>Candidate profile status</p>
                        </div>
                    </div>

                    {/* Quick Shortcuts */}
                    <div className="card">
                        <h3>⚡ AI Career Accelerators</h3>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem', marginTop: '1.25rem' }}>
                            <div style={{ padding: '1.25rem', border: '1px solid var(--border)', borderRadius: '12px', background: 'var(--bg)', cursor: 'pointer' }} onClick={() => onNavigate("chat")}>
                                <h4 style={{ color: 'var(--accent)', marginBottom: '0.25rem' }}>💬 Chat Career Coach</h4>
                                <p style={{ fontSize: '0.85rem', margin: 0 }}>Consult our LLM agent on skill trends and coding practice</p>
                            </div>
                            <div style={{ padding: '1.25rem', border: '1px solid var(--border)', borderRadius: '12px', background: 'var(--bg)', cursor: 'pointer' }} onClick={() => onNavigate("resume")}>
                                <h4 style={{ color: 'var(--accent)', marginBottom: '0.25rem' }}>📄 ATS Resume Reviewer</h4>
                                <p style={{ fontSize: '0.85rem', margin: 0 }}>Paste your resume text to get formatting and keyword improvements</p>
                            </div>
                            <div style={{ padding: '1.25rem', border: '1px solid var(--border)', borderRadius: '12px', background: 'var(--bg)', cursor: 'pointer' }} onClick={() => onNavigate("salary")}>
                                <h4 style={{ color: 'var(--accent)', marginBottom: '0.25rem' }}>💰 Market CTC Predictor</h4>
                                <p style={{ fontSize: '0.85rem', margin: 0 }}>Verify compensation range based on your skills and location</p>
                            </div>
                            <div style={{ padding: '1.25rem', border: '1px solid var(--border)', borderRadius: '12px', background: 'var(--bg)', cursor: 'pointer' }} onClick={() => onNavigate("roadmap")}>
                                <h4 style={{ color: 'var(--accent)', marginBottom: '0.25rem' }}>🗺️ Custom Roadmaps</h4>
                                <p style={{ fontSize: '0.85rem', margin: 0 }}>Generate learning guides and projects to upscale your career</p>
                            </div>
                            <div style={{ padding: '1.25rem', border: '1px solid var(--border)', borderRadius: '12px', background: 'var(--bg)', cursor: 'pointer' }} onClick={() => onNavigate("prep")}>
                                <h4 style={{ color: 'var(--accent)', marginBottom: '0.25rem' }}>📝 Interview MCQ & Mock Prep</h4>
                                <p style={{ fontSize: '0.85rem', margin: 0 }}>Practice roles questions and get instant graded results</p>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Recruiter / Admin Dashboard View */}
            {(userRole === "recruiter" || userRole === "admin") && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.5rem' }}>
                        <div className="card" style={{ margin: 0, display: 'flex', flexDirection: 'column', justifyItems: 'center', textAlign: 'center' }}>
                            <span style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🏢</span>
                            <span style={{ fontSize: '0.85rem', opacity: 0.7, textTransform: 'uppercase', letterSpacing: '0.05em' }}>My Companies</span>
                            <h2 style={{ fontSize: '2rem', margin: '0.25rem 0' }}>{stats.total_companies ?? 0}</h2>
                            <p style={{ fontSize: '0.8rem', opacity: 0.8, margin: 0 }}>Registered business portals</p>
                        </div>

                        <div className="card" style={{ margin: 0, display: 'flex', flexDirection: 'column', justifyItems: 'center', textAlign: 'center' }}>
                            <span style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>💼</span>
                            <span style={{ fontSize: '0.85rem', opacity: 0.7, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Active Postings</span>
                            <h2 style={{ fontSize: '2rem', margin: '0.25rem 0', color: 'var(--accent)' }}>{stats.total_jobs ?? 0}</h2>
                            <p style={{ fontSize: '0.8rem', opacity: 0.8, margin: 0 }}>Jobs accepting applications</p>
                        </div>

                        <div className="card" style={{ margin: 0, display: 'flex', flexDirection: 'column', justifyItems: 'center', textAlign: 'center' }}>
                            <span style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>👥</span>
                            <span style={{ fontSize: '0.85rem', opacity: 0.7, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Received Applications</span>
                            <h2 style={{ fontSize: '2rem', margin: '0.25rem 0', color: 'var(--success)' }}>{stats.total_applications ?? 0}</h2>
                            <p style={{ fontSize: '0.8rem', opacity: 0.8, margin: 0 }}>Applicants awaiting review</p>
                        </div>

                        {userRole === "admin" && (
                            <div className="card" style={{ margin: 0, display: 'flex', flexDirection: 'column', justifyItems: 'center', textAlign: 'center' }}>
                                <span style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🛡️</span>
                                <span style={{ fontSize: '0.85rem', opacity: 0.7, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Platform Users</span>
                                <h2 style={{ fontSize: '2rem', margin: '0.25rem 0' }}>{stats.platform_users ?? 0}</h2>
                                <p style={{ fontSize: '0.8rem', opacity: 0.8, margin: 0 }}>Total users registered</p>
                            </div>
                        )}
                    </div>

                    <div className="card">
                        <h3>🛠️ Recruiter Shortcuts</h3>
                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem', marginTop: '1.25rem' }}>
                            <div style={{ padding: '1.25rem', border: '1px solid var(--border)', borderRadius: '12px', background: 'var(--bg)', cursor: 'pointer' }} onClick={() => onNavigate("recruiter")}>
                                <h4 style={{ color: 'var(--accent)', marginBottom: '0.25rem' }}>📊 Candidate Match Ranker</h4>
                                <p style={{ fontSize: '0.85rem', margin: 0 }}>Compare list of applicants side-by-side using AI matching</p>
                            </div>
                            <div style={{ padding: '1.25rem', border: '1px solid var(--border)', borderRadius: '12px', background: 'var(--bg)', cursor: 'pointer' }} onClick={() => onNavigate("recruiter")}>
                                <h4 style={{ color: 'var(--accent)', marginBottom: '0.25rem' }}>👥 Vector Duplicate Checker</h4>
                                <p style={{ fontSize: '0.85rem', margin: 0 }}>Check two resumes for Jaccard and cosine duplication ratios</p>
                            </div>
                            <div style={{ padding: '1.25rem', border: '1px solid var(--border)', borderRadius: '12px', background: 'var(--bg)', cursor: 'pointer' }} onClick={() => onNavigate("recruiter")}>
                                <h4 style={{ color: 'var(--accent)', marginBottom: '0.25rem' }}>🛡️ Authenticity Verification</h4>
                                <p style={{ fontSize: '0.85rem', margin: 0 }}>Scan text format resumes for credentials inconsistencies</p>
                            </div>
                            <div style={{ padding: '1.25rem', border: '1px solid var(--border)', borderRadius: '12px', background: 'var(--bg)', cursor: 'pointer' }} onClick={() => onNavigate("home")}>
                                <h4 style={{ color: 'var(--accent)', marginBottom: '0.25rem' }}>🏢 Manage Job Postings</h4>
                                <p style={{ fontSize: '0.85rem', margin: 0 }}>Edit details or delete active postings</p>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Dashboard;
