# mood-decode

## API Documentation

This FastAPI application provides NLP endpoints for emotion analysis, crisis detection, and text summarization.

### Base URL

```
https://mood-decode.onrender.com
```

---

## Endpoints

### 1. Analyze Mood

**POST** `/analyze_mood`

Analyze the emotional tone of a given text.

#### Request Body
```json
{
  "text": "string"
}
```

#### Response
```json
{
  "emotion": "happy | sad | angry | fear | surprise | disgust | neutral",
  "confidence": 0.0
}
```

#### Example
**Request:**
```json
{
  "text": "I'm thrilled about my promotion!"
}
```
**Response:**
```json
{
  "emotion": "happy",
  "confidence": 0.9
}
```

---

### 2. Detect Crisis

**POST** `/detect_crisis`

Detects potential mental health crisis indicators in the text.

#### Request Body
```json
{
  "text": "string"
}
```

#### Response
```json
{
  "crisis_detected": true,
  "severity": "none | low | moderate | high",
  "confidence": 0.0
}
```

#### Example
**Request:**
```json
{
  "text": "I don't want to be here anymore."
}
```
**Response:**
```json
{
  "crisis_detected": true,
  "severity": "high",
  "confidence": 0.95
}
```

---

### 3. Summarize Text

**POST** `/summarize`

Summarizes long text into a concise version.

#### Request Body
```json
{
  "text": "string"
}
```

#### Response
```json
{
  "summary": "string"
}
```

#### Example
**Request:**
```json
{
  "text": "Climate change is a long-term shift in global or regional climate patterns... (long text)"
}
```
**Response:**
```json
{
  "summary": "Climate change refers to significant, long-term changes in the global climate, often caused by human activities."
}
```

---

## Health Check

- `GET /` — API health and endpoint listing
- `GET /health` — Simple health check

---

## Error Handling

All endpoints return standard HTTP error codes and a JSON error message in case of failure.

---

