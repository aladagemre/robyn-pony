# ---- Build the PostgreSQL Base ----
FROM postgres:latest AS postgres-base

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=robyndb

# ---- Build the Python App ----
FROM python:3.11-bookworm

# Install supervisor and postgresql-client
RUN apt-get update && apt-get install -y supervisor postgresql-client

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements .
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application
COPY app/ app/
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy PostgreSQL binaries from the first stage
COPY --from=postgres-base /usr/local/bin /usr/local/bin
COPY --from=postgres-base /usr/lib/postgresql /usr/lib/postgresql
COPY --from=postgres-base /usr/share/postgresql /usr/share/postgresql
COPY --from=postgres-base /var/lib/postgresql /var/lib/postgresql

# Create necessary directories for PostgreSQL
RUN mkdir -p /var/run/postgresql && chown -R postgres:postgres /var/run/postgresql

# Environment variables
ENV PYTHONPATH=/app
ENV DATABASE_URL=postgresql://postgres:password@localhost:5432/robyndb
ENV ENVIRONMENT=production

# Expose ports (Robyn and PostgreSQL)
EXPOSE 8000 5432

CMD ["/usr/bin/supervisord"]
