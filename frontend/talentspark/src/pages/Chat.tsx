import { useState, useRef, useEffect } from "react";
import { askCareerChat } from "../Services/ChatService";
import type { ChatMessage } from "../types/chat";

function Chat() {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [sessionId] = useState(() => "session_" + Date.now());
    const chatEndRef = useRef<HTMLDivElement | null>(null);

    const scrollToBottom = () => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, loading]);

    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage: ChatMessage = { role: "user", content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput("");
        setLoading(true);

        try {
            const response = await askCareerChat(input, sessionId);
            const botMessage: ChatMessage = { role: "bot", content: response };
            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            console.error("Chat error:", error);
            const errorMessage: ChatMessage = { role: "bot", content: "Error: Could not retrieve a response. Please check your Groq API key." };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
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
                    <h2>AI Career Coach</h2>
                    <p style={{ margin: 0, opacity: 0.8 }}>Get expert guidance on tech stack trends, interview prep, and career path decisions</p>
                </div>
            </div>

            <div className="chat-window">
                {/* Chat Top Info Bar */}
                <div style={{ padding: '1rem 1.5rem', background: 'var(--glass)', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <div style={{ width: '10px', height: '10px', background: '#10b981', borderRadius: '50%', boxShadow: '0 0 8px #10b981' }}></div>
                    <span style={{ fontWeight: 700, fontSize: '0.9rem', color: 'var(--text-h)' }}>Llama-3.3 Assistant</span>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text)', opacity: 0.7, marginLeft: 'auto' }}>Active Session</span>
                </div>

                {/* Messages Box */}
                <div className="chat-history">
                    {messages.length === 0 && (
                        <div style={{ margin: 'auto', color: 'var(--text)', textAlign: 'center', padding: '2rem', maxWidth: '400px' }}>
                            <span style={{ fontSize: '3rem', display: 'block', marginBottom: '1rem' }}>🤖</span>
                            <h3 style={{ marginBottom: '0.5rem' }}>Welcome to Jobcart!</h3>
                            <p style={{ fontSize: '0.9rem', opacity: 0.8 }}>
                                Ask me anything! For example:
                                <br />
                                <em>"What skills are needed for a junior frontend role?"</em> or 
                                <br />
                                <em>"Can you write a template resume cover letter?"</em>
                            </p>
                        </div>
                    )}
                    {messages.map((msg, i) => (
                        <div key={i} className={`chat-message ${msg.role === "user" ? "chat-user" : "chat-bot"}`}>
                            <strong style={{ display: 'block', marginBottom: '0.35rem', opacity: 0.8, fontSize: '0.85rem' }}>
                                {msg.role === "user" ? "You" : "Jobcart"}
                            </strong>
                            <p style={{ margin: 0, fontSize: '0.95rem', whiteSpace: 'pre-wrap' }}>{msg.content}</p>
                        </div>
                    ))}
                    {loading && (
                        <div className="chat-message chat-bot">
                            <strong style={{ display: 'block', marginBottom: '0.35rem', opacity: 0.8, fontSize: '0.85rem' }}>Jobcart</strong>
                            <div className="typing-indicator">
                                <div className="typing-dot"></div>
                                <div className="typing-dot"></div>
                                <div className="typing-dot"></div>
                            </div>
                        </div>
                    )}
                    <div ref={chatEndRef}></div>
                </div>

                {/* Chat Send Form */}
                <form onSubmit={handleSend} style={{ margin: 0, maxWidth: '100%', padding: '1.25rem', borderTop: '1px solid var(--border)', display: 'flex', gap: '1rem', boxShadow: 'none', background: 'var(--glass)' }}>
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type your question here..."
                        style={{ marginBottom: 0, flex: 1, borderRadius: '100px' }}
                        disabled={loading}
                    />
                    <button type="submit" className="btn-primary" style={{ borderRadius: '100px', padding: '0.6rem 1.5rem' }} disabled={loading || !input.trim()}>
                        <span>Send</span>
                        <svg style={{ width: '16px', height: '16px' }} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
                        </svg>
                    </button>
                </form>
            </div>
        </div>
    );
}

export default Chat;
