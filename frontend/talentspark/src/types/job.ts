interface Job {
    id: number;
    title: string;
    description: string;
    salary: string;
    company_id: number;
    location?: string;
    job_type?: string;
    experience_level?: string;
    skills?: string;
}
export type { Job }