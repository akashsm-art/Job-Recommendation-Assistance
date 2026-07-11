"""
TalentSpark AI — Email Service
Email notifications (placeholder — configure SMTP for production).
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
APP_NAME = os.getenv("APP_NAME", "TalentSpark AI")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")


async def send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Send an email. Falls back to console logging if SMTP is not configured.
    """
    if not SMTP_USER or not SMTP_PASSWORD or SMTP_USER == "your_email@gmail.com":
        print(f"[Email Service] SMTP not configured. Would send to {to_email}:")
        print(f"  Subject: {subject}")
        print(f"  Body: {body[:200]}...")
        return True

    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{APP_NAME} <{SMTP_USER}>"
        msg["To"] = to_email

        html_body = f"""
        <html>
        <body style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 12px 12px 0 0; text-align: center;">
                <h1 style="color: white; margin: 0; font-size: 28px;">🚀 {APP_NAME}</h1>
            </div>
            <div style="background: #ffffff; padding: 30px; border: 1px solid #e2e8f0; border-radius: 0 0 12px 12px;">
                {body}
            </div>
            <div style="text-align: center; padding: 20px; color: #718096; font-size: 12px;">
                <p>© 2024 {APP_NAME}. All rights reserved.</p>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, to_email, msg.as_string())

        return True
    except Exception as e:
        print(f"[Email Service] Failed to send email: {e}")
        return False


async def send_password_reset_email(to_email: str, reset_token: str) -> bool:
    """Send a password reset email with a token link."""
    reset_link = f"{FRONTEND_URL}/reset-password?token={reset_token}"
    body = f"""
    <h2 style="color: #1a202c;">Password Reset Request</h2>
    <p style="color: #4a5568; line-height: 1.6;">
        You requested to reset your password. Click the button below to proceed:
    </p>
    <div style="text-align: center; margin: 30px 0;">
        <a href="{reset_link}"
           style="background: linear-gradient(135deg, #667eea, #764ba2); color: white;
                  padding: 14px 32px; text-decoration: none; border-radius: 8px;
                  font-weight: 600; display: inline-block;">
            Reset Password
        </a>
    </div>
    <p style="color: #718096; font-size: 14px;">
        This link expires in 1 hour. If you didn't request this, please ignore this email.
    </p>
    """
    return await send_email(to_email, f"{APP_NAME} — Password Reset", body)


async def send_verification_email(to_email: str, verification_token: str) -> bool:
    """Send an email verification link."""
    verify_link = f"{FRONTEND_URL}/verify-email?token={verification_token}"
    body = f"""
    <h2 style="color: #1a202c;">Welcome to {APP_NAME}! 🎉</h2>
    <p style="color: #4a5568; line-height: 1.6;">
        Thank you for registering. Please verify your email to get started:
    </p>
    <div style="text-align: center; margin: 30px 0;">
        <a href="{verify_link}"
           style="background: linear-gradient(135deg, #667eea, #764ba2); color: white;
                  padding: 14px 32px; text-decoration: none; border-radius: 8px;
                  font-weight: 600; display: inline-block;">
            Verify Email
        </a>
    </div>
    """
    return await send_email(to_email, f"Welcome to {APP_NAME} — Verify Your Email", body)


async def send_application_status_email(to_email: str, job_title: str, company_name: str, status: str) -> bool:
    """Notify candidate about application status change."""
    status_colors = {
        "shortlisted": "#38a169",
        "rejected": "#e53e3e",
        "interview_scheduled": "#3182ce",
        "offered": "#805ad5",
    }
    color = status_colors.get(status, "#4a5568")
    body = f"""
    <h2 style="color: #1a202c;">Application Update</h2>
    <p style="color: #4a5568; line-height: 1.6;">
        Your application for <strong>{job_title}</strong> at <strong>{company_name}</strong>
        has been updated:
    </p>
    <div style="text-align: center; margin: 20px 0;">
        <span style="background: {color}; color: white; padding: 8px 20px; border-radius: 20px;
                     font-weight: 600; text-transform: uppercase; font-size: 14px;">
            {status.replace('_', ' ')}
        </span>
    </div>
    """
    return await send_email(to_email, f"{APP_NAME} — Application Update: {job_title}", body)
