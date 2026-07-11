import { useState, useEffect } from "react";
import { getMyApplications, getJobs, type ApplicationData } from "../Services/JobService";
import type { Job } from "../types/job";

function Applications() {
    const [applications, setApplications] = useState<ApplicationData[]>([]);
    const [jobs, setJobs] = useState<Job[]>([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState("all");

    useEffect(() => {
        fetchData();
    }, []);

    async function fetchData() {
        setLoading(true);
        try {
            const [apps, allJobs] = await Promise.all([
                getMyApplications(),
                getJobs(),
            ]);
            setApplications(apps);
            setJobs(allJobs);
        } catch (err) {
            console.error("Error fetching applications:", err);
        } finally {
            setLoading(false);
        }
    }

    const statusColors: Record<string, { bg: string; color: string; icon: string }> = {
        applied: { bg: "rgba(54, 162, 235, 0.15)", color: "#36a2eb", icon: "📨" },
        under_review: { bg: "rgba(255, 206, 86, 0.15)", color: "#ffce56", icon: "🔍" },
        shortlisted: { bg: "rgba(75, 192, 192, 0.15)", color: "#4bc0c0", icon: "⭐" },
        interview_scheduled: { bg: "rgba(153, 102, 255, 0.15)", color: "#9966ff", icon: "📅" },
        interviewed: { bg: "rgba(255, 159, 64, 0.15)", color: "#ff9f40", icon: "🎤" },
        offered: { bg: "rgba(46, 213, 115, 0.15)", color: "#2ed573", icon: "🎉" },
        accepted: { bg: "rgba(46, 213, 115, 0.2)", color: "#2ed573", icon: "✅" },
        rejected: { bg: "rgba(255, 71, 87, 0.15)", color: "#ff4757", icon: "❌" },
        withdrawn: { bg: "rgba(150, 150, 150, 0.15)", color: "#999", icon: "↩️" },
    };

    const filteredApps = filter === "all"
        ? applications
        : applications.filter(a => a.status === filter);

    const statusCounts = applications.reduce((acc, a) => {
        acc[a.status] = (acc[a.status] || 0) + 1;
        return acc;
    }, {} as Record<string, number>);

    if (loading) {
        return (
            <div className="page-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
                <div style={{ textAlign: 'center', opacity: 0.7 }}>
                    <div style={{ fontSize: '2.5rem', marginBottom: '1rem', animation: 'pulse 1.5s infinite' }}>📋</div>
                    <p>Loading applications…</p>
                </div>
            </div>
        );
    }

    return (
        <div className="page-container" style={{ maxWidth: '1000px', margin: '0 auto', padding: '2rem 1.5rem' }}>
            {/* Header */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
                <div style={{ padding: '0.75rem', background: 'var(--accent-bg)', borderRadius: '15px' }}>
                    <span style={{ fontSize: '1.8rem' }}>📋</span>
                </div>
                <div>
                    <h2 style={{ margin: 0 }}>My Applications</h2>
                    <p style={{ margin: 0, opacity: 0.6 }}>Track all your job applications in one place</p>
                </div>
            </div>

            {/* Stats Row */}
            <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
                <button
                    onClick={() => setFilter("all")}
                    style={{
                        padding: '0.5rem 1rem', borderRadius: '10px', border: 'none', cursor: 'pointer',
                        background: filter === "all" ? 'var(--accent)' : 'var(--card-bg)',
                        color: filter === "all" ? '#fff' : 'inherit',
                        fontWeight: filter === "all" ? 700 : 400,
                        transition: 'all 0.2s',
                    }}
                >
                    All ({applications.length})
                </button>
                {Object.entries(statusCounts).map(([st, count]) => {
                    const s = statusColors[st] || statusColors.applied;
                    return (
                        <button
                            key={st}
                            onClick={() => setFilter(st)}
                            style={{
                                padding: '0.5rem 1rem', borderRadius: '10px', border: 'none', cursor: 'pointer',
                                background: filter === st ? s.color : s.bg,
                                color: filter === st ? '#fff' : s.color,
                                fontWeight: filter === st ? 700 : 500,
                                transition: 'all 0.2s', fontSize: '0.85rem',
                            }}
                        >
                            {s.icon} {st.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase())} ({count})
                        </button>
                    );
                })}
            </div>

            {/* Applications List */}
            {filteredApps.length === 0 ? (
                <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                    <div style={{ fontSize: '3rem', marginBottom: '1rem', opacity: 0.5 }}>📭</div>
                    <h3 style={{ opacity: 0.7 }}>No applications {filter !== "all" ? `with status "${filter}"` : "yet"}</h3>
                    <p style={{ opacity: 0.5 }}>Go to the Jobs section and start applying!</p>
                </div>
            ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                    {filteredApps.map(app => {
                        const job = jobs.find(j => j.id === app.job_id);
                        const s = statusColors[app.status] || statusColors.applied;
                        return (
                            <div key={app.id} className="card" style={{
                                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                                padding: '1.25rem 1.5rem', transition: 'all 0.3s',
                                borderLeft: `4px solid ${s.color}`,
                            }}>
                                <div style={{ flex: 1 }}>
                                    <h3 style={{ margin: '0 0 0.25rem', fontSize: '1.1rem' }}>
                                        {job?.title || `Job #${app.job_id}`}
                                    </h3>
                                    <p style={{ margin: 0, opacity: 0.6, fontSize: '0.85rem' }}>
                                        Applied on {app.applied_at ? new Date(app.applied_at).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }) : "N/A"}
                                    </p>
                                    {app.match_score !== null && app.match_score !== undefined && (
                                        <div style={{ marginTop: '0.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                            <span style={{ fontSize: '0.8rem', opacity: 0.6 }}>Match Score:</span>
                                            <div style={{
                                                width: '100px', height: '6px', borderRadius: '3px',
                                                background: 'rgba(255,255,255,0.1)',
                                            }}>
                                                <div style={{
                                                    width: `${Math.min(app.match_score * 100, 100)}%`,
                                                    height: '100%', borderRadius: '3px',
                                                    background: app.match_score > 0.7 ? '#2ed573' : app.match_score > 0.4 ? '#ffce56' : '#ff4757',
                                                }} />
                                            </div>
                                            <span style={{ fontSize: '0.8rem', fontWeight: 600 }}>
                                                {Math.round(app.match_score * 100)}%
                                            </span>
                                        </div>
                                    )}
                                </div>
                                <div style={{
                                    padding: '0.4rem 1rem', borderRadius: '20px',
                                    background: s.bg, color: s.color,
                                    fontWeight: 600, fontSize: '0.8rem', whiteSpace: 'nowrap',
                                }}>
                                    {s.icon} {app.status.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase())}
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
}

export default Applications;
