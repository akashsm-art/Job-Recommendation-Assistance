import api from "./api";

// --- Salary Prediction ---
export interface SalaryPredictionRequest {
    role: string;
    experience_years: number;
    skills: string[];
    location?: string;
    current_ctc?: number;
    education?: string;
    use_llm?: boolean;
}

export interface SalaryPredictionResponse {
    predicted_min_lpa: number;
    predicted_max_lpa: number;
    recommended_ctc_lpa: number;
    confidence_pct: number;
    currency: string;
    hike_percentage?: number;
    factors: string[];
    premium_skills: string[];
    market_trend: string;
    comparable_roles: string[];
    reasoning?: string;
    negotiation_tips?: string[];
    market_insight?: string;
}

export async function predictSalary(data: SalaryPredictionRequest): Promise<SalaryPredictionResponse> {
    const response = await api.post<SalaryPredictionResponse>("/ai/predict-salary", data);
    return response.data;
}

// --- Career Roadmap ---
export interface CareerRoadmapRequest {
    target_role: string;
    use_llm?: boolean;
}

export interface RoadmapPhase {
    phase: number;
    title: string;
    duration: string;
    skills: string[];
    skills_known: string[];
    skills_to_learn: string[];
    resources: string[];
    projects: string[];
    milestone: string;
    completion_pct: number;
    status: string;
    adjusted_duration?: string;
}

export interface CareerRoadmapResponse {
    title: string;
    estimated_duration: string;
    overall_readiness: number;
    skills_gap_count?: number;
    current_skills_count?: number;
    phases: RoadmapPhase[];
    tips: string[];
}

export async function getCareerRoadmap(data: CareerRoadmapRequest): Promise<CareerRoadmapResponse> {
    const response = await api.post<CareerRoadmapResponse>("/ai/career-roadmap", data);
    return response.data;
}

// --- Resume Rewriting & Cover Letters ---
export interface ResumeRewriteRequest {
    resume_text: string;
    target_role: string;
    job_description?: string;
}

export interface ResumeRewriteResponse {
    professional_summary: string;
    key_highlights: string[];
    optimized_skills: Record<string, string[]>;
    experience_bullets: string[];
    keywords_added: string[];
    ats_tips: string[];
    before_after: { before: string; after: string }[];
    overall_improvement: string;
}

export async function rewriteResume(data: ResumeRewriteRequest): Promise<ResumeRewriteResponse> {
    const response = await api.post<ResumeRewriteResponse>("/ai/rewrite-resume", data);
    return response.data;
}

export interface CoverLetterRequest {
    target_role: string;
    company_name: string;
    job_description?: string;
    tone?: string;
}

export interface CoverLetterResponse {
    cover_letter: string;
    subject_line: string;
    key_selling_points: string[];
    personalization_tips: string[];
    word_count: number;
}

export async function generateCoverLetter(data: CoverLetterRequest): Promise<CoverLetterResponse> {
    const response = await api.post<CoverLetterResponse>("/ai/generate-cover-letter", data);
    return response.data;
}

// --- Interview Prep ---
export interface InterviewPrepRequest {
    role: string;
    difficulty?: string;
    categories?: string[];
    num_questions?: number;
    company?: string;
}

export interface InterviewPrepResponse {
    role: string;
    difficulty: string;
    company?: string;
    sections: Record<string, any>;
    tips: string[];
}

export async function getInterviewPrep(data: InterviewPrepRequest): Promise<InterviewPrepResponse> {
    const response = await api.post<InterviewPrepResponse>("/ai/interview-prep", data);
    return response.data;
}

export interface MockInterviewRound {
    round: number;
    title: string;
    duration: string;
    type: string;
    questions: any[];
    scoring: Record<string, any>;
}

export interface MockInterviewResponse {
    role: string;
    difficulty: string;
    total_rounds: number;
    estimated_duration: string;
    rounds: MockInterviewRound[];
}

export async function getMockInterview(role: string, difficulty: string = "Medium", rounds: number = 3): Promise<MockInterviewResponse> {
    const response = await api.get<MockInterviewResponse>("/ai/mock-interview", {
        params: { role, difficulty, rounds }
    });
    return response.data;
}

export interface InterviewAnswerEvaluationRequest {
    question: string;
    answer: string;
    role: string;
}

export interface InterviewAnswerEvaluationResponse {
    score: number;
    max_score: number;
    feedback: string;
    strengths: string[];
    improvements: string[];
    ideal_answer_outline: string;
    communication_score: number;
    technical_score: number;
    confidence_score: number;
}

export async function evaluateInterviewAnswer(data: InterviewAnswerEvaluationRequest): Promise<InterviewAnswerEvaluationResponse> {
    const response = await api.post<InterviewAnswerEvaluationResponse>("/ai/evaluate-answer", data);
    return response.data;
}

