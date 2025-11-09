# FastAPI Backend

A FastAPI backend for the fullstack application.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- On Windows:
```bash
venv\Scripts\activate
```
- On macOS/Linux:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Provide an OpenAI API key (one of the following):
   - Set the `FLOWPAD_OPENAI_API_KEY` environment variable, **or**
   - Create a file `backend/openai_api_key.txt` containing only the key (this file is ignored by git).

## Running the Server

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

## Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check endpoint
- `GET /api/items` - Get all items
- `POST /api/items` - Create a new item

