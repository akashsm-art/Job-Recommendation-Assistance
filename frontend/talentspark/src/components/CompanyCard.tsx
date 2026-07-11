import type {Company} from "../types/company";
import type {Job} from "../types/job";
import {useState} from "react";

type Props = {
    companies:Company[];
    jobs:Job[];
    userRole: string;
    onEdit: (company:Company)=>void;
    onDelete: (id:number)=>void;
    onAdd: (company:Company)=>void;
}


function CompanyCard({
    companies,jobs,userRole,onAdd,onEdit,onDelete}:Props){
    const isAdmin = userRole === "admin";
    const [editCompanyId, setEditCompanyId] = useState<number | null>(null);
    const [addform,setAddform] = useState<Company>({
        id:0,
        name:"",
        email:"",
        phone:"",
        location:"",
        jobs:[]
    });
    const [editform,setEditform] = useState<Company>({
        id:0,
        name:"",
        email:"",
        phone:"",
        location:"",
        jobs:[]
    });
    const handleAdd = () => {
        if (!addform.name.trim()) return;
        onAdd(addform);
        setAddform({
            id:0,
            name:"",
            email:"",
            phone:"",
            location:"",
            jobs:[]
        })
    }
    const handleSave = () => {
        if (!editform.name.trim()) return;
        onEdit(editform);
        setEditCompanyId(null);
        setEditform({
            id:0,
            name:"",
            email:"",
            phone:"",
            location:"",
            jobs:[]
        })
    } 
    const handlecancel = () => {
        setEditCompanyId(null);
        setEditform({
            id:0,
            name:"",
            email:"",
            phone:"",
            location:"",
            jobs:[]
        })
    } 

    return(
        <div className="page-container">
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '2rem' }}>
                <div style={{ padding: '0.75rem', background: 'var(--accent-bg)', borderRadius: '15px' }}>
                    <svg style={{ width: '32px', height: '32px', color: 'var(--accent)' }} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                    </svg>
                </div>
                <div>
                    <h2>Partner Companies</h2>
                    <p style={{ margin: 0, opacity: 0.8 }}>Manage all registered enterprise partners and recruitment entities</p>
                </div>
            </div>

            <div className="grid-layout">
                {companies.map((company) => (
                    <div key={company.id} className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                        {editCompanyId === company.id ? (
                            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                                <h3 style={{ color: 'var(--accent)' }}>Edit Company Details</h3>
                                <label>Company Name</label>
                                <input type="text" value={editform.name} onChange={(e)=>setEditform({...editform,name:e.target.value})} placeholder="Company Name" />
                                
                                <label>Email Address</label>
                                <input type="text" value={editform.email} onChange={(e)=>setEditform({...editform,email:e.target.value})} placeholder="Email" />
                                
                                <label>Phone Number</label>
                                <input type="text" value={editform.phone} onChange={(e)=>setEditform({...editform,phone:e.target.value})} placeholder="Phone" />
                                
                                <label>Location</label>
                                <input type="text" value={editform.location} onChange={(e)=>setEditform({...editform,location:e.target.value})} placeholder="Location" />
                                
                                <div className="action-buttons" style={{ marginTop: '1rem' }}>
                                    <button className="btn-primary" onClick={handleSave}>Save Changes</button>
                                    <button onClick={handlecancel}>Cancel</button>
                                </div>
                            </div>
                        ):
                        <div style={{ display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between' }}>
                            <div>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '0.75rem' }}>
                                    <h3 style={{ margin: 0 }}>{company.name}</h3>
                                    <span className="badge badge-info">{company.location || 'Unknown'}</span>
                                </div>
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', margin: '1rem 0' }}>
                                    <p style={{ margin: 0, fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        <strong>✉</strong> {company.email || 'No email registered'}
                                    </p>
                                    <p style={{ margin: 0, fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                        <strong>📞</strong> {company.phone || 'No phone registered'}
                                    </p>
                                </div>
                            </div>
                            <div>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.25rem', padding: '0.5rem', background: 'var(--accent-bg)', borderRadius: '10px' }}>
                                    <span style={{ fontSize: '1.1rem' }}>💼</span>
                                    <span style={{ fontWeight: 600, fontSize: '0.85rem', color: 'var(--accent)' }}>
                                        {jobs.filter(j => j.company_id === company.id).length} Active Opening{jobs.filter(j => j.company_id === company.id).length === 1 ? '' : 's'}
                                    </span>
                                </div>
                                <div className="action-buttons">
                                    {isAdmin && (
                                        <button
                                            onClick={() => {
                                                setEditCompanyId(company.id);
                                                setEditform({
                                                    id: company.id,
                                                    name: company.name,
                                                    email: company.email,
                                                    phone: company.phone,
                                                    location: company.location,
                                                    jobs: company.jobs,
                                                });
                                            }}
                                        >
                                            Edit
                                        </button>
                                    )}
                                    {isAdmin && (
                                        <button className="btn-danger" onClick={() => onDelete(company.id)}>Delete</button>
                                    )}
                                </div>
                            </div>
                        </div>}
                    </div>
                ))}
            </div>

            {isAdmin && (
            <div style={{ marginTop: '3.5rem', maxWidth: '600px' }}>
                <h2 style={{ fontSize: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span>➕</span> Add New Partner Company
                </h2>
                <div className="card">
                    <label>Company Name</label>
                    <input type="text" value={addform.name} onChange={(e)=>setAddform({...addform,name:e.target.value})} placeholder="e.g. Acme Corporation" />
                    
                    <label>Contact Email</label>
                    <input type="text" value={addform.email} onChange={(e)=>setAddform({...addform,email:e.target.value})} placeholder="e.g. contact@acme.com" />
                    
                    <label>Contact Phone</label>
                    <input type="text" value={addform.phone} onChange={(e)=>setAddform({...addform,phone:e.target.value})} placeholder="e.g. +1 (555) 019-2834" />
                    
                    <label>Headquarters Location</label>
                    <input type="text" value={addform.location} onChange={(e)=>setAddform({...addform,location:e.target.value})} placeholder="e.g. San Francisco, CA" />
                    
                    <button className="btn-primary" onClick={handleAdd} style={{ width: '100%', marginTop: '0.5rem' }}>Add Company Partner</button>
                </div>
            </div>
            )}
        </div>
    )
}

export default CompanyCard