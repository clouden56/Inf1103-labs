FROM python:3.11-slim

WORKDIR /app

COPY persistent_auditor.py .

# inventory.txt lives in /app/data so it can be mounted as a volume
ENV INVENTORY_FILE=/app/data/inventory.txt
RUN mkdir -p /app/data

CMD ["python", "persistent_auditor.py"]
