import aiohttp
from aiohttp import web
from aiohttp.client import request

import state
import guess_number

HOST_IP = "0.0.0.0"
HOST_PORT = 1254

async def skill_chislo(request_obj):
    request = await request_obj.json

    response = {}
    response["version"] = request["version"]
    response["session"] = request["session"]
    response["response"] = {"end_session" : False}
    user_state = state.get_state(request)
    session_state = user_state.get_session_state()

    if request["session"]["state"]:
        new_state = guess_number.get_root_state
    else:
        current_state = guess_number.get_state(session_state["current_state_id"])
        new_state = current_state.get_next_state(request["request"]["command"])

    response["response"]["text"] = new_state.get_text()
    if not new_state.is_end_state():
        session_state["current_state_id"] = new_state.get_id()
        user_state.save_session_state(response)
    else:
        response["response"]["end_session"] = True
    
    return web.json_response(response)

def init():
    app = web.Application()
    app.router.add_post("/skill_chislo", skill_chislo)
    web.run_app(app, host = HOST_IP, port = HOST_PORT)

if __name__ == "__main__":
    init()
