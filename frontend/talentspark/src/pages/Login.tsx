import { useState } from "react";
import { login } from "../Services/AuthService";

type Props = {
    onLogin: (token: string) => void;
    onSwitchToRegister: () => void;
}

function Login({ onLogin, onSwitchToRegister }: Props) {
    const [email, setEmail]       = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading]   = useState(false);
    const [error, setError]       = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setLoading(true);
        try {
            const response = await login({ email, password });
            onLogin(response.access_token);
        } catch (err: unknown) {
            let msg = (err as { response?: { data?: { detail?: any } } })?.response?.data?.detail;
            if (typeof msg === "object" && msg !== null) {
                if (Array.isArray(msg)) {
                    msg = msg.map((e: any) => e.msg || JSON.stringify(e)).join(", ");
                } else {
                    msg = msg.message || JSON.stringify(msg);
                }
            }
            setError(typeof msg === "string" ? msg : "Login failed. Please check your credentials.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <div className="auth-header">
                    <div className="auth-logo">🛒</div>
                    <h1 className="auth-title">Welcome Back</h1>
                    <p className="auth-subtitle">Sign in to your Jobcart account</p>
                </div>

                {error && (
                    <div className="auth-error">
                        <span>⚠️</span> {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="form-group">
                        <label className="form-label">Email Address</label>
                        <input
                            id="login-email"
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
                            id="login-password"
                            className="form-input"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Your password"
                            required
                            autoComplete="current-password"
                        />
                    </div>

                    <button
                        id="login-submit"
                        type="submit"
                        className="btn-primary auth-btn"
                        disabled={loading}
                    >
                        {loading ? "Signing in…" : "Sign In"}
                    </button>
                </form>

                <p className="auth-switch">
                    Don't have an account?{" "}
                    <button type="button" className="auth-link" onClick={onSwitchToRegister}>
                        Create one
                    </button>
                </p>
            </div>
        </div>
    );
}

export default Login;