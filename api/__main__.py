"""Start the server with the host and port from api/config.toml: python -m api"""

import uvicorn

from api.core.config import get_settings

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run("api.main:app", host=settings.host, port=settings.port)
