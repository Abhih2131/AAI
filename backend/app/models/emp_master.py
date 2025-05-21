import sqlalchemy as sa
from sqlalchemy import MetaData

metadata = MetaData()

EmpMaster = sa.Table(
    "Emp_Master",
    metadata,
    sa.Column("employee_id", sa.Integer, primary_key=True),
    sa.Column("employee_name", sa.String),
    sa.Column("gender", sa.String),
    sa.Column("date_of_birth", sa.String),
    sa.Column("date_of_joining", sa.String),
    sa.Column("date_of_exit", sa.String),
    sa.Column("annual_ctc", sa.Float),
)
