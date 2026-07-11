import api from "./api";


export async function askChat(query: string): Promise<string> {
    const response = await api.post<{ query: string; response: string }>("/chat/", { query });
    return response.data.response;
}

export async function askCareerChat(query: string, session_id: string): Promise<string> {
    const response = await api.post<{ query: string; response: string; session_id: string }>("/chat/career-coach", {
        query,
        session_id
    });
    return response.data.response;
}
