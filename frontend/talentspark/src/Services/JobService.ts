import api from "./api"
import type { Job } from "../types/job"

export async function getJobs(): Promise<Job[]> {
    const response = await api.get("/job/")
    return response.data
}

export async function getMyJobs(): Promise<Job[]> {
    const response = await api.get("/job/my-jobs")
    return response.data
}

export async function getJob(id: number): Promise<Job> {
    const response = await api.get(`/job/${id}`)
    return response.data
}

export async function createJob(job: Job): Promise<Job> {
    const response = await api.post("/job/", job)
    return response.data
}

export async function updateJob(id: number, job: Job): Promise<Job> {
    const response = await api.put(`/job/${id}`, job)
    return response.data
}

export async function deleteJob(id: number): Promise<void> {
    const response = await api.delete(`/job/${id}`)
    return response.data
}

// --- Applications ---

export interface ApplicationData {
    id: number;
    user_id: number;
    job_id: number;
    status: string;
    cover_letter?: string;
    match_score?: number;
    match_details?: string;
    applied_at?: string;
    updated_at?: string;
}

export async function applyToJob(jobId: number, coverLetter?: string): Promise<ApplicationData> {
    const response = await api.post("/job/apply", {
        job_id: jobId,
        cover_letter: coverLetter || null,
    })
    return response.data
}

export async function getMyApplications(): Promise<ApplicationData[]> {
    const response = await api.get("/job/applications/my")
    return response.data
}

export async function getJobApplicants(jobId: number): Promise<ApplicationData[]> {
    const response = await api.get(`/job/${jobId}/applicants`)
    return response.data
}

export async function updateApplicationStatus(appId: number, status: string): Promise<ApplicationData> {
    const response = await api.put(`/job/applications/${appId}/status`, { status })
    return response.data
}

// --- Notifications ---

export interface NotificationData {
    id: number;
    type: string;
    title: string;
    message: string;
    is_read: boolean;
    created_at?: string;
}

export async function getNotifications(): Promise<NotificationData[]> {
    const response = await api.get("/job/notifications")
    return response.data
}

export async function getUnreadNotificationCount(): Promise<number> {
    const response = await api.get("/job/notifications/unread-count")
    return response.data.count
}

export async function markNotificationRead(id: number): Promise<void> {
    await api.put(`/job/notifications/${id}/read`)
}

export async function markAllNotificationsRead(): Promise<void> {
    await api.put("/job/notifications/read-all")
}

// --- Admin ---

export interface AdminStats {
    total_users: number;
    total_candidates: number;
    total_recruiters: number;
    total_companies: number;
    total_jobs: number;
    active_jobs: number;
    total_applications: number;
}

export async function getAdminStats(): Promise<AdminStats> {
    const response = await api.get("/rag/admin-stats")
    return response.data
}

// --- Profile ---

export async function getProfile(): Promise<any> {
    const response = await api.get("/auth/me")
    return response.data
}

export async function updateProfile(data: any): Promise<any> {
    const response = await api.put("/auth/profile", data)
    return response.data
}