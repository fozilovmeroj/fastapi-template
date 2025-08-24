from fastapi import Request, Depends


def get_log_data(request: Request):
    client_host = request.client.host
    user_agent = request.headers.get("user-agent")
    return {
        "ip_address": client_host,
        "user_agent": user_agent,
    }
