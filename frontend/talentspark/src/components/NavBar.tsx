import { useState, useEffect, useRef } from "react";
import { getNotifications, markNotificationRead, markAllNotificationsRead, type NotificationData } from "../Services/JobService";

type Props = {
    currentPage: string;
    onNavigate: (page: string) => void;
    onLogout?: () => void;
    userRole: string;
}

function NavBar({ currentPage, onNavigate, onLogout, userRole }: Props) {
    const isCandidate = userRole === "candidate";
    const isRecruiter = userRole === "recruiter";
    const isAdmin = userRole === "admin";

    const [notifications, setNotifications] = useState<NotificationData[]>([]);
    const [showNotifDropdown, setShowNotifDropdown] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);

    // Fetch notifications
    const fetchNotifications = async () => {
        try {
            const data = await getNotifications();
            setNotifications(data);
        } catch (err) {
            console.error("Failed to fetch notifications:", err);
        }
    };

    useEffect(() => {
        fetchNotifications();
        // Poll notifications every 8 seconds
        const timer = setInterval(fetchNotifications, 8000);
        return () => clearInterval(timer);
    }, []);

    // Close dropdown on click outside
    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setShowNotifDropdown(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    const unreadCount = notifications.filter(n => !n.is_read).length;

    const handleMarkRead = async (id: number) => {
        try {
            await markNotificationRead(id);
            setNotifications(prev => prev.map(n => n.id === id ? { ...n, is_read: true } : n));
        } catch (err) {
            console.error("Failed to mark notification as read:", err);
        }
    };

    const handleMarkAllRead = async () => {
        try {
            await markAllNotificationsRead();
            setNotifications(prev => prev.map(n => ({ ...n, is_read: true })));
        } catch (err) {
            console.error("Failed to mark all as read:", err);
        }
    };

    return (
        <nav style={{ 
            flexWrap: 'wrap', 
            gap: '0.5rem', 
            borderRadius: '15px', 
            padding: '0.75rem 1.5rem',
            position: 'relative'
        }}>
            <div className="nav-brand" style={{ cursor: 'pointer' }} onClick={() => onNavigate("dashboard")}>
                🛒 Jobcart
            </div>
            
            <div className="nav-links" style={{ flexWrap: 'wrap', gap: '0.35rem', alignItems: 'center' }}>
                {/* Dashboard: All Roles */}
                <button 
                    className={currentPage === "dashboard" ? "active" : ""} 
                    onClick={() => onNavigate("dashboard")}
                    style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
                >
                    Dashboard
                </button>

                {/* Jobs: All Roles */}
                <button 
                    className={currentPage === "home" ? "active" : ""} 
                    onClick={() => onNavigate("home")}
                    style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
                >
                    Jobs
                </button>

                {/* AI Coach: Candidate and Admin */}
                {(isCandidate || isAdmin) && (
                    <button 
                        className={currentPage === "chat" ? "active" : ""} 
                        onClick={() => onNavigate("chat")}
                        style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
                    >
                        AI Coach
                    </button>
                )}

                {/* Analyser: Candidate and Admin */}
                {(isCandidate || isAdmin) && (
                    <button 
                        className={currentPage === "resume" ? "active" : ""} 
                        onClick={() => onNavigate("resume")}
                        style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
                    >
                        Analyser
                    </button>
                )}

                {/* Profile: Candidate */}
                {isCandidate && (
                    <button 
                        className={currentPage === "profile" ? "active" : ""} 
                        onClick={() => onNavigate("profile")}
                        style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
                    >
                        Profile
                    </button>
                )}

                {/* Applications: Candidate */}
                {isCandidate && (
                    <button 
                        className={currentPage === "applications" ? "active" : ""} 
                        onClick={() => onNavigate("applications")}
                        style={{ fontSize: '0.85rem', padding: '0.4rem 1rem' }}
                    >
                        Applications
                    </button>
                )}

                {/* Recruiter Portal: Recruiter and Admin */}
                {(isRecruiter || isAdmin) && (
                    <button 
                        className={currentPage === "recruiter" ? "active" : ""} 
                        onClick={() => onNavigate("recruiter")}
                        style={{ fontSize: '0.85rem', padding: '0.4rem 1rem', border: '1px dashed var(--accent)' }}
                    >
                        Recruiter Portal
                    </button>
                )}

                {/* Notifications Bell */}
                <div style={{ position: 'relative' }} ref={dropdownRef}>
                    <button
                        onClick={() => setShowNotifDropdown(!showNotifDropdown)}
                        style={{
                            background: 'transparent',
                            border: 'none',
                            fontSize: '1.25rem',
                            cursor: 'pointer',
                            padding: '0.25rem 0.5rem',
                            display: 'flex',
                            alignItems: 'center',
                            position: 'relative',
                        }}
                        title="Notifications"
                    >
                        <span className={unreadCount > 0 ? "shake-bell" : ""}>🔔</span>
                        {unreadCount > 0 && (
                            <span style={{
                                position: 'absolute',
                                top: '-3px',
                                right: '-3px',
                                background: '#ff4757',
                                color: '#fff',
                                fontSize: '0.65rem',
                                fontWeight: 'bold',
                                borderRadius: '50%',
                                minWidth: '16px',
                                height: '16px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                padding: '0 4px',
                            }}>
                                {unreadCount}
                            </span>
                        )}
                    </button>

                    {/* Notifications Dropdown */}
                    {showNotifDropdown && (
                        <div style={{
                            position: 'absolute',
                            right: 0,
                            top: '100%',
                            marginTop: '0.5rem',
                            width: '320px',
                            background: 'var(--card-bg)',
                            border: '1px solid var(--border)',
                            borderRadius: '12px',
                            boxShadow: '0 10px 25px rgba(0, 0, 0, 0.3)',
                            zIndex: 1000,
                            maxHeight: '400px',
                            overflowY: 'auto',
                        }}>
                            <div style={{
                                display: 'flex',
                                justifyContent: 'space-between',
                                alignItems: 'center',
                                padding: '0.75rem 1rem',
                                borderBottom: '1px solid var(--border)'
                            }}>
                                <span style={{ fontWeight: 600, fontSize: '0.9rem' }}>Notifications</span>
                                {unreadCount > 0 && (
                                    <button 
                                        onClick={handleMarkAllRead}
                                        style={{
                                            background: 'transparent',
                                            border: 'none',
                                            color: 'var(--accent)',
                                            fontSize: '0.75rem',
                                            cursor: 'pointer',
                                            fontWeight: 600,
                                        }}
                                    >
                                        Mark all as read
                                    </button>
                                )}
                            </div>

                            <div style={{ display: 'flex', flexDirection: 'column' }}>
                                {notifications.length === 0 ? (
                                    <div style={{ padding: '2rem', textAlign: 'center', opacity: 0.5, fontSize: '0.85rem' }}>
                                        No notifications yet
                                    </div>
                                ) : (
                                    notifications.map(n => (
                                        <div 
                                            key={n.id} 
                                            onClick={() => !n.is_read && handleMarkRead(n.id)}
                                            style={{
                                                padding: '0.75rem 1rem',
                                                borderBottom: '1px solid rgba(255,255,255,0.04)',
                                                background: n.is_read ? 'transparent' : 'rgba(124, 58, 237, 0.05)',
                                                cursor: n.is_read ? 'default' : 'pointer',
                                                transition: 'background 0.2s',
                                            }}
                                        >
                                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.2rem' }}>
                                                <span style={{ 
                                                    fontWeight: n.is_read ? 500 : 700, 
                                                    fontSize: '0.85rem',
                                                    color: n.is_read ? 'var(--text-h)' : 'var(--accent)'
                                                }}>
                                                    {n.title}
                                                </span>
                                                {!n.is_read && (
                                                    <span style={{
                                                        width: '8px',
                                                        height: '8px',
                                                        borderRadius: '50%',
                                                        background: 'var(--accent)',
                                                        alignSelf: 'center'
                                                    }} />
                                                )}
                                            </div>
                                            <p style={{ margin: 0, fontSize: '0.8rem', opacity: 0.8, lineHeight: 1.3 }}>
                                                {n.message}
                                            </p>
                                        </div>
                                    ))
                                )}
                            </div>
                        </div>
                    )}
                </div>

                {/* Logout Button */}
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