// --- Company Fit ---
export interface CompanyFitRequest {
    company_id: number;
    use_llm?: boolean;
}

export interface CompanyFitResponse {
    scores: Record<string, number>;
    recommendation: string;
    matching_tech: string[];
    missing_tech: string[];
    insights: string[];
    overall_fit_pct?: number;
    dimensions?: Record<string, any>;
    pros?: string[];
    cons?: string[];
    questions_to_ask?: string[];
}

export async function getCompanyFit(data: CompanyFitRequest): Promise<CompanyFitResponse> {
    const response = await api.post<CompanyFitResponse>("/ai/company-fit", data);
    return response.data;
}

// --- Skill Trends ---
export interface SkillTrendResponse {
    skills?: Record<string, { demand: string; trend: string; growth_pct: number; avg_salary_boost_pct?: number; category?: string }>;
    categories?: Record<string, any[]>;
    updated: string;
}

export async function getSkillTrends(skills?: string[]): Promise<SkillTrendResponse> {
    const response = await api.post<SkillTrendResponse>("/ai/skill-trends", { skills });
    return response.data;
}

export interface JobMarketOverviewResponse {
    trends: Record<string, any>;
    top_growing_skills: any[];
    hot_roles: any[];
    insights: string[];
    updated: string;
}

export async function getJobMarketOverview(): Promise<JobMarketOverviewResponse> {
    const response = await api.get<JobMarketOverviewResponse>("/ai/market-overview");
    return response.data;
}

export interface UserSkillValueAnalysisResponse {
    trending_skills: any[];
    stable_skills: any[];
    declining_skills: any[];
    untracked_skills: string[];
    estimated_salary_boost_pct: number;
    market_readiness: Record<string, any>;
    recommendations: string[];
}

export async function getSkillValueAnalysis(): Promise<UserSkillValueAnalysisResponse> {
    const response = await api.get<UserSkillValueAnalysisResponse>("/ai/skill-value-analysis");
    return response.data;
}

// --- Resume Builder ---
export interface ResumeBuildResponse {
    template: { name: string; description: string; style: string };
    generated_at: string;
    sections: Record<string, any>;
}

export async function buildResume(template: string = "modern", targetRole?: string): Promise<ResumeBuildResponse> {
    const response = await api.post<ResumeBuildResponse>("/ai/build-resume", { template, target_role: targetRole });
    return response.data;
}

export async function buildResumeHtml(template: string = "modern", targetRole?: string): Promise<string> {
    const response = await api.post<{ html: string }>("/ai/build-resume/html", { template, target_role: targetRole });
    return response.data.html;
}

// --- Recruiter AI ---
export interface CandidateRankInfo {
    user_id: number;
    name: string;
    email: string;
    match_score: number;
    technical_match: number;
    experience_match: number;
    education_match: number;
    matching_skills: string[];
    missing_skills: string[];
    rank_reason: string;
    rank: number;
    tier: string;
}

export async function rankCandidates(jobId: number): Promise<CandidateRankInfo[]> {
    const response = await api.post<{ ranked_candidates: CandidateRankInfo[] }>("/ai/rank-candidates", { job_id: jobId });
    return response.data.ranked_candidates;
}

export interface DuplicateDetectionResponse {
    similarity_score: number;
    cosine_similarity: number;
    text_overlap_pct: number;
    is_duplicate: boolean;
    verdict: string;
}

export async function detectDuplicates(resumeText1: string, resumeText2: string): Promise<DuplicateDetectionResponse> {
    const response = await api.post<DuplicateDetectionResponse>("/ai/detect-duplicates", {
        resume_text_1: resumeText1,
        resume_text_2: resumeText2,
    });
    return response.data;
}

export interface ResumeAuthenticityResponse {
    authenticity_score: number;
    verdict: string;
    flags: string[];
    word_count: number;
    has_contact_info: boolean;
    has_verifiable_links: boolean;
    recommendations: string[];
}

export async function scanAuthenticity(resumeText: string): Promise<ResumeAuthenticityResponse> {
    const response = await api.post<ResumeAuthenticityResponse>("/ai/resume-authenticity", {
        resume_text: resumeText
    });
    return response.data;
}

export interface RecruiterPoolSummaryResponse {
    summary: string;
    stats: Record<string, any>;
    top_skills_in_pool: any[];
    recommendation: string;
}

export async function getPoolSummary(jobId: number): Promise<RecruiterPoolSummaryResponse> {
    const response = await api.get<RecruiterPoolSummaryResponse>(`/ai/pool-summary/${jobId}`);
    return response.data;
}

// --- Dashboard Stats ---
export async function getDashboardStats(): Promise<Record<string, any>> {
    const response = await api.get<Record<string, any>>("/rag/dashboard-stats");
    return response.data;
}
