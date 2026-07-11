import { useState } from "react";
import { buildResumeHtml } from "../Services/AiService";

function ResumeBuilder() {
    const [template, setTemplate] = useState("modern");
    const [targetRole, setTargetRole] = useState("Software Engineer");
    const [htmlContent, setHtmlContent] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleBuild = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        setHtmlContent("");

        try {
            const html = await buildResumeHtml(template, targetRole);
            setHtmlContent(html);
        } catch (err) {
            setError("Failed to build resume html. Make sure your user profile is filled.");
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handlePrint = () => {
        const printWindow = window.open("", "_blank");
        if (printWindow) {
            printWindow.document.write(htmlContent);
            printWindow.document.close();
            printWindow.focus();
            printWindow.print();
        }
    };

    return (
        <div className="page-container" style={{ marginTop: '2rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
                <div style={{ padding: '0.75rem', background: 'var(--accent-bg)', borderRadius: '15px' }}>
                    <svg style={{ width: '32px', height: '32px', color: 'var(--accent)' }} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                    </svg>
                </div>
                <div>
                    <h2>AI Resume HTML Builder</h2>
                    <p style={{ margin: 0, opacity: 0.8 }}>Choose a template and compile your profile information into a clean, downloadable resume format</p>
                </div>
            </div>

            <div className="split-pane">
                {/* Left panel */}
                <div className="card">
                    <h3>Resume Options</h3>
                    <form onSubmit={handleBuild} style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '1.25rem', background: 'transparent', border: 'none', boxShadow: 'none', padding: 0 }}>
                        <div className="form-group">
                            <label>Target Role</label>
                            <input 
                                type="text" 
                                value={targetRole} 
                                onChange={(e) => setTargetRole(e.target.value)} 
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label>Select Template</label>
                            <select value={template} onChange={(e) => setTemplate(e.target.value)}>
                                <option value="modern">Modern Accent</option>
                                <option value="minimal">Minimal Clean</option>
                                <option value="corporate">Corporate Formal</option>
                                <option value="ats_friendly">ATS Plain Text</option>
                            </select>
                        </div>

                        <button type="submit" className="btn-primary" disabled={loading} style={{ width: '100%', marginTop: '1rem' }}>
                            {loading ? "Compiling..." : "Build Resume HTML"}
                        </button>
                    </form>
                </div>

                {/* Right panel: Preview */}
                <div>
                    {error && (
                        <div className="card" style={{ borderLeft: '4px solid var(--danger)' }}>
                            <p style={{ color: 'var(--danger)', margin: 0 }}>⚠️ {error}</p>
                        </div>
                    )}

                    {!htmlContent && !loading && (
                        <div className="card" style={{ textAlign: 'center', padding: '3.5rem', opacity: 0.7 }}>
                            <span style={{ fontSize: '3rem', display: 'block', marginBottom: '1rem' }}>📄</span>
                            <h3>Resume Preview Area</h3>
                            <p>Once built, you can preview the generated structure here and print/save to PDF.</p>
                        </div>
                    )}

                    {loading && (
                        <div className="card" style={{ textAlign: 'center', padding: '4rem' }}>
                            <div className="typing-indicator" style={{ justifyContent: 'center', marginBottom: '1rem' }}>
                                <div className="typing-dot" style={{ width: '10px', height: '10px', backgroundColor: 'var(--accent)' }}></div>
                                <div className="typing-dot" style={{ width: '10px', height: '10px', backgroundColor: 'var(--accent)' }}></div>
                                <div className="typing-dot" style={{ width: '10px', height: '10px', backgroundColor: 'var(--accent)' }}></div>
                            </div>
                            <p style={{ fontWeight: 600, color: 'var(--accent)' }}>Pulling profile milestones, skills, and projects...</p>
                        </div>
                    )}

                    {htmlContent && (
                        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <h3>Resume Compiled Successfully!</h3>
                                <button type="button" className="btn-primary" onClick={handlePrint} style={{ padding: '0.4rem 1.25rem', fontSize: '0.85rem' }}>
                                    🖨️ Print / Save PDF
                                </button>
                            </div>

                            <div style={{ 
                                border: '1px solid var(--border)', 
                                borderRadius: '8px', 
                                overflow: 'hidden', 
                                height: '400px', 
                                background: 'white'
                            }}>
                                <iframe 
                                    srcDoc={htmlContent} 
                                    title="Resume Preview" 
                                    style={{ width: '100%', height: '100%', border: 'none' }}
                                />
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default ResumeBuilder;
