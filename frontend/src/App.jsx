import React, { useEffect, useState } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid
} from 'recharts'

const API = 'http://localhost:8080/api'

const initialForm = {
  name: '',
  cgpa: 8,
  aptitudeScore: 70,
  codingScore: 70,
  communicationScore: 70,
  projects: 2,
  internships: 1,
  certifications: 2,
  attendance: 85,
  backlogs: 0,
  placementStatus: true
}

export default function App() {
  const [form, setForm] = useState(initialForm)
  const [overview, setOverview] = useState(null)
  const [correlations, setCorrelations] = useState(null)
  const [probabilities, setProbabilities] = useState(null)
  const [hypothesis, setHypothesis] = useState(null)
  const [prediction, setPrediction] = useState(null)
  const [message, setMessage] = useState('')

  const load = async () => {
    try {
      const [o, c, p, h] = await Promise.all([
        fetch(`${API}/analytics/overview`).then(r => r.json()),
        fetch(`${API}/analytics/correlations`).then(r => r.json()),
        fetch(`${API}/analytics/probabilities`).then(r => r.json()),
        fetch(`${API}/analytics/hypothesis`).then(r => r.json())
      ])
      setOverview(o)
      setCorrelations(c)
      setProbabilities(p)
      setHypothesis(h)
    } catch {
      setMessage('Start PostgreSQL, Python and Spring Boot first.')
    }
  }

  useEffect(() => { load() }, [])

  const update = (e) => {
    const { name, value, type, checked } = e.target
    setForm({ ...form, [name]: type === 'checkbox' ? checked : value })
  }

  const save = async (e) => {
    e.preventDefault()
    try {
      const payload = { ...form }
      ;['cgpa','aptitudeScore','codingScore','communicationScore','projects',
        'internships','certifications','attendance','backlogs']
        .forEach(k => payload[k] = Number(payload[k]))

      const r = await fetch(`${API}/students`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      if (!r.ok) throw new Error()
      setMessage('Student saved successfully.')
      await load()
    } catch {
      setMessage('Could not save. Check Spring Boot and PostgreSQL.')
    }
  }

  const predict = async () => {
    const payload = {
      cgpa: Number(form.cgpa),
      aptitude_score: Number(form.aptitudeScore),
      coding_score: Number(form.codingScore),
      communication_score: Number(form.communicationScore),
      projects: Number(form.projects),
      internships: Number(form.internships),
      certifications: Number(form.certifications),
      attendance: Number(form.attendance),
      backlogs: Number(form.backlogs)
    }
    try {
      const r = await fetch(`${API}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      setPrediction(await r.json())
    } catch {
      setMessage('Prediction failed. Check the Python service.')
    }
  }

  const chartData = correlations?.correlations
    ? Object.entries(correlations.correlations).map(([factor, value]) => ({
        factor: factor.replaceAll('_', ' '), value
      }))
    : []

  const fields = [
    ['name','Name','text'],
    ['cgpa','CGPA','number'],
    ['aptitudeScore','Aptitude Score','number'],
    ['codingScore','Coding Score','number'],
    ['communicationScore','Communication Score','number'],
    ['projects','Projects','number'],
    ['internships','Internships','number'],
    ['certifications','Certifications','number'],
    ['attendance','Attendance','number'],
    ['backlogs','Backlogs','number']
  ]

  return (
    <div className="app">
      <header>
        <div>
          <p className="eyebrow">PROBABILITY & STATISTICS PROJECT</p>
          <h1>Placement Prediction</h1>
          <p className="sub">Student placement analytics using statistical analysis</p>
        </div>
        <button className="light" onClick={load}>Refresh Analysis</button>
      </header>

      {message && <div className="notice">{message}</div>}

      <section className="cards">
        <Card title="Total Students" value={overview?.total_students ?? '—'} />
        <Card title="Placed" value={overview?.placed_students ?? '—'} />
        <Card title="Placement Rate" value={overview ? `${overview.placement_rate}%` : '—'} />
        <Card title="Average CGPA" value={overview?.means?.cgpa ?? '—'} />
      </section>

      <div className="grid">
        <section className="panel">
          <h2>Student Input</h2>
          <form onSubmit={save} className="form">
            {fields.map(([key, label, type]) => (
              <label key={key}>
                {label}
                <input
                  name={key}
                  type={type}
                  step={type === 'number' ? '0.01' : undefined}
                  value={form[key]}
                  onChange={update}
                  required
                />
              </label>
            ))}
            <label className="check">
              <input
                type="checkbox"
                name="placementStatus"
                checked={form.placementStatus}
                onChange={update}
              />
              Historical placement status
            </label>
            <div className="buttons">
              <button type="submit">Save Student</button>
              <button type="button" className="secondary" onClick={predict}>
                Predict Placement
              </button>
            </div>
          </form>
        </section>

        <section className="panel">
          <h2>Placement Prediction</h2>
          {prediction ? (
            <div className="prediction">
              <div className="prob">{prediction.probability_percent ?? '—'}%</div>
              <h3>{prediction.prediction}</h3>
              <p>{prediction.model_type || prediction.message}</p>
              {prediction.top_model_factors && (
                <ul>
                  {prediction.top_model_factors.map(x => (
                    <li key={x.factor}>
                      {x.factor.replaceAll('_',' ')}: {x.coefficient}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ) : (
            <div className="empty">Enter values and click Predict Placement.</div>
          )}
        </section>
      </div>

      <div className="grid">
        <section className="panel">
          <h2>Correlation with Placement</h2>
          <ResponsiveContainer width="100%" height={330}>
            <BarChart data={chartData} layout="vertical" margin={{left:35,right:20}}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" domain={[-1,1]} />
              <YAxis type="category" dataKey="factor" width={125} />
              <Tooltip />
              <Bar dataKey="value" />
            </BarChart>
          </ResponsiveContainer>
        </section>

        <section className="panel">
          <h2>Conditional Probability</h2>
          {probabilities && (
            <div className="stats">
              <Row label="P(Placed)" value={`${probabilities.overall}%`} />
              <Row label="P(Placed | CGPA > 8)" value={`${probabilities.cgpa_above_8?.probability_percent ?? '—'}%`} />
              <Row label="P(Placed | Coding > 75)" value={`${probabilities.coding_above_75?.probability_percent ?? '—'}%`} />
              <Row label="P(Placed | Aptitude > 75)" value={`${probabilities.aptitude_above_75?.probability_percent ?? '—'}%`} />
              <Row label="P(Placed | No Backlogs)" value={`${probabilities.no_backlogs?.probability_percent ?? '—'}%`} />
              <Row label="P(Placed | Internship ≥ 1)" value={`${probabilities.internship_at_least_1?.probability_percent ?? '—'}%`} />
            </div>
          )}
        </section>
      </div>

      <section className="panel">
        <h2>Hypothesis Testing</h2>
        {hypothesis && !hypothesis.message ? (
          <>
            <p><b>Question:</b> {hypothesis.question}</p>
            <p><b>H₀:</b> {hypothesis.null_hypothesis}</p>
            <p><b>H₁:</b> {hypothesis.alternative_hypothesis}</p>
            <div className="hyp">
              <Row label="t-statistic" value={hypothesis.t_statistic} />
              <Row label="p-value" value={hypothesis.p_value} />
              <Row label="Significance" value={hypothesis.significance_level} />
              <Row label="Decision" value={hypothesis.decision} />
            </div>
          </>
        ) : (
          <div className="empty">{hypothesis?.message || 'No result.'}</div>
        )}
      </section>

      <footer>Python statistical engine • Spring Boot • PostgreSQL • React</footer>
    </div>
  )
}

function Card({title, value}) {
  return <div className="card"><span>{title}</span><strong>{value}</strong></div>
}

function Row({label, value}) {
  return <div><span>{label}</span><b>{value}</b></div>
}
