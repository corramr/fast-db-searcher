from utils.utterances import CAR_UTTERANCES, COUNTRIES_UTTERANCES
from semantic_router import Route
import os
import json
from tqdm import tqdm
from semantic_router.encoders import OpenAIEncoder
from semantic_router.routers import SemanticRouter

# define encoder
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
encoder = OpenAIEncoder(score_threshold=0.16) # you can tune this parameter to steer the performance of your router

# define routes based on some utterances
cars = Route(name="cars", utterances=CAR_UTTERANCES)
countries = Route(name="countries", utterances=COUNTRIES_UTTERANCES)
routes = [cars, countries]

# define router
rl = SemanticRouter(encoder=encoder, routes=routes, auto_sync="local")

# load queries
with open("queries.json", "r") as file:
    queries = json.load(file)

# build report
report = []

for query in tqdm(queries, desc="Processing questions"):
    route = rl(query["query"]).name

    # fill out report
    report.append(
        {
            "query": query["query"],
            "category": query["category"],
            "route": route,
        }
    )

# Save report
with open("report.json", "w") as file:
    file.write(json.dumps(report, indent=4))
