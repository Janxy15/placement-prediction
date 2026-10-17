import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sqlalchemy import create_engine, text
from config import DATABASE_URL

FEATURES = [
    "cgpa", "aptitude_score", "coding_score", "communication_score",
    "projects", "internships", "certifications", "attendance", "backlogs"
]

def engine():
    return create_engine(DATABASE_URL, pool_pre_ping=True)

def load_students():
    query = """
        SELECT id, name, cgpa, aptitude_score, coding_score,
               communication_score, projects, internships,
               certifications, attendance, backlogs, placement_status
        FROM students ORDER BY id
    """
    with engine().connect() as conn:
        return pd.read_sql(text(query), conn)

def overview():
    df = load_students()
    if df.empty:
        return {"total_students": 0, "placed_students": 0,
                "not_placed_students": 0, "placement_rate": 0,
                "means": {}, "medians": {}, "std_deviations": {}}
    return {
        "total_students": int(len(df)),
        "placed_students": int(df.placement_status.sum()),
        "not_placed_students": int((~df.placement_status).sum()),
        "placement_rate": round(float(df.placement_status.mean() * 100), 2),
        "means": {c: round(float(df[c].mean()), 2) for c in FEATURES},
        "medians": {c: round(float(df[c].median()), 2) for c in FEATURES},
        "std_deviations": {
            c: round(float(df[c].std()), 2) if len(df) > 1 else 0
            for c in FEATURES
        }
    }

def correlations():
    df = load_students()
    if len(df) < 2:
        return {"correlations": {}, "matrix": {}}
    target = df.placement_status.astype(int)
    result = {c: round(float(df[c].corr(target)), 4) for c in FEATURES}
    corr = df[FEATURES + ["placement_status"]].copy()
    corr["placement_status"] = target
    return {"correlations": result, "matrix": corr.corr().round(3).to_dict()}

def probabilities():
    df = load_students()
    if df.empty:
        return {}
    placed = df.placement_status.astype(bool)

    def conditional(mask):
        n = int(mask.sum())
        p = int((mask & placed).sum())
        return {
            "students": n,
            "placed": p,
            "probability_percent": round(100 * p / n, 2) if n else None
        }

    return {
        "overall": round(float(placed.mean() * 100), 2),
        "cgpa_above_8": conditional(df.cgpa > 8),
        "coding_above_75": conditional(df.coding_score > 75),
        "aptitude_above_75": conditional(df.aptitude_score > 75),
        "no_backlogs": conditional(df.backlogs == 0),
        "internship_at_least_1": conditional(df.internships >= 1)
    }

def hypothesis():
    df = load_students()
    if len(df) < 4:
        return {"message": "At least 4 records are needed."}

    placed = df.loc[df.placement_status, "coding_score"]
    not_placed = df.loc[~df.placement_status, "coding_score"]

    if len(placed) < 2 or len(not_placed) < 2:
        return {"message": "Need at least two placed and two non-placed records."}

    test = stats.ttest_ind(placed, not_placed, equal_var=False)
    r, p = stats.pointbiserialr(
        df.placement_status.astype(int), df.coding_score
    )

    return {
        "question": "Does coding performance differ significantly between placed and non-placed students?",
        "null_hypothesis": "There is no significant difference in mean coding score.",
        "alternative_hypothesis": "There is a significant difference in mean coding score.",
        "t_statistic": round(float(test.statistic), 4),
        "p_value": round(float(test.pvalue), 6),
        "significance_level": 0.05,
        "decision": "Reject H0" if test.pvalue < 0.05 else "Fail to reject H0",
        "coding_placement_correlation": round(float(r), 4),
        "correlation_p_value": round(float(p), 6)
    }

def train_model():
    df = load_students()
    if len(df) < 20 or df.placement_status.nunique() < 2:
        return None
    model = LogisticRegression(max_iter=2000)
    model.fit(df[FEATURES].astype(float), df.placement_status.astype(int))
    return model

def predict(payload):
    model = train_model()
    if model is None:
        return {
            "probability_percent": None,
            "prediction": "Not enough historical data",
            "message": "Add at least 20 records containing both placement outcomes."
        }

    row = np.array([[float(payload[x]) for x in FEATURES]])
    probability = float(model.predict_proba(row)[0][1])
    coefficients = model.coef_[0]

    factors = sorted(
        [
            {
                "factor": FEATURES[i],
                "coefficient": round(float(coefficients[i]), 4)
            }
            for i in range(len(FEATURES))
        ],
        key=lambda x: abs(x["coefficient"]),
        reverse=True
    )[:5]

    return {
        "probability_percent": round(probability * 100, 2),
        "prediction": (
            "Likely to be placed"
            if probability >= 0.5
            else "Lower placement probability"
        ),
        "top_model_factors": factors,
        "model_type": "Logistic Regression"
    }
