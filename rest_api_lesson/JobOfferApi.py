from __future__ import annotations
from rest_api_lesson.InfoJobsApi import create_info_jobs_api, JobOffer
from fastapi import FastAPI, Query
from typing import List
from pydantic import BaseModel

app = FastAPI()

class ResponseJobOffer(BaseModel):
    title: str | None = None
    category: str | None = None
    subcategory: str | None = None
    city: str | None = None
    province: str | None = None
    salaryMin: str | None = None
    salaryMax: str | None = None
    salaryPeriod: str | None = None
    experienceMin: str | None = None

    @classmethod
    def from_job_offer(cls: ResponseJobOffer, job_offer: JobOffer):
        return cls(title=job_offer.title, 
                   category=job_offer.category, 
                   subcategory=job_offer.subcategory, 
                   city=job_offer.city, 
                   province=job_offer.province, 
                   salaryMin=job_offer.salaryMin,
                   salaryMax=job_offer.salaryMax,
                   salaryPeriod=job_offer.salaryPeriod,
                   experienceMin=job_offer.experienceMin)


@app.get('/offer')
async def get_jobs(keyword: str = Query(None), 
            category: str = Query(None),
            subcategory: str = Query(None),
            city: str = Query(None),
            province: str = Query(None),
            salaryMin: str = Query(None),
            salaryMax: str = Query(None),
            experienceMin: str = Query(None), 
            dummy: bool = Query(False)) -> List[ResponseJobOffer]:

    args = {
            "keyword": keyword,
            "category": category,
            "subcategory": subcategory,
            "city": city,
            "province": province,
            "salaryMin": salaryMin,
            "salaryMax": salaryMax,
            "experienceMin": experienceMin,
            "dummy": dummy
        }

    app = create_info_jobs_api()
    job_offers = app.get_jobs(args)

    return [ResponseJobOffer.from_job_offer(job_offer) for job_offer in job_offers]
