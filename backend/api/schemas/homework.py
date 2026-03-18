from datetime import datetime
from pydantic import BaseModel



class HomeworkRequest(BaseModel):
    group_data_value: str
    date_data_value: str
    lesson_index: int
    homework: str