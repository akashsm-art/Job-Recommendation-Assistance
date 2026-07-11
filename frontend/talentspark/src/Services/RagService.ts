import api from "./api";
import type {
    ResumeAnalysis,
    RagAnswer,
    EmbedResult,
    JobMatchResponse,
    SemanticSearchResponse
} from "../types/rag";

export async function embedJobs(): Promise<EmbedResult> {
    const response = await api.post<EmbedResult>("/rag/embed-jobs");
    return response.data;
}

export async function semanticSearch(question: string): Promise<SemanticSearchResponse> {
    const response = await api.post<SemanticSearchResponse>("/rag/search", { question });
    return response.data;
}

export async function ragAsk(question: string): Promise<RagAnswer> {
    const response = await api.post<RagAnswer>("/rag/search", { question });
    return response.data;
}

export async function analyseResume(resume_text: string, job_description?: string): Promise<ResumeAnalysis> {
    const response = await api.post<{ analysis: any }>("/rag/analyze-resume", {
        resume_text,
        job_description
    });
    // In our backend analyze-resume returns {"analysis": {...}}
    // Let's stringify it beautifully or parse it directly
    const analysisStr = typeof response.data.analysis === 'string' 
        ? response.data.analysis 
        : JSON.stringify(response.data.analysis, null, 2);
    return { analysis: analysisStr };
}

export async function matchJobs(skills: string, experience: string): Promise<JobMatchResponse> {
    // Falls back to search-similar-jobs query on backend
    const response = await api.post<SemanticSearchResponse>("/rag/search", { question: `Skills: ${skills}. Experience: ${experience}` });
    const matches = (response.data.results || []).map(r => ({
        job_id: r.job_id,
        title: r.title,
        description: r.description,
        salary: r.salary,
        match_score: r.score * 100
    }));
    return { matches };
}
