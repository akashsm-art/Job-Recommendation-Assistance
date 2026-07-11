import NavBar from "./components/NavBar";
import CompanyCard from "./components/CompanyCard";
import JobCard from "./components/JobCard";
import Footer from "./components/Footer";
import { useEffect, useState } from "react";
import { getCompanies, updateCompany, deleteCompany, createCompany } from "./Services/CompanyService";
import { getJobs, updateJob, deleteJob, createJob } from "./Services/JobService";
import type { Company } from "./types/company"
import type { Job } from "./types/job"
import Login from "./pages/Login";
import Register from "./pages/Register";
import Chat from "./pages/Chat";
import ResumeAnalyser from "./pages/ResumeAnalyser";
import JobMatch from "./pages/JobMatch";

// Phase 2/3 newly added pages
import Dashboard from "./pages/Dashboard";
import SalaryPredictor from "./pages/SalaryPredictor";
import CareerRoadmap from "./pages/CareerRoadmap";
import RecruiterPortal from "./pages/RecruiterPortal";
import LearningDashboard from "./pages/LearningDashboard";
import InterviewPrep from "./pages/InterviewPrep";
import Profile from "./pages/Profile";
import Applications from "./pages/Applications";

/** Decode a JWT payload without any library */
function decodeJwtRole(token: string): string {
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.role ?? "candidate";
  } catch {
    return "candidate";
  }
}

function App() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null)
  const [companies, setCompanies] = useState<Company[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));
  const [userRole, setUserRole] = useState<string>(() => {
    const t = localStorage.getItem("token");
    return t ? decodeJwtRole(t) : "candidate";
  });
  const [page, setPage] = useState<"login" | "register">("login");
  const [currentPage, setCurrentPage] = useState("dashboard");

  const handleLogin = (newToken: string) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
    setUserRole(decodeJwtRole(newToken));
    setCurrentPage("dashboard");
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
    setUserRole("candidate");
  };

  async function fetchData() {
    setLoading(true);
    try {
      const [companiesResult, jobsResult] = await Promise.allSettled([
        getCompanies(),
        getJobs()
      ]);
      if (companiesResult.status === "fulfilled") {
        setCompanies(companiesResult.value);
      } else {
        console.warn("Failed to load companies:", companiesResult.reason);
      }
      if (jobsResult.status === "fulfilled") {
        setJobs(jobsResult.value);
      } else {
        console.warn("Failed to load jobs:", jobsResult.reason);
      }
    } catch (error) {
      console.error("Unexpected error in fetchData:", error);
    } finally {
      setLoading(false);
    }
  }

  async function handleEdit(company: Company) {
    try {
      const updatedCompany = await updateCompany(company.id, company);
      setCompanies(prev =>
        prev.map(company =>
          company.id === updatedCompany.id ? updatedCompany : company
        )
      );
    } catch (error) {
      setError(error as Error);
    }
  }

  async function handleDelete(id: number) {
    try {
      await deleteCompany(id);
      setCompanies(prev =>
        prev.filter(company => company.id !== id)
      );
    } catch (error) {
      setError(error as Error);
    }
  }

  async function handleAdd(company: Company) {
    try {
      const newCompany = await createCompany(company);
      setCompanies(prev => [...prev, newCompany]);
    } catch (error) {
      setError(error as Error);
    }
  }

  async function handleJobEdit(job: Job) {
    try {
      const updatedJob = await updateJob(job.id, job);
      setJobs(prev =>
        prev.map(j =>
          j.id === updatedJob.id ? updatedJob : j
        )
      );
    } catch (error) {
      setError(error as Error);
    }
  }

  async function handleJobDelete(id: number) {
    try {
      await deleteJob(id);
      setJobs(prev =>
        prev.filter(job => job.id !== id)
      );
    } catch (error) {
      setError(error as Error);
    }
  }

  async function handleJobAdd(job: Job) {
    try {
      const newJob = await createJob(job);
      setJobs(prev => [...prev, newJob]);
    } catch (error) {
      setError(error as Error);
    }
  }


  useEffect(() => {
    if (token) {
      fetchData();
    }
  }, [token]);

  if (!token) {
    return (
      <>
        {page === "login" ? (
          <Login onLogin={handleLogin} onSwitchToRegister={() => setPage("register")} />
        ) : (
          <Register onSwitchToLogin={() => setPage("login")} />
        )}
      </>
    )
  }

  if (loading) {
    return <div className="auth-container"><div className="auth-card"><p style={{textAlign:'center',opacity:0.7}}>Loading…</p></div></div>;
  }

  if (error) {
    const errorMsg = (error as any)?.response?.data?.detail || error.message || "Something went wrong";
    return (
      <div className="auth-container">
        <div className="auth-card" style={{textAlign:'center'}}>
          <div style={{fontSize:'2.5rem',marginBottom:'0.5rem'}}>⚠️</div>
          <h2 style={{margin:'0 0 0.5rem',color:'#ff6b6b'}}>Connection Error</h2>
          <p style={{opacity:0.7,marginBottom:'1.5rem'}}>{errorMsg}</p>
          <p style={{opacity:0.5,fontSize:'0.85rem',marginBottom:'1.5rem'}}>
            Make sure the backend server is running at the correct address.
          </p>
          <button className="btn-primary" onClick={() => { setError(null); fetchData(); }}>
            🔄 Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <>
      <NavBar currentPage={currentPage} onNavigate={setCurrentPage} onLogout={handleLogout} userRole={userRole} />
      
      {currentPage === "dashboard" && (
        <Dashboard userRole={userRole} onNavigate={setCurrentPage} />
      )}
      
      {currentPage === "home" && (
        <>
          <CompanyCard
            companies={companies}
            jobs={jobs}
            userRole={userRole}
            onEdit={handleEdit}
            onDelete={handleDelete}
            onAdd={handleAdd}
          />
          <JobCard
            jobs={jobs}
            companies={companies}
            userRole={userRole}
            onEdit={handleJobEdit}
            onDelete={handleJobDelete}
            onAdd={handleJobAdd}
          />
        </>
      )}
      
      {currentPage === "chat" && <Chat />}
      {currentPage === "resume" && <ResumeAnalyser />}
      {currentPage === "jobmatch" && <JobMatch />}
      
      {currentPage === "salary" && <SalaryPredictor />}
      {currentPage === "roadmap" && <CareerRoadmap />}
      {currentPage === "prep" && <InterviewPrep />}
      {currentPage === "learning" && <LearningDashboard />}
      {currentPage === "recruiter" && <RecruiterPortal />}
      {currentPage === "profile" && <Profile />}
      {currentPage === "applications" && <Applications />}
      
      <Footer />
    </>
  )
}

export default App