# pgAdmin Guide

## 1. Start Services
```bash
docker compose up -d
```

## 2. Open pgAdmin
- URL: `http://localhost:5050`
- Email: `admin@etl.local`
- Password: `admin123`

## 3. Register Database Server
In pgAdmin:
1. `Servers` -> `Register` -> `Server...`
2. General tab: Name = `etl-local`
3. Connection tab:
   - Host = `postgres`
   - Port = `5432`
   - Username = `etl_user`
   - Password = `etl_password`
4. Save

## 4. Verify Expected Tables
Under `etl_db`, check:
- `staging.products_clean`
- `staging.products_rejected`
- `analytics.category_summary`
- `analytics.top_expensive_stream`

## 5. Quick SQL Checks
```sql
SELECT COUNT(*) FROM staging.products_clean;
SELECT * FROM analytics.category_summary ORDER BY total_inventory_value DESC;
SELECT * FROM analytics.top_expensive_stream ORDER BY consumed_at DESC LIMIT 10;
```
