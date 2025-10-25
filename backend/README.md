# Backend Todo List API

Backend Flask per l'applicazione Todo List.

## Setup

1. Creare l'ambiente virtuale:
```bash
python3 -m venv venv
```

2. Attivare l'ambiente virtuale:
```bash
source venv/bin/activate  # Linux/Mac
# oppure
venv\Scripts\activate  # Windows
```

3. Installare le dipendenze:
```bash
pip install -r requirements.txt
```

## Avvio Server

```bash
python app.py
```

Il server sarà disponibile su `http://localhost:5000`

## API Endpoints

### Tasks

**GET /api/tasks** - Ottieni tutte le task
- Query params opzionali:
  - `status=pending|completed`
  - `priority=high|medium|low`
  - `category_id=<id>`
  - `search=<testo>`

**GET /api/tasks/:id** - Ottieni una singola task

**POST /api/tasks** - Crea una nuova task
```json
{
  "title": "Titolo obbligatorio",
  "description": "Descrizione opzionale",
  "priority": "high|medium|low",
  "due_date": "2025-10-30T10:00:00"
}
```

**PUT /api/tasks/:id** - Aggiorna una task
```json
{
  "title": "Nuovo titolo",
  "priority": "low",
  "status": "completed"
}
```

**DELETE /api/tasks/:id** - Elimina una task

**PATCH /api/tasks/:id/toggle** - Cambia lo stato di completamento della task

## Esempi di Test

```bash
# Ottieni tutte le task
curl http://localhost:5000/api/tasks

# Crea una task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Test task","priority":"high"}'

# Filtra per priorità
curl http://localhost:5000/api/tasks?priority=high

# Aggiorna una task
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"completed"}'

# Toggle completamento
curl -X PATCH http://localhost:5000/api/tasks/1/toggle

# Elimina una task
curl -X DELETE http://localhost:5000/api/tasks/1
```

## Database

Il database SQLite viene creato automaticamente in `database.db` al primo avvio.

### Schema

**tasks**:
- id (INTEGER PRIMARY KEY)
- title (TEXT NOT NULL)
- description (TEXT)
- created_at (DATETIME)
- due_date (DATETIME)
- priority (TEXT) - 'high', 'medium', 'low'
- status (TEXT) - 'pending', 'completed'
- category_id (INTEGER FOREIGN KEY)

**categories** (da implementare):
- id (INTEGER PRIMARY KEY)
- name (TEXT NOT NULL)
- color (TEXT)
- created_at (DATETIME)

## Tecnologie

- Flask 3.0.0
- Flask-CORS 4.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-Migrate 4.0.5
- SQLite

## Note di Sviluppo

- CORS è abilitato per consentire richieste dal frontend Angular (porta 4200)
- Tutte le risposte includono un campo `success` per indicare l'esito dell'operazione
- Gli errori restituiscono status code HTTP appropriati (400, 404, 500)
- Le date sono gestite in formato ISO 8601
