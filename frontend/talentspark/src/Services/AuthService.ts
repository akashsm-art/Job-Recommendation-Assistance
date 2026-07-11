import type {LoginRequest,LoginResponse,RegisterRequest,RegisterResponse} from "../types/user";
import api from "./api";

export const login = async (credentials:LoginRequest):Promise<LoginResponse>=>{
    // Backend expects OAuth2PasswordRequestForm (form-encoded with "username" field)
    const formData = new URLSearchParams();
    formData.append("username", credentials.email);
    formData.append("password", credentials.password);

    const response = await api.post<LoginResponse>(`/auth/login`, formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
    });
    return response.data;
}

export const register = async (user:RegisterRequest):Promise<RegisterResponse>=>{
    const payload = {
        full_name: user.name,
        email: user.email,
        password: user.password,
        role: user.role
    };
    const response = await api.post<RegisterResponse>(`/auth/register`, payload);
    return response.data;
}
