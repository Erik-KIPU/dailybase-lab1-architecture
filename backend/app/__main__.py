"""Run from the repository root: python -m backend.app."""
import uvicorn

from backend.app.config.settings import Settings
from backend.app.main import create_app


def main() -> None:
    settings = Settings()
    uvicorn.run(create_app(settings), host=settings.http_host, port=settings.http_port)


if __name__ == '__main__':
    main()
