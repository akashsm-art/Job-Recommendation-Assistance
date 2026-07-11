type Props = {
    currentPage: string;
    onNavigate: (page: string) => void;
    onLogout?: () => void;
    userRole: string;
}

function NavBar({ currentPage, onNavigate, onLogout, userRole }: Props) {
    const isRecruiterOrAdmin = userRole === "recruiter" || userRole === "admin";

    return (
        <nav style={{ flexWrap: 'wrap', gap: '0.5rem', borderRadius: '15px', padding: '0.75rem 1.5rem' }}>
            <div className="nav-brand" style={{ cursor: 'pointer' }} onClick={() => onNavigate("dashboard")}>
                🛒 Jobcart
            </div>
            
            <div className="nav-links" style={{ flexWrap: 'wrap', gap: '0.35rem' }}>
                <button 
                    className={currentPage === "dashboard" ? "active" : ""} 
                    onClick={() => onNavigate("dashboard")}
                    style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
                >
                    Dashboard
                </button>
                <button 
                    className={currentPage === "home" ? "active" : ""} 
                    onClick={() => onNavigate("home")}
                    style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
                >
                    Jobs
                </button>
                <button 
                    className={currentPage === "chat" ? "active" : ""} 
                    onClick={() => onNavigate("chat")}
                    style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
                >
                    AI Coach
                </button>
                <button 
                    className={currentPage === "resume" ? "active" : ""} 
                    onClick={() => onNavigate("resume")}
                    style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
                >
                    Analyser
                </button>
                <button 
                    className={currentPage === "jobmatch" ? "active" : ""} 
                    onClick={() => onNavigate("jobmatch")}
                    style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
                >
                    Job Match
                </button>
                <button 
                    className={currentPage === "salary" ? "active" : ""} 
                    onClick={() => onNavigate("salary")}
                    style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
                >
                    Salary
                </button>
                <button 
                    className={currentPage === "roadmap" ? "active" : ""} 
                    onClick={() => onNavigate("roadmap")}
                    style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
                >
                    Roadmap
                </button>
                <button 
                    className={currentPage === "prep" ? "active" : ""} 
                    onClick={() => onNavigate("prep")}
                    style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
                >
                    Interview
                </button>
                <button 
                    className={currentPage === "learning" ? "active" : ""} 
                    onClick={() => onNavigate("learning")}
                    style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
                >
                    Learning
                </button>
                <button 
                    className={currentPage === "builder" ? "active" : ""} 
                    onClick={() => onNavigate("builder")}
                    style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
                >
                    Builder
                </button>

                {isRecruiterOrAdmin && (
                    <button 
                        className={currentPage === "recruiter" ? "active" : ""} 
                        onClick={() => onNavigate("recruiter")}
                        style={{ fontSize: '0.85rem', padding: '0.4rem 1rem', border: '1px dashed var(--accent)' }}
                    >
                        Recruiter Portal
                    </button>
                )}

                <button
                    className="btn-danger"
                    onClick={() => { if (onLogout) onLogout(); else { localStorage.removeItem("token"); window.location.reload(); } }}
                    style={{ marginLeft: '0.5rem', fontSize: '0.85rem', padding: '0.4rem 1rem' }}
                >
                    Logout
                </button>
            </div>
        </nav>
    );
}

export default NavBar;