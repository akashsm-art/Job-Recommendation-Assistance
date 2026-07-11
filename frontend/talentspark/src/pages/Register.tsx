import { useState } from "react";
import { register } from "../Services/AuthService";

type Props = {
    onSwitchToLogin: () => void;
}

const ROLE_OPTIONS = [
    { label: "🔍 Job Seeker",     value: "candidate",   desc: "Browse and apply to job opportunities" },
    { label: "📋 Job Recruiter",  value: "recruiter",   desc: "Post and manage job listings" },
];

function Register({ onSwitchToLogin }: Props) {
    const [name, setName]         = useState("");
    const [email, setEmail]       = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole]         = useState("candidate");
    const [loading, setLoading]   = useState(false);
    const [error, setError]       = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setLoading(true);
        try {
            await register({ name, email, password, role });
            alert("Registration successful! Please login.");
            onSwitchToLogin();
        } catch (err: unknown) {
            let msg = (err as { response?: { data?: { detail?: any } } })?.response?.data?.detail;
            if (typeof msg === "object" && msg !== null) {
                if (Array.isArray(msg)) {
                    msg = msg.map((e: any) => e.msg || JSON.stringify(e)).join(", ");
                } else {
                    msg = msg.message || JSON.stringify(msg);
                }
            }
            setError(typeof msg === "string" ? msg : "Registration failed. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                {/* Header */}
                <div className="auth-header">
                    <div className="auth-logo">🛒</div>
                    <h1 className="auth-title">Create Account</h1>
                    <p className="auth-subtitle">Join Jobcart and get started</p>
                </div>

                {error && (
                    <div className="auth-error">
                        <span>⚠️</span> {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="form-group">
                        <label className="form-label">Full Name</label>
                        <input
                            id="register-name"
                            className="form-input"
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            placeholder="e.g. Jane Doe"
                            required
                            autoComplete="name"
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">Email Address</label>
                        <input
                            id="register-email"
                            className="form-input"
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="you@example.com"
                            required
                            autoComplete="email"
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">Password</label>
                        <input
                            id="register-password"
                            className="form-input"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Minimum 6 characters"
                            required
                            minLength={6}
                            autoComplete="new-password"
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">I am a…</label>
                        <div className="role-selector">
                            {ROLE_OPTIONS.map((opt) => (
                                <label
                                    key={opt.value}
                                    className={`role-option ${role === opt.value ? "role-option-active" : ""}`}
                                >
                                    <input
                                        type="radio"
                                        name="role"
                                        value={opt.value}
                                        checked={role === opt.value}
                                        onChange={() => setRole(opt.value)}
                                        style={{ display: "none" }}
                                    />
                                    <span className="role-option-label">{opt.label}</span>
                                    <span className="role-option-desc">{opt.desc}</span>
                                </label>
                            ))}
                        </div>
                    </div>

                    <button
                        id="register-submit"
                        type="submit"
                        className="btn-primary auth-btn"
                        disabled={loading}
                    >
                        {loading ? "Creating account…" : "Create Account"}
                    </button>
                </form>

                <p className="auth-switch">
                    Already have an account?{" "}
                    <button type="button" className="auth-link" onClick={onSwitchToLogin}>
                        Sign in
                    </button>
                </p>
            </div>
        </div>
    );
}

export default Register;
