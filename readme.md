# Cook Book

### Requirements

- External database (tested with PostgreSQL and SQLite)

#### Environment variables

- SECRET_KEY
- DATABASE_URI
- GOOGLE_CLIENT_ID
- GOOGLE_CLIENT_SECRET

---

### Docker
- `docker build -t cookbook .`
- `docker run -p 8000:8000 -e SECRET_KEY=1234567890abcdefghijklmnopqrstuv -e DATABASE_URI=DATABASE_URI=postgresql://user:password@127.0.0.1/cookbook -e GOOGLE_CLIENT_ID=appid -e GOOGLE_CLIENT_SECRET=appsecret cookbook`
