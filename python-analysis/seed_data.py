import random
from sqlalchemy import create_engine, text
from config import DATABASE_URL

random.seed(42)
engine = create_engine(DATABASE_URL)

def make_student(i):
    cgpa = round(random.uniform(5.5, 9.7), 2)
    aptitude = round(min(100, max(0, random.gauss(68 + (cgpa - 7) * 7, 11))), 2)
    coding = round(min(100, max(0, random.gauss(64 + (cgpa - 7) * 8, 14))), 2)
    communication = round(min(100, max(0, random.gauss(68 + (cgpa - 7) * 4, 10))), 2)
    projects = random.randint(0, 5)
    internships = random.randint(0, 2)
    certifications = random.randint(0, 6)
    attendance = round(min(100, max(50, random.gauss(82, 9))), 2)
    backlogs = random.choices([0, 1, 2, 3], weights=[70, 20, 8, 2])[0]

    score = (
        0.55 * (cgpa - 5.5) / 4.2 +
        0.20 * aptitude / 100 +
        0.25 * coding / 100 +
        0.08 * communication / 100 +
        0.04 * projects / 5 +
        0.05 * internships / 2 +
        0.03 * certifications / 6 +
        0.03 * attendance / 100 -
        0.12 * min(backlogs, 3) / 3
    )

    probability = 1 / (1 + pow(2.718281828, -6 * (score - 0.63)))
    placed = random.random() < probability

    return (
        f"Student {i}", cgpa, aptitude, coding, communication,
        projects, internships, certifications, attendance, backlogs, placed
    )

rows = [make_student(i) for i in range(1, 301)]

sql = text("""
INSERT INTO students
(name, cgpa, aptitude_score, coding_score, communication_score,
 projects, internships, certifications, attendance, backlogs, placement_status)
VALUES
(:name, :cgpa, :aptitude, :coding, :communication,
 :projects, :internships, :certifications, :attendance, :backlogs, :placed)
""")

with engine.begin() as conn:
    count = conn.execute(text("SELECT COUNT(*) FROM students")).scalar()

    if count == 0:
        for row in rows:
            conn.execute(sql, {
                "name": row[0],
                "cgpa": row[1],
                "aptitude": row[2],
                "coding": row[3],
                "communication": row[4],
                "projects": row[5],
                "internships": row[6],
                "certifications": row[7],
                "attendance": row[8],
                "backlogs": row[9],
                "placed": row[10]
            })
        print("Inserted 300 synthetic development records.")
    else:
        print(f"Database contains {count} records; no seed data inserted.")
