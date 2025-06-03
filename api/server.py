# api/server.py

from ariadne import make_executable_schema, graphql_sync
from ariadne.constants import PLAYGROUND_HTML
from fastapi import FastAPI, Request
from api.schema import type_defs
from api.resolvers import query

schema = make_executable_schema(type_defs, query)
app = FastAPI()

@app.get("/")
async def graphql_playground():
    return PLAYGROUND_HTML

@app.post("/")
async def graphql_server(request: Request):
    data = await request.json()
    success, result = graphql_sync(schema, data, context_value=request, debug=True)
    return result
