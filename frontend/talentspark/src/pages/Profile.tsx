import { useState, useEffect } from "react";
import { getProfile, updateProfile } from "../Services/JobService";

function Profile() {
    const [profile, setProfile] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [success, setSuccess] = useState("");
    const [error, setError] = useState("");
    const [activeTab, setActiveTab] = useState("personal");

    const [form, setForm] = useState({
        full_name: "",
        phone: "",
        dob: "",
        gender: "",
        nationality: "",
        languages_known: "",
        current_address: "",
        linkedin: "",
        github: "",
        portfolio: "",
        current_company: "",
        experience_years: "",
        current_ctc: "",
        expected_ctc: "",
        notice_period: "",
        preferred_role: "",
        preferred_location: "",
        expected_salary: "",
        work_mode: "",
        highest_qualification: "",
        university: "",
        cgpa: "",
        career_objective: "",
    });

    useEffect(() => {
        fetchProfile();
    }, []);

    async function fetchProfile() {
        setLoading(true);
        try {
            const data = await getProfile();
            setProfile(data);
            setForm({
                full_name: data.full_name || "",
                phone: data.phone || "",
                dob: data.dob || "",
                gender: data.gender || "",
                nationality: data.nationality || "",
                languages_known: Array.isArray(data.languages_known) ? data.languages_known.join(", ") : "",
                current_address: data.current_address || "",
                linkedin: data.linkedin || "",
                github: data.github || "",
                portfolio: data.portfolio || "",
                current_company: data.current_company || "",
                experience_years: data.experience_years?.toString() || "",
                current_ctc: data.current_ctc?.toString() || "",
                expected_ctc: data.expected_ctc?.toString() || "",
                notice_period: data.notice_period || "",
                preferred_role: data.preferred_role || "",
                preferred_location: data.preferred_location || "",
                expected_salary: data.expected_salary?.toString() || "",
                work_mode: data.work_mode || "",
                highest_qualification: data.highest_qualification || "",
                university: data.university || "",
                cgpa: data.cgpa?.toString() || "",
                career_objective: data.career_objective || "",
            });
        } catch (err) {
            setError("Failed to load profile");
        } finally {
            setLoading(false);
        }
    }

    async function handleSave() {
        setSaving(true);
        setError("");
        setSuccess("");
        try {
            const payload: any = { ...form };
            // Convert numeric fields
            if (payload.experience_years) payload.experience_years = parseFloat(payload.experience_years);
            else payload.experience_years = null;
            if (payload.current_ctc) payload.current_ctc = parseFloat(payload.current_ctc);
            else payload.current_ctc = null;
            if (payload.expected_ctc) payload.expected_ctc = parseFloat(payload.expected_ctc);
            else payload.expected_ctc = null;
            if (payload.expected_salary) payload.expected_salary = parseFloat(payload.expected_salary);
            else payload.expected_salary = null;
            if (payload.cgpa) payload.cgpa = parseFloat(payload.cgpa);
            else payload.cgpa = null;
            // Convert languages to array
            if (payload.languages_known) {
                payload.languages_known = payload.languages_known.split(",").map((s: string) => s.trim()).filter(Boolean);
            } else {
                payload.languages_known = null;
            }
            // Convert empty date to null
            if (!payload.dob) payload.dob = null;

            await updateProfile(payload);
            setSuccess("Profile saved successfully!");
            setTimeout(() => setSuccess(""), 3000);
        } catch (err: any) {
            setError(err?.response?.data?.detail || "Failed to save profile");
        } finally {
            setSaving(false);
        }
    }

    const tabs = [
        { key: "personal", label: "👤 Personal", icon: "👤" },
        { key: "professional", label: "💼 Professional", icon: "💼" },
        { key: "education", label: "🎓 Education", icon: "🎓" },
        { key: "social", label: "🔗 Social Links", icon: "🔗" },
        { key: "skills", label: "⚡ Skills", icon: "⚡" },
    ];

    if (loading) {
        return (
            <div className="page-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
                <div style={{ textAlign: 'center', opacity: 0.7 }}>
                    <div style={{ fontSize: '2.5rem', marginBottom: '1rem', animation: 'pulse 1.5s infinite' }}>👤</div>
                    <p>Loading profile…</p>
                </div>
            </div>
        );
    }

    return (
        <div className="page-container" style={{ maxWidth: '900px', margin: '0 auto', padding: '2rem 1.5rem' }}>
            {/* Header */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
                <div style={{
                    width: '70px', height: '70px', borderRadius: '50%',
                    background: 'linear-gradient(135deg, var(--accent), #7c3aed)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: '2rem', color: '#fff', fontWeight: 700,
                    boxShadow: '0 4px 15px rgba(124, 58, 237, 0.3)',
                }}>
                    {(form.full_name || "U")[0].toUpperCase()}
                </div>
                <div>
                    <h2 style={{ margin: 0, fontSize: '1.6rem' }}>{form.full_name || "Your Profile"}</h2>
                    <p style={{ margin: 0, opacity: 0.6 }}>{profile?.email}</p>
                    <span className="badge badge-primary" style={{ marginTop: '0.25rem' }}>
                        {profile?.role?.toUpperCase()}
                    </span>
                </div>
            </div>

            {/* Alerts */}
            {error && (
                <div style={{
                    padding: '0.75rem 1rem', borderRadius: '10px',
                    background: 'rgba(255, 71, 87, 0.15)', border: '1px solid rgba(255, 71, 87, 0.3)',
                    color: '#ff4757', marginBottom: '1rem',
                }}>⚠️ {error}</div>
            )}
            {success && (
                <div style={{
                    padding: '0.75rem 1rem', borderRadius: '10px',
                    background: 'rgba(46, 213, 115, 0.15)', border: '1px solid rgba(46, 213, 115, 0.3)',
                    color: '#2ed573', marginBottom: '1rem',
                }}>✅ {success}</div>
            )}

            {/* Tab Navigation */}
            <div style={{
                display: 'flex', gap: '0.5rem', marginBottom: '1.5rem', overflowX: 'auto',
                borderBottom: '2px solid rgba(255,255,255,0.06)', paddingBottom: '0.5rem',
            }}>
                {tabs.map(t => (
                    <button
                        key={t.key}
                        onClick={() => setActiveTab(t.key)}
                        style={{
                            padding: '0.5rem 1rem', borderRadius: '10px 10px 0 0', border: 'none',
                            background: activeTab === t.key ? 'var(--accent-bg)' : 'transparent',
                            color: activeTab === t.key ? 'var(--accent)' : 'inherit',
                            fontWeight: activeTab === t.key ? 700 : 400,
                            cursor: 'pointer', fontSize: '0.85rem', whiteSpace: 'nowrap',
                            borderBottom: activeTab === t.key ? '2px solid var(--accent)' : '2px solid transparent',
                            transition: 'all 0.2s',
                        }}
                    >
                        {t.label}
                    </button>
                ))}
            </div>

            {/* Personal Tab */}
            {activeTab === "personal" && (
                <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <h3 style={{ color: 'var(--accent)', margin: 0 }}>Personal Information</h3>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                        <div>
                            <label>Full Name</label>
                            <input type="text" value={form.full_name} onChange={e => setForm({ ...form, full_name: e.target.value })} placeholder="Your full name" />
                        </div>
                        <div>
                            <label>Phone</label>
                            <input type="text" value={form.phone} onChange={e => setForm({ ...form, phone: e.target.value })} placeholder="+91 98765 43210" />
                        </div>
                        <div>
                            <label>Date of Birth</label>
                            <input type="date" value={form.dob} onChange={e => setForm({ ...form, dob: e.target.value })} />
                        </div>
                        <div>
                            <label>Gender</label>
                            <select value={form.gender} onChange={e => setForm({ ...form, gender: e.target.value })}>
                                <option value="">Select</option>
                                <option value="male">Male</option>
                                <option value="female">Female</option>
                                <option value="other">Other</option>
                                <option value="prefer_not_to_say">Prefer not to say</option>
                            </select>
                        </div>
                        <div>
                            <label>Nationality</label>
                            <input type="text" value={form.nationality} onChange={e => setForm({ ...form, nationality: e.target.value })} placeholder="e.g. Indian" />
                        </div>
                        <div>
                            <label>Languages Known</label>
                            <input type="text" value={form.languages_known} onChange={e => setForm({ ...form, languages_known: e.target.value })} placeholder="English, Hindi, Tamil" />
                        </div>
                    </div>
                    <div>
                        <label>Current Address</label>
                        <textarea value={form.current_address} onChange={e => setForm({ ...form, current_address: e.target.value })} placeholder="Your current address" rows={2} style={{ resize: 'vertical' }} />
                    </div>
                </div>
            )}

            {/* Professional Tab */}
            {activeTab === "professional" && (
                <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <h3 style={{ color: 'var(--accent)', margin: 0 }}>Professional Details</h3>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                        <div>
                            <label>Current Company</label>
                            <input type="text" value={form.current_company} onChange={e => setForm({ ...form, current_company: e.target.value })} placeholder="e.g. Google" />
                        </div>
                        <div>
                            <label>Experience (Years)</label>
                            <input type="number" step="0.5" value={form.experience_years} onChange={e => setForm({ ...form, experience_years: e.target.value })} placeholder="e.g. 3" />
                        </div>
                        <div>
                            <label>Current CTC (₹ LPA)</label>
                            <input type="number" value={form.current_ctc} onChange={e => setForm({ ...form, current_ctc: e.target.value })} placeholder="e.g. 12" />
                        </div>
                        <div>
                            <label>Expected CTC (₹ LPA)</label>
                            <input type="number" value={form.expected_ctc} onChange={e => setForm({ ...form, expected_ctc: e.target.value })} placeholder="e.g. 18" />
                        </div>
                        <div>
                            <label>Notice Period</label>
                            <select value={form.notice_period} onChange={e => setForm({ ...form, notice_period: e.target.value })}>
                                <option value="">Select</option>
                                <option value="Immediate">Immediate</option>
                                <option value="15 days">15 days</option>
                                <option value="1 month">1 month</option>
                                <option value="2 months">2 months</option>
                                <option value="3 months">3 months</option>
                            </select>
                        </div>
                        <div>
                            <label>Work Mode</label>
                            <select value={form.work_mode} onChange={e => setForm({ ...form, work_mode: e.target.value })}>
                                <option value="">Select</option>
                                <option value="remote">Remote</option>
                                <option value="hybrid">Hybrid</option>
                                <option value="onsite">Onsite</option>
                            </select>
                        </div>
                    </div>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                        <div>
                            <label>Preferred Role</label>
                            <input type="text" value={form.preferred_role} onChange={e => setForm({ ...form, preferred_role: e.target.value })} placeholder="e.g. Full Stack Developer" />
                        </div>
                        <div>
                            <label>Preferred Location</label>
                            <input type="text" value={form.preferred_location} onChange={e => setForm({ ...form, preferred_location: e.target.value })} placeholder="e.g. Bangalore, Remote" />
                        </div>
                    </div>
                    <div>
                        <label>Career Objective</label>
                        <textarea value={form.career_objective} onChange={e => setForm({ ...form, career_objective: e.target.value })} placeholder="Your career objective..." rows={3} style={{ resize: 'vertical' }} />
                    </div>
                </div>
            )}

            {/* Education Tab */}
            {activeTab === "education" && (
                <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <h3 style={{ color: 'var(--accent)', margin: 0 }}>Education</h3>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                        <div>
                            <label>Highest Qualification</label>
                            <select value={form.highest_qualification} onChange={e => setForm({ ...form, highest_qualification: e.target.value })}>
                                <option value="">Select</option>
                                <option value="High School">High School</option>
                                <option value="Diploma">Diploma</option>
                                <option value="Bachelor's">Bachelor's</option>
                                <option value="Master's">Master's</option>
                                <option value="PhD">PhD</option>
                            </select>
                        </div>
                        <div>
                            <label>CGPA / Percentage</label>
                            <input type="number" step="0.01" value={form.cgpa} onChange={e => setForm({ ...form, cgpa: e.target.value })} placeholder="e.g. 8.5" />
                        </div>
                    </div>
                    <div>
                        <label>University / College</label>
                        <input type="text" value={form.university} onChange={e => setForm({ ...form, university: e.target.value })} placeholder="e.g. IIT Delhi" />
                    </div>
                </div>
            )}

            {/* Social Links Tab */}
            {activeTab === "social" && (
                <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <h3 style={{ color: 'var(--accent)', margin: 0 }}>Social & Portfolio Links</h3>
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                        <div>
                            <label>🔗 LinkedIn</label>
                            <input type="url" value={form.linkedin} onChange={e => setForm({ ...form, linkedin: e.target.value })} placeholder="https://linkedin.com/in/..." />
                        </div>
                        <div>
                            <label>💻 GitHub</label>
                            <input type="url" value={form.github} onChange={e => setForm({ ...form, github: e.target.value })} placeholder="https://github.com/..." />
                        </div>
                        <div style={{ gridColumn: '1 / -1' }}>
                            <label>🌐 Portfolio</label>
                            <input type="url" value={form.portfolio} onChange={e => setForm({ ...form, portfolio: e.target.value })} placeholder="https://your-portfolio.com" />
                        </div>
                    </div>
                </div>
            )}

            {/* Skills Tab */}
            {activeTab === "skills" && (
                <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <h3 style={{ color: 'var(--accent)', margin: 0 }}>Skills (from Resume)</h3>
                    <p style={{ opacity: 0.6, fontSize: '0.85rem' }}>
                        Skills are auto-populated when you upload your resume in the Analyser. Below are your current skills.
                    </p>
                    {profile?.technical_skills?.length > 0 && (
                        <div>
                            <label style={{ marginBottom: '0.5rem', display: 'block', fontWeight: 600 }}>Technical Skills</label>
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
                                {profile.technical_skills.map((s: string, i: number) => (
                                    <span key={i} className="badge badge-primary">{s}</span>
                                ))}
                            </div>
                        </div>
                    )}
                    {profile?.programming_languages?.length > 0 && (
                        <div>
                            <label style={{ marginBottom: '0.5rem', display: 'block', fontWeight: 600 }}>Programming Languages</label>
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
                                {profile.programming_languages.map((s: string, i: number) => (
                                    <span key={i} className="badge badge-info">{s}</span>
                                ))}
                            </div>
                        </div>
                    )}
                    {profile?.frameworks?.length > 0 && (
                        <div>
                            <label style={{ marginBottom: '0.5rem', display: 'block', fontWeight: 600 }}>Frameworks</label>
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
                                {profile.frameworks.map((s: string, i: number) => (
                                    <span key={i} className="badge badge-warning">{s}</span>
                                ))}
                            </div>
                        </div>
                    )}
                    {(!profile?.technical_skills?.length && !profile?.programming_languages?.length && !profile?.frameworks?.length) && (
                        <div style={{ textAlign: 'center', padding: '2rem', opacity: 0.5 }}>
                            <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>📄</div>
                            <p>No skills found. Upload your resume in the Analyser to auto-populate.</p>
                        </div>
                    )}
                </div>
            )}

            {/* Save Button */}
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1.5rem', gap: '0.75rem' }}>
                <button className="btn-primary" onClick={handleSave} disabled={saving}
                    style={{
                        padding: '0.75rem 2.5rem', fontSize: '1rem', borderRadius: '12px',
                        background: 'linear-gradient(135deg, var(--accent), #7c3aed)',
                        boxShadow: '0 4px 15px rgba(124, 58, 237, 0.3)',
                        transition: 'all 0.3s',
                    }}
                >
                    {saving ? "Saving…" : "💾 Save Profile"}
                </button>
            </div>
        </div>
    );
}

export default Profile;
