# Railway Deployment Guide

## Required Services

Add these services to your Railway project in this order:

1. **PostgreSQL** (Database)
   - Add via "New" → "Database" → "PostgreSQL"
   - Railway will auto-inject `DATABASE_URL` environment variable

2. **Redis** (Cache/Message Broker)
   - Add via "New" → "Data" → "Redis"
   - Railway will auto-inject `REDIS_URL` environment variable

3. **Backend** (FastAPI)
   - Deploy from `backend/` directory
   - Set `Start Command`: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - Add environment variable: `DATABASE_URL` (auto from PostgreSQL)
   - Add environment variable: `REDIS_URL` (auto from Redis)

4. **Frontend** (Next.js)
   - Deploy from `frontend/` directory
   - Set `Start Command`: `npm run start`
   - Set `NODE_ENV`: `production`
   - Add environment variable: `NEXT_PUBLIC_API_URL` = `https://<your-backend-url>.up.railway.app`

5. **Celery Worker** (Background Tasks)
   - Deploy from `backend/` directory
   - Set `Start Command`: `celery -A app.workers.celery_app worker --loglevel=info`
   - Add environment variables: `DATABASE_URL`, `REDIS_URL`

## Environment Variables

### Backend
```
DATABASE_URL=${{ Postgres.DATABASE_URL }}
REDIS_URL=${{ Redis.REDIS_URL }}
NODE_ENV=production
```

### Frontend
```
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://<backend-service-url>.up.railway.app
```

### Celery Worker
```
DATABASE_URL=${{ Postgres.DATABASE_URL }}
REDIS_URL=${{ Redis.REDIS_URL }}
```

## Important Notes

1. **DATABASE_URL Format**: Railway auto-injects the correct URL. Do NOT use localhost.
   - Correct: `postgresql://postgres:password@postgresql.railway.internal:5432/railway`
   - Wrong: `postgresql://postgres:password@localhost:5432/wartracker`

2. **NODE_ENV**: Must be `production` for production deployment

3. **Redis**: Required for Celery workers. Add Redis service before deploying backend/celery.

4. **Celery**: Separate service needed for background task processing.

## Troubleshooting

### "Not Found" Page
- Check that frontend is deployed and running
- Verify `NEXT_PUBLIC_API_URL` points to correct backend URL
- Check Railway logs for deployment errors

### Database Connection Errors
- Ensure PostgreSQL service is added
- Verify `DATABASE_URL` environment variable is set
- Check that DATABASE_URL uses Railway's internal hostname, not localhost

### Redis Connection Errors
- Ensure Redis service is added
- Verify `REDIS_URL` environment variable is set

### Celery Not Starting
- Ensure Redis service exists (Celery needs Redis as broker)
- Check `REDIS_URL` is configured
- Verify celery command in Railway dashboard

## Costs

Railway charges based on:
- Compute time (CPU/RAM usage)
- Database storage
- Network egress

Monitor usage in Railway dashboard to avoid surprise costs.
