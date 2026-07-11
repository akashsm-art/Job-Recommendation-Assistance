import type {Job} from "../types/job";
import type {Company} from "../types/company";
import {useState} from "react";

type Props = {
    jobs:Job[];
    companies:Company[];
    userRole: string;
    onEdit: (job:Job)=>void;
    onDelete: (id:number)=>void;
    onAdd: (job:Job)=>void;
}

function JobCard({
    jobs,companies,userRole,onEdit,onDelete,onAdd}:Props){
        const canManageJobs = userRole === "admin" || userRole === "recruiter";
        const [editJobId, setEditJobId] = useState<number | null>(null);
        const [addform,setAddform] = useState<Job>({
            id:0,
            title:"",
            description:"",
            salary:"",
            company_id:0,
            location:"",
            job_type:"Full-time",
            experience_level:"Mid Level",
            skills:""
        });
        const [editform,setEditform] = useState<Job>({
            id:0,
            title:"",
            description:"",
            salary:"",
            company_id:0,
            location:"",
            job_type:"Full-time",
            experience_level:"Mid Level",
            skills:""
        });
        const handleAdd = () => {
            if (!addform.title.trim() || addform.company_id === 0) return;
            onAdd(addform);
            setAddform({
                id:0,
                title:"",
                description:"",
                salary:"",
                company_id:0,
                location:"",
                job_type:"Full-time",
                experience_level:"Mid Level",
                skills:""
            })
        }
        const handleSave = () => {
            if (!editform.title.trim() || editform.company_id === 0) return;
            onEdit(editform);
            setEditJobId(null);
            setEditform({
                id:0,
                title:"",
                description:"",
                salary:"",
                company_id:0,
                location:"",
                job_type:"Full-time",
                experience_level:"Mid Level",
                skills:""
            })
        }
        const handlecancel = () => {
            setEditJobId(null);
            setEditform({
                id:0,
                title:"",
                description:"",
                salary:"",
                company_id:0,
                location:"",
                job_type:"Full-time",
                experience_level:"Mid Level",
                skills:""
            })
        }

    return(
        <div className="page-container" style={{ marginTop: '4rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
                <div style={{ padding: '0.75rem', background: 'var(--accent-bg)', borderRadius: '15px' }}>
                    <svg style={{ width: '32px', height: '32px', color: 'var(--accent)' }} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                    </svg>
                </div>
                <div>
                    <h2>Open Careers</h2>
                    <p style={{ margin: 0, opacity: 0.8 }}>Explore, create, and manage active professional job opportunities</p>
                </div>
            </div>

            <div className="grid-layout">
                {jobs.map((job) => (
                    <div key={job.id} className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                        {editJobId === job.id ? (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                                <h3 style={{ color: 'var(--accent)' }}>Edit Job Details</h3>
                                
                                <label>Job Title</label>
                                <input type="text" value={editform.title} onChange={(e)=>setEditform({...editform,title:e.target.value})} placeholder="Title" />
                                
                                <label>Job Description</label>
                                <textarea value={editform.description} onChange={(e)=>setEditform({...editform,description:e.target.value})} placeholder="Description" rows={3} style={{ resize: 'vertical' }} />
                                
                                <label>Salary (USD/Yr or range)</label>
                                <input type="text" value={editform.salary} onChange={(e)=>setEditform({...editform,salary:e.target.value})} placeholder="e.g. 120000" />
                                
                                <label>Partner Company</label>
                                <select value={editform.company_id} onChange={(e)=>setEditform({...editform,company_id:Number(e.target.value)})}>
                                    <option value={0}>Select a Company</option>
                                    {companies.map(c => (
                                        <option key={c.id} value={c.id}>{c.name}</option>
                                    ))}
                                </select>

                                <label>Location</label>
                                <input type="text" value={editform.location} onChange={(e)=>setEditform({...editform,location:e.target.value})} placeholder="e.g. Remote / Chicago, IL" />

                                <label>Job Type</label>
                                <select value={editform.job_type} onChange={(e)=>setEditform({...editform,job_type:e.target.value})}>
                                    <option value="Full-time">Full-time</option>
                                    <option value="Part-time">Part-time</option>
                                    <option value="Contract">Contract</option>
                                    <option value="Internship">Internship</option>
                                </select>

                                <label>Experience Level</label>
                                <select value={editform.experience_level} onChange={(e)=>setEditform({...editform,experience_level:e.target.value})}>
                                    <option value="Entry Level">Entry Level</option>
                                    <option value="Mid Level">Mid Level</option>
                                    <option value="Senior Level">Senior Level</option>
                                    <option value="Lead / Exec">Lead / Exec</option>
                                </select>

                                <label>Required Skills (comma-separated)</label>
                                <input type="text" value={editform.skills} onChange={(e)=>setEditform({...editform,skills:e.target.value})} placeholder="e.g. Python, SQL, REST APIs" />

                                <div className="action-buttons" style={{ marginTop: '1rem' }}>
                                    <button className="btn-primary" onClick={handleSave}>Save</button>
                                    <button onClick={handlecancel}>Cancel</button>
                                </div>
                            </div>
                        ):
                        <div style={{ display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between' }}>
                            <div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '0.5rem' }}>
                                    <h3 style={{ margin: 0 }}>{job.title}</h3>
                                    <span style={{ fontWeight: 700, color: 'var(--success)', fontSize: '0.95rem' }}>
                                        {isNaN(Number(job.salary)) ? job.salary : `$${Number(job.salary).toLocaleString()}`}
                                    </span>
                                </div>
                                <p style={{ fontWeight: 600, fontSize: '0.85rem', color: 'var(--accent)', marginBottom: '1rem' }}>
                                    🏢 {companies.find(c => c.id === job.company_id)?.name || `Company #${job.company_id}`}
                                </p>
                                
                                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '1rem' }}>
                                    {job.job_type && <span className="badge badge-primary">{job.job_type}</span>}
                                    {job.location && <span className="badge badge-success">{job.location}</span>}
                                    {job.experience_level && <span className="badge badge-warning">{job.experience_level}</span>}
                                </div>

                                <p style={{ fontSize: '0.9rem', opacity: 0.9, display: '-webkit-box', WebkitLineClamp: 3, WebkitBoxOrient: 'vertical', overflow: 'hidden', textOverflow: 'ellipsis', marginBottom: '1rem' }}>
                                    {job.description || "No description provided."}
                                </p>
                                
                                {job.skills && (
                                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.25rem', marginBottom: '1.25rem' }}>
                                        {job.skills.split(',').map((skill, index) => (
                                            <span key={index} className="badge badge-info" style={{ textTransform: 'none', fontSize: '0.7rem', padding: '0.2rem 0.5rem' }}>
                                                {skill.trim()}
                                            </span>
                                        ))}
                                    </div>
                                )}
                            </div>
                            <div>
                                <div className="action-buttons">
                                    {canManageJobs && (
                                    <button
                                        onClick={() => {
                                            setEditJobId(job.id);
                                            setEditform({
                                                id: job.id,
                                                title: job.title,
                                                description: job.description || "",
                                                salary: job.salary,
                                                company_id: job.company_id,
                                                location: job.location || "",
                                                job_type: job.job_type || "Full-time",
                                                experience_level: job.experience_level || "Mid Level",
                                                skills: job.skills || ""
                                            });
                                        }}
                                    >
                                        Edit
                                    </button>
                                    )}
                                    {canManageJobs && (
                                        <button className="btn-danger" onClick={() => onDelete(job.id)}>Delete</button>
                                    )}
                                </div>
                            </div>
                        </div>}
                    </div>
                ))}
            </div>

            {canManageJobs && (
            <div style={{ marginTop: '3.5rem', maxWidth: '600px' }}>
                <h2 style={{ fontSize: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span>➕</span> Add New Career Listing
                </h2>
                <div className="card">
                    <label>Job Title</label>
                    <input type="text" value={addform.title} onChange={(e)=>setAddform({...addform,title:e.target.value})} placeholder="e.g. Senior Software Engineer" />
                    
                    <label>Job Description</label>
                    <textarea value={addform.description} onChange={(e)=>setAddform({...addform,description:e.target.value})} placeholder="Detail the roles, responsibilities, and benefits..." rows={4} style={{ resize: 'vertical' }} />
                    
                    <label>Salary (USD/Yr)</label>
                    <input type="text" value={addform.salary} onChange={(e)=>setAddform({...addform,salary:e.target.value})} placeholder="e.g. 145000" />
                    
                    <label>Select Partner Company</label>
                    <select value={addform.company_id} onChange={(e)=>setAddform({...addform,company_id:Number(e.target.value)})}>
                        <option value={0}>-- Select Company --</option>
                        {companies.map(c => (
                            <option key={c.id} value={c.id}>{c.name}</option>
                        ))}
                    </select>

                    <label>Job Location</label>
                    <input type="text" value={addform.location} onChange={(e)=>setAddform({...addform,location:e.target.value})} placeholder="e.g. Remote, USA / Boston, MA" />

                    <label>Employment Type</label>
                    <select value={addform.job_type} onChange={(e)=>setAddform({...addform,job_type:e.target.value})}>
                        <option value="Full-time">Full-time</option>
                        <option value="Part-time">Part-time</option>
                        <option value="Contract">Contract</option>
                        <option value="Internship">Internship</option>
                    </select>

                    <label>Experience Target</label>
                    <select value={addform.experience_level} onChange={(e)=>setAddform({...addform,experience_level:e.target.value})}>
                        <option value="Entry Level">Entry Level</option>
                        <option value="Mid Level">Mid Level</option>
                        <option value="Senior Level">Senior Level</option>
                        <option value="Lead / Exec">Lead / Exec</option>
                    </select>

                    <label>Key Technologies / Skills (comma-separated)</label>
                    <input type="text" value={addform.skills} onChange={(e)=>setAddform({...addform,skills:e.target.value})} placeholder="e.g. React, Node.js, AWS, Postgres" />

                    <button className="btn-primary" onClick={handleAdd} style={{ width: '100%', marginTop: '0.5rem' }}>Create Job Opportunity</button>
                </div>
            </div>
            )}
        </div>
    )
}

export default JobCard