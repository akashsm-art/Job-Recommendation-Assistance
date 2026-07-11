import { useState } from "react";
import { predictSalary, type SalaryPredictionResponse } from "../Services/AiService";

function SalaryPredictor() {
    const [role, setRole] = useState("Software Engineer");
    const [experience, setExperience] = useState<number>(3);
    const [skillsInput, setSkillsInput] = useState("Python, React, SQL");
    const [location, setLocation] = useState("Bangalore");
    const [currentCtc, setCurrentCtc] = useState<number | "">("");
    const [education, setEducation] = useState("B.Tech Computer Science");
    const [useLlm, setUseLlm] = useState(false);
    
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<SalaryPredictionResponse | null>(null);
    const [error, setError] = useState("");

    const handlePredict = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        setResult(null);

        const skills = skillsInput.split(",").map(s => s.trim()).filter(Boolean);

        try {
            const data = await predictSalary({
                role,
                experience_years: Number(experience),
                skills,
                location: location || undefined,
                current_ctc: currentCtc ? Number(currentCtc) : undefined,
                education: education || undefined,
                use_llm: useLlm
            });
            setResult(data);
        } catch (err: any) {
            setError("Failed to calculate salary prediction. Please try again.");
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
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                </div>
                <div>
                    <h2>AI Salary Predictor</h2>
                    <p style={{ margin: 0, opacity: 0.8 }}>Get realistic salary predictions and market demand analysis powered by AI reasoning</p>
                </div>
            </div>

            <div className="split-pane">
                {/* Left panel: Input Form */}
                <div className="card">
                    <h3>Prediction Criteria</h3>
                    <form onSubmit={handlePredict} style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem', marginTop: '1rem', background: 'transparent', border: 'none', boxShadow: 'none', padding: 0 }}>
                        <div className="form-group">
                            <label>Target Role / Title</label>
                            <input 
                                type="text" 
                                value={role} 
                                onChange={(e) => setRole(e.target.value)} 
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label>Experience (Years)</label>
                            <input 
                                type="number" 
                                min="0" 
                                max="40" 
                                step="0.5"
                                value={experience} 
                                onChange={(e) => setExperience(Number(e.target.value))} 
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label>Skills (Comma-separated)</label>
                            <textarea 
                                value={skillsInput} 
                                onChange={(e) => setSkillsInput(e.target.value)} 
                                placeholder="React, Node.js, AWS, Kubernetes"
                                style={{ height: '80px', resize: 'none' }}
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label>Preferred Location</label>
                            <input 
                                type="text" 
                                value={location} 
                                onChange={(e) => setLocation(e.target.value)} 
                                placeholder="e.g. Bangalore, Remote, Pune"
                            />
                        </div>

                        <div className="form-group">
                            <label>Current CTC (LPA) - Optional</label>
                            <input 
                                type="number" 
                                value={currentCtc} 
                                onChange={(e) => setCurrentCtc(e.target.value === "" ? "" : Number(e.target.value))} 
                                placeholder="e.g. 8"
                            />
                        </div>

                        <div className="form-group">
                            <label>Highest Education / University</label>
                            <input 
                                type="text" 
                                value={education} 
                                onChange={(e) => setEducation(e.target.value)} 
                                placeholder="e.g. B.Tech IIT, MCA, BCA"
                            />
                        </div>

                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem' }}>
                            <input 
                                type="checkbox" 
                                id="use-llm" 
                                checked={useLlm} 
                                onChange={(e) => setUseLlm(e.target.checked)}
                                style={{ width: 'auto', marginBottom: 0 }}
                            />
                            <label htmlFor="use-llm" style={{ marginBottom: 0, cursor: 'pointer' }}>Use Deep AI LLM Reasoning (Slower)</label>
                        </div>

                        <button type="submit" className="btn-primary" disabled={loading} style={{ width: '100%' }}>
                            {loading ? "Calculating..." : "Predict Market CTC"}
                        </button>
                    </form>
                </div>

                {/* Right panel: Results */}
                <div>
                    {error && (
                        <div className="card" style={{ borderLeft: '4px solid var(--danger)' }}>
                            <p style={{ color: 'var(--danger)', margin: 0 }}>⚠️ {error}</p>
                        </div>
                    )}

                    {!result && !loading && (
                        <div className="card" style={{ textAlign: 'center', padding: '3rem', opacity: 0.7 }}>
                            <span style={{ fontSize: '3rem', display: 'block', marginBottom: '1rem' }}>💰</span>
                            <h3>Enter your details</h3>
                            <p>Calculate target market range, potential hikes, and premium skill upgrades</p>
                        </div>
                    )}

                    {loading && (
                        <div className="card" style={{ textAlign: 'center', padding: '4rem' }}>
                            <div className="typing-indicator" style={{ justifyContent: 'center', marginBottom: '1rem' }}>
                                <div className="typing-dot" style={{ width: '10px', height: '10px', backgroundColor: 'var(--accent)' }}></div>
                                <div className="typing-dot" style={{ width: '10px', height: '10px', backgroundColor: 'var(--accent)' }}></div>
                                <div className="typing-dot" style={{ width: '10px', height: '10px', backgroundColor: 'var(--accent)' }}></div>
                            </div>
                            <p style={{ fontWeight: 600, color: 'var(--accent)' }}>Running predictive salary models...</p>
                        </div>
                    )}

                    {result && (
                        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <span className="badge badge-success">{result.market_trend}</span>
                                <span style={{ fontSize: '0.85rem', opacity: 0.7 }}>Confidence: {result.confidence_pct}%</span>
                            </div>

                            <div style={{ textAlign: 'center', margin: '1rem 0' }}>
                                <span style={{ fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.05em', opacity: 0.7 }}>Predicted Salary Range</span>
                                <h1 style={{ fontSize: '2.5rem', margin: '0.5rem 0' }}>
                                    ₹{result.predicted_min_lpa} - ₹{result.predicted_max_lpa} <span style={{ fontSize: '1.25rem', fontWeight: 500 }}>LPA</span>
                                </h1>
                                <p style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--accent)' }}>
                                    Recommended Ask: ₹{result.recommended_ctc_lpa} LPA
                                </p>
                            </div>

                            {result.hike_percentage !== null && result.hike_percentage !== undefined && (
                                <div style={{ background: 'var(--success-bg)', padding: '1rem', borderRadius: '12px', textAlign: 'center' }}>
                                    <span style={{ fontSize: '0.9rem', color: 'var(--success)', fontWeight: 700 }}>
                                        📈 Predicted hike over current CTC: {result.hike_percentage}%
                                    </span>
                                </div>
                            )}

                            <div>
                                <h4 style={{ marginBottom: '0.75rem' }}>Core Influence Factors:</h4>
                                <ul style={{ listStyleType: 'none', display: 'flex', flexDirection: 'column', gap: '0.5rem', paddingLeft: 0 }}>
                                    {result.factors.map((f, idx) => (
                                        <li key={idx} style={{ fontSize: '0.9rem', opacity: 0.85 }}>{f}</li>
                                    ))}
                                </ul>
                            </div>

                            {result.premium_skills.length > 0 && (
                                <div>
                                    <h4 style={{ marginBottom: '0.5rem' }}>Your Premium Value Additions:</h4>
                                    <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                                        {result.premium_skills.map((skill, idx) => (
                                            <span key={idx} className="badge badge-primary">{skill}</span>
                                        ))}
                                    </div>
                                </div>
                            )}

                            {result.reasoning && (
                                <div style={{ borderTop: '1px solid var(--border)', paddingTop: '1rem' }}>
                                    <h4 style={{ marginBottom: '0.5rem' }}>AI Expert Insight:</h4>
                                    <p style={{ fontSize: '0.9rem', opacity: 0.85, fontStyle: 'italic', margin: 0 }}>
                                        {result.reasoning}
                                    </p>
                                </div>
                            )}

                            {result.negotiation_tips && result.negotiation_tips.length > 0 && (
                                <div style={{ borderTop: '1px solid var(--border)', paddingTop: '1rem' }}>
                                    <h4 style={{ marginBottom: '0.5rem' }}>Compensation Negotiation Tips:</h4>
                                    <ul style={{ paddingLeft: '1.25rem', fontSize: '0.9rem', display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
                                        {result.negotiation_tips.map((tip, idx) => (
                                            <li key={idx} style={{ opacity: 0.85 }}>{tip}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default SalaryPredictor;
