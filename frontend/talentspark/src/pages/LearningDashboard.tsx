import { useState, useEffect } from "react";
import { getSkillValueAnalysis } from "../Services/AiService";

interface Course {
    title: string;
    provider: string;
    url: string;
    rating: number;
    duration: string;
    difficulty: string;
    is_free: boolean;
    has_certificate: boolean;
    price?: string;
    estimated_completion?: string;
}

function LearningDashboard() {
    const [skillsAnalysis, setSkillsAnalysis] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    // Custom learning tracking (mock state persisted in session/local)
    const [myCourses, setMyCourses] = useState<Array<{ course: Course; progress: number; status: string }>>([
        {
            course: {
                title: "Python for Everybody",
                provider: "Coursera",
                url: "https://www.coursera.org/specializations/python",
                rating: 4.8,
                duration: "8 months",
                difficulty: "Beginner",
                is_free: true,
                has_certificate: true
            },
            progress: 60,
            status: "🔄 In Progress"
        },
        {
            course: {
                title: "Docker Mastery",
                provider: "Udemy",
                url: "https://www.udemy.com/course/docker-mastery/",
                rating: 4.7,
                duration: "20 hours",
                difficulty: "Intermediate",
                is_free: false,
                has_certificate: true
            },
            progress: 10,
            status: "🔄 In Progress"
        }
    ]);

    useEffect(() => {
        const loadAnalysis = async () => {
            try {
                const analysis = await getSkillValueAnalysis();
                setSkillsAnalysis(analysis);
            } catch (err) {
                console.error(err);
                setError("Could not load skill market analysis.");
            } finally {
                setLoading(false);
            }
        };
        loadAnalysis();
    }, []);

    const updateProgress = (title: string, amount: number) => {
        setMyCourses(prev => prev.map(c => {
            if (c.course.title === title) {
                const nextProg = Math.min(100, c.progress + amount);
                return {
                    ...c,
                    progress: nextProg,
                    status: nextProg === 100 ? "✅ Completed" : "🔄 In Progress"
                };
            }
            return c;
        }));
    };

    return (
        <div className="page-container" style={{ marginTop: '2rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
                <div style={{ padding: '0.75rem', background: 'var(--accent-bg)', borderRadius: '15px' }}>
                    <svg style={{ width: '32px', height: '32px', color: 'var(--accent)' }} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                    </svg>
                </div>
                <div>
                    <h2>My Learning & Upskilling Dashboard</h2>
                    <p style={{ margin: 0, opacity: 0.8 }}>Track your course progress, evaluate your skill set market value, and study in-demand technologies</p>
                </div>
            </div>

            <div className="split-pane">
                {/* Left panel: Active Courses progress */}
                <div className="card">
                    <h3>Active Learning Courses</h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', marginTop: '1.25rem' }}>
                        {myCourses.map((c, idx) => (
                            <div key={idx} style={{ 
                                padding: '1rem', 
                                background: 'var(--bg)', 
                                border: '1px solid var(--border)', 
                                borderRadius: '12px' 
                            }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                    <strong style={{ fontSize: '0.95rem', color: 'var(--text-h)' }}>{c.course.title}</strong>
                                    <span className="badge badge-primary" style={{ fontSize: '0.7rem' }}>{c.course.provider}</span>
                                </div>
                                
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.85rem', opacity: 0.8, margin: '0.5rem 0' }}>
                                    <span>Difficulty: <strong>{c.course.difficulty}</strong></span>
                                    <span>{c.status}</span>
                                </div>

                                {/* Progress Bar */}
                                <div style={{ width: '100%', height: '8px', background: 'var(--border)', borderRadius: '100px', overflow: 'hidden', margin: '0.75rem 0' }}>
                                    <div style={{ width: `${c.progress}%`, height: '100%', background: 'var(--accent-gradient)', borderRadius: '100px' }}></div>
                                </div>

                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.8rem' }}>
                                    <span>Progress: {c.progress}%</span>
                                    {c.progress < 100 && (
                                        <button 
                                            type="button" 
                                            onClick={() => updateProgress(c.course.title, 10)}
                                            style={{ padding: '0.2rem 0.6rem', fontSize: '0.75rem', borderRadius: '6px' }}
                                        >
                                            📚 Study +10%
                                        </button>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Right panel: Skill market value */}
                <div>
                    {error && (
                        <div className="card" style={{ borderLeft: '4px solid var(--danger)' }}>
                            <p style={{ color: 'var(--danger)', margin: 0 }}>⚠️ {error}</p>
                        </div>
                    )}

                    {loading && (
                        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
                            <p>Calculating market values...</p>
                        </div>
                    )}

                    {skillsAnalysis && (
                        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <h3>Market Value Audit</h3>
                                <span className="badge badge-success" style={{ fontSize: '0.75rem' }}>
                                    Hike Boost: +{skillsAnalysis.estimated_salary_boost_pct}%
                                </span>
                            </div>

                            <div style={{ textAlign: 'center', background: 'var(--accent-bg)', padding: '1rem', borderRadius: '12px' }}>
                                <span style={{ fontSize: '0.8rem', opacity: 0.8, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Market Readiness Score</span>
                                <h1 style={{ fontSize: '2.5rem', margin: '0.25rem 0' }}>{skillsAnalysis.market_readiness.score}/100</h1>
                                <span style={{ fontWeight: 600, color: 'var(--accent)' }}>{skillsAnalysis.market_readiness.level}</span>
                            </div>

                            {/* Trending skills list */}
                            {skillsAnalysis.trending_skills.length > 0 && (
                                <div>
                                    <strong style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-h)', fontSize: '0.9rem' }}>📈 Your In-Demand Skills:</strong>
                                    <div style={{ display: 'flex', gap: '0.35rem', flexWrap: 'wrap' }}>
                                        {skillsAnalysis.trending_skills.map((s: any, sIdx: number) => (
                                            <span key={sIdx} className="badge badge-success" style={{ fontSize: '0.75rem', textTransform: 'none' }}>
                                                {s.skill} (+{s.growth_pct}% demand)
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {/* Recommended upskills */}
                            <div>
                                <strong style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-h)', fontSize: '0.9rem' }}>🎯 Actions & Mentorship Recommendations:</strong>
                                <ul style={{ paddingLeft: '1.25rem', fontSize: '0.85rem', display: 'flex', flexDirection: 'column', gap: '0.35rem', margin: 0 }}>
                                    {skillsAnalysis.recommendations.map((rec: string, rIdx: number) => (
                                        <li key={rIdx} style={{ opacity: 0.85 }}>{rec}</li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default LearningDashboard;
