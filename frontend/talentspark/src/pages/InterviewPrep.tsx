import { useState } from "react";
import { getInterviewPrep, evaluateInterviewAnswer, getMockInterview, type MockInterviewResponse, type InterviewPrepResponse } from "../Services/AiService";

function InterviewPrep() {
    const [role, setRole] = useState("Software Engineer");
    const [difficulty, setDifficulty] = useState("Medium");
    const [loading, setLoading] = useState(false);
    const [prepData, setPrepData] = useState<InterviewPrepResponse | null>(null);
    const [mockData, setMockData] = useState<MockInterviewResponse | null>(null);
    
    // Feedback Evaluator State
    const [userAnswers, setUserAnswers] = useState<Record<string, string>>({});
    const [evaluations, setEvaluations] = useState<Record<string, any>>({});
    const [evaluating, setEvaluating] = useState<Record<string, boolean>>({});

    const [activeTab, setActiveTab] = useState<"study" | "mock">("study");
    const [error, setError] = useState("");

    const handleGeneratePrep = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        setPrepData(null);
        setMockData(null);
        setEvaluations({});
        setUserAnswers({});

        try {
            if (activeTab === "study") {
                const res = await getInterviewPrep({
                    role,
                    difficulty,
                    categories: ["mcq", "coding", "system_design", "hr", "behavioral"],
                    num_questions: 5
                });
                setPrepData(res);
            } else {
                const res = await getMockInterview(role, difficulty, 3);
                setMockData(res);
            }
        } catch (err: any) {
            setError("Failed to fetch interview questions. Please make sure the backend server is running.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleEvaluate = async (qText: string) => {
        const ans = userAnswers[qText];
        if (!ans || !ans.trim()) return;

        setEvaluating(prev => ({ ...prev, [qText]: true }));
        try {
            const res = await evaluateInterviewAnswer({
                question: qText,
                answer: ans,
                role: role
            });
            setEvaluations(prev => ({ ...prev, [qText]: res }));
        } catch (err) {
            console.error("Evaluation error:", err);
            alert("Error running AI evaluator.");
        } finally {
            setEvaluating(prev => ({ ...prev, [qText]: false }));
        }
    };

    return (
        <div className="page-container" style={{ marginTop: '2rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
                <div style={{ padding: '0.75rem', background: 'var(--accent-bg)', borderRadius: '15px' }}>
                    <svg style={{ width: '32px', height: '32px', color: 'var(--accent)' }} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                    </svg>
                </div>
                <div>
                    <h2>AI Interview Prep & Mock Portal</h2>
                    <p style={{ margin: 0, opacity: 0.8 }}>Get category-wise study material, mock interview rounds, and real-time response evaluations</p>
                </div>
            </div>

            <div className="card">
                <div style={{ display: 'flex', borderBottom: '1px solid var(--border)', marginBottom: '1.5rem', gap: '1.5rem' }}>
                    <button 
                        type="button"
                        style={{ border: 'none', background: 'none', padding: '0.5rem 0', borderRadius: 0, color: activeTab === "study" ? "var(--accent)" : "var(--text)", borderBottom: activeTab === "study" ? "2px solid var(--accent)" : "none", fontWeight: 700 }}
                        onClick={() => { setActiveTab("study"); setPrepData(null); setMockData(null); }}
                    >
                        📚 Study Material & QA
                    </button>
                    <button 
                        type="button"
                        style={{ border: 'none', background: 'none', padding: '0.5rem 0', borderRadius: 0, color: activeTab === "mock" ? "var(--accent)" : "var(--text)", borderBottom: activeTab === "mock" ? "2px solid var(--accent)" : "none", fontWeight: 700 }}
                        onClick={() => { setActiveTab("mock"); setPrepData(null); setMockData(null); }}
                    >
                        🎯 Mock Interview Rounds
                    </button>
                </div>

                <form onSubmit={handleGeneratePrep} style={{ display: 'flex', gap: '1rem', alignItems: 'flex-end', background: 'transparent', border: 'none', boxShadow: 'none', padding: 0 }}>
                    <div className="form-group" style={{ flex: 2, marginBottom: 0 }}>
                        <label>Target Role</label>
                        <input 
                            type="text" 
                            value={role} 
                            onChange={(e) => setRole(e.target.value)} 
                            required
                        />
                    </div>

                    <div className="form-group" style={{ flex: 1, marginBottom: 0 }}>
                        <label>Difficulty</label>
                        <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
                            <option value="Beginner">Beginner</option>
                            <option value="Medium">Medium</option>
                            <option value="Advanced">Advanced</option>
                        </select>
                    </div>

                    <button type="submit" className="btn-primary" disabled={loading} style={{ height: '42px', padding: '0.5rem 2rem' }}>
                        {loading ? "Generating..." : "Generate Preparation"}
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
                    <p style={{ fontWeight: 600, color: 'var(--accent)' }}>Compiling interview questions, answers outlines, and tips...</p>
                </div>
            )}

            {prepData && activeTab === "study" && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                    
                    {/* General Tips */}
                    <div className="card" style={{ background: 'var(--accent-bg)', borderColor: 'rgba(99, 102, 241, 0.15)' }}>
                        <h4 style={{ marginBottom: '0.5rem' }}>💡 Expert Tips for {prepData.role} Interviews</h4>
                        <ul style={{ paddingLeft: '1.25rem', fontSize: '0.9rem', display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
                            {prepData.tips.map((tip, idx) => (
                                <li key={idx} style={{ opacity: 0.85 }}>{tip}</li>
                            ))}
                        </ul>
                    </div>

                    {/* Section 1: MCQs */}
                    {prepData.sections.mcq && prepData.sections.mcq.length > 0 && (
                        <div className="card">
                            <h3>📝 Technical Multiple Choice Questions</h3>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginTop: '1rem' }}>
                                {prepData.sections.mcq.map((item: any, idx: number) => (
                                    <div key={idx} style={{ borderBottom: idx < prepData.sections.mcq.length - 1 ? '1px solid var(--border)' : 'none', paddingBottom: '1rem' }}>
                                        <p style={{ fontWeight: 600, color: 'var(--text-h)' }}>Q{idx+1}. {item.q}</p>
                                        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.5rem', marginTop: '0.5rem' }}>
                                            {item.options.map((opt: string, oIdx: number) => (
                                                <div key={oIdx} style={{ padding: '0.5rem 1rem', background: 'var(--bg)', border: '1px solid var(--border)', borderRadius: '8px', fontSize: '0.85rem' }}>
                                                    {opt}
                                                </div>
                                            ))}
                                        </div>
                                        <div style={{ marginTop: '0.75rem', background: 'var(--success-bg)', padding: '0.75rem', borderRadius: '8px', fontSize: '0.85rem' }}>
                                            🟢 <strong>Correct Answer:</strong> {item.answer}
                                            <p style={{ margin: '0.25rem 0 0 0', opacity: 0.85 }}>{item.explanation}</p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Section 2: Coding */}
                    {prepData.sections.coding && prepData.sections.coding.length > 0 && (
                        <div className="card">
                            <h3>💻 Coding Challenges</h3>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginTop: '1rem' }}>
                                {prepData.sections.coding.map((item: any, idx: number) => (
                                    <div key={idx} style={{ borderBottom: idx < prepData.sections.coding.length - 1 ? '1px solid var(--border)' : 'none', paddingBottom: '1rem' }}>
                                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                            <h4 style={{ margin: 0 }}>{item.title}</h4>
                                            <span className="badge badge-primary">{item.difficulty || "Medium"}</span>
                                        </div>
                                        <p style={{ marginTop: '0.5rem', fontSize: '0.9rem' }}>{item.description}</p>
                                        {item.hint && (
                                            <div style={{ background: 'var(--warning-bg)', padding: '0.5rem 1rem', borderRadius: '8px', fontSize: '0.85rem', color: 'var(--warning)', fontWeight: 600 }}>
                                                💡 Hint: {item.hint}
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Section 3: HR & Behavioral + AI Evaluator */}
                    {prepData.sections.hr_behavioral && prepData.sections.hr_behavioral.length > 0 && (
                        <div className="card">
                            <h3>🗣️ HR & Behavioral Interview (AI Feedback Evaluator)</h3>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginTop: '1rem' }}>
                                {prepData.sections.hr_behavioral.map((item: any, idx: number) => (
                                    <div key={idx} style={{ borderBottom: idx < prepData.sections.hr_behavioral.length - 1 ? '1px solid var(--border)' : 'none', paddingBottom: '1.5rem' }}>
                                        <p style={{ fontWeight: 600, color: 'var(--text-h)', margin: 0 }}>Q{idx+1}. {item.q}</p>
                                        
                                        <textarea
                                            value={userAnswers[item.q] || ""}
                                            onChange={(e) => setUserAnswers(prev => ({ ...prev, [item.q]: e.target.value }))}
                                            placeholder="Type your practice response here..."
                                            style={{ margin: '0.75rem 0', height: '80px', resize: 'none', fontSize: '0.9rem' }}
                                        />

                                        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                                            <button 
                                                type="button" 
                                                className="btn-primary" 
                                                style={{ padding: '0.35rem 1rem', fontSize: '0.8rem' }}
                                                onClick={() => handleEvaluate(item.q)}
                                                disabled={evaluating[item.q] || !(userAnswers[item.q]?.trim())}
                                            >
                                                {evaluating[item.q] ? "Evaluating..." : "Check Response with AI"}
                                            </button>
                                            <span style={{ fontSize: '0.8rem', opacity: 0.7 }}>💡 Tip: {item.tips}</span>
                                        </div>

                                        {evaluations[item.q] && (
                                            <div style={{ marginTop: '1rem', borderLeft: '3px solid var(--accent)', paddingLeft: '1rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                                                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                                                    <span className="badge badge-success" style={{ fontSize: '0.75rem' }}>
                                                        Score: {evaluations[item.q].score}/100
                                                    </span>
                                                    <span style={{ fontSize: '0.8rem', opacity: 0.8 }}>
                                                        Communication: {evaluations[item.q].communication_score} | Tech: {evaluations[item.q].technical_score}
                                                    </span>
                                                </div>
                                                <p style={{ fontSize: '0.85rem', margin: 0 }}>
                                                    <strong>Feedback:</strong> {evaluations[item.q].feedback}
                                                </p>
                                                <div style={{ fontSize: '0.8rem' }}>
                                                    <strong>Suggested Points:</strong> {evaluations[item.q].ideal_answer_outline}
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}

            {mockData && activeTab === "mock" && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                    <div className="card" style={{ background: 'var(--accent-bg)', borderColor: 'rgba(99, 102, 241, 0.15)' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <div>
                                <h3 style={{ margin: 0 }}>Mock Interview Path: {mockData.role}</h3>
                                <span style={{ fontSize: '0.85rem', opacity: 0.8 }}>Total Rounds: <strong>{mockData.total_rounds}</strong> | Total Duration: <strong>{mockData.estimated_duration}</strong></span>
                            </div>
                            <span className="badge badge-primary">{mockData.difficulty}</span>
                        </div>
                    </div>

                    {mockData.rounds.map((rnd, idx) => (
                        <div key={idx} className="card">
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border)', paddingBottom: '0.75rem', marginBottom: '1rem' }}>
                                <h4 style={{ margin: 0 }}>Round {rnd.round}: {rnd.title}</h4>
                                <div style={{ display: 'flex', gap: '0.5rem' }}>
                                    <span className="badge badge-info">{rnd.type}</span>
                                    <span className="badge badge-warning">{rnd.duration}</span>
                                </div>
                            </div>

                            <p style={{ fontSize: '0.9rem', fontWeight: 600 }}>Assessments in this round:</p>
                            <ul style={{ paddingLeft: '1.25rem', fontSize: '0.9rem', marginBottom: '1.5rem', display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
                                {rnd.questions.map((qItem: any, qIdx: number) => (
                                    <li key={qIdx} style={{ opacity: 0.85 }}>
                                        {qItem.q || qItem.title || "Technical Question"}
                                    </li>
                                ))}
                            </ul>

                            <div style={{ background: 'var(--bg)', padding: '1rem', borderRadius: '10px', fontSize: '0.8rem' }}>
                                📋 <strong>Scoring Criteria:</strong> {rnd.scoring.criteria ? rnd.scoring.criteria.join(", ") : `Pass threshold: ${rnd.scoring.pass_threshold}%`}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default InterviewPrep;
