from fastapi import FastAPI
from helper import get_spectral_values
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/seismic_hazard")
async def api_handler(latitude: float, longitude: float, dyhd_no: int):
    ss, s1, pga, pgv = get_spectral_values(dyhd_no, latitude, longitude)

    return {"PGA": pga, "PGV": pgv, "SS": ss, "S1": s1}
