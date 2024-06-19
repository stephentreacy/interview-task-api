FROM python:3.12-slim

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV DATABASE_URL=sqlite+aiosqlite:///./data/app.db

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# docker build -t weather-app .
# docker run -v weather_db:/usr/src/app/data --rm -p 8000:8000 weather-app