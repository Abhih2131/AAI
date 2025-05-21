from fastapi import APIRouter
from app.core.database import database
from app.models.emp_master import EmpMaster
from datetime import datetime

router = APIRouter()

def fy_range():
    now = datetime.now()
    if now.month >= 4:
        start = datetime(now.year, 4, 1)
        end = datetime(now.year + 1, 3, 31)
    else:
        start = datetime(now.year - 1, 4, 1)
        end = datetime(now.year, 3, 31)
    return start, end

@router.get("/executive-summary")
async def executive_summary():
    query = EmpMaster.select()
    rows = await database.fetch_all(query)

    today = datetime.now()
    fy_start, fy_end = fy_range()

    # Filters
    active = [r for r in rows if r["date_of_exit"] == "NA"]
    exited_this_fy = [
        r for r in rows if r["date_of_exit"] not in ("NA", None, "") and
        fy_start <= datetime.strptime(r["date_of_exit"], "%d-%b-%y") <= fy_end
    ]
    joined_this_fy = [
        r for r in rows if r["date_of_joining"] not in (None, "") and
        fy_start <= datetime.strptime(r["date_of_joining"], "%d-%b-%y") <= fy_end
        and r["date_of_exit"] == "NA"
    ]

    # KPIs
    current_headcount = len(active)
    total_cost = sum([r["annual_ctc"] or 0 for r in active])
    avg_age = (
        sum([
            (today - datetime.strptime(r["date_of_birth"], "%d-%b-%y")).days // 365
            for r in active if r["date_of_birth"] not in (None, "")
        ]) / current_headcount
    ) if current_headcount else 0
    exits = len(exited_this_fy)
    joiners = len(joined_this_fy)
    opening_headcount = sum([
        1 for r in rows if (
            (r["date_of_joining"] == "" or datetime.strptime(r["date_of_joining"], "%d-%b-%y") <= fy_start)
            and (r["date_of_exit"] == "NA" or datetime.strptime(r["date_of_exit"], "%d-%b-%y") > fy_start)
        )
    ])
    closing_headcount = current_headcount
    avg_fy_headcount = (opening_headcount + closing_headcount) / 2 if (opening_headcount + closing_headcount) > 0 else 1
    attrition = (exits / avg_fy_headcount) * 100 if avg_fy_headcount else 0

    return {
        "current_headcount": current_headcount,
        "total_cost": total_cost,
        "average_age": round(avg_age, 1),
        "joiners_this_year": joiners,
        "exits_this_year": exits,
        "attrition_percent": round(attrition, 2),
    }
