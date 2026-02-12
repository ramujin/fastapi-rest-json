# FastAPI Full-Stack REST Demo

This repo is a full-stack app using the [FastAPI web framework](https://fastapi.tiangolo.com) and a REST API to manage a simple in-memory users list. The server persists state by writing an atomic JSON snapshot to disk on shutdown.

![Screenshot](screenshot.png)

## Prerequesites

You just need to have Python 3.10+ installed.

## Usage

1. Install `uv` (one-time)

    ```bash
    brew install uv
    ```

    If you don’t use Homebrew, see https://docs.astral.sh/uv/getting-started/ for alternatives.

2. Create a virtual environment and sync dependencies

    ```bash
    uv sync
    ```

3. Run the server (recommended: single worker)

    ```bash
    uv run server/main.py
    ```

## Persistence

- The server keeps data in memory and saves a snapshot only when the application exits (during FastAPI shutdown).
- Default snapshot path: `server/snapshot.users.json`
- If the snapshot file is missing or invalid JSON, the server starts with an empty dataset.
