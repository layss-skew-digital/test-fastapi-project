# Customer Support AI Service

A FastAPI server that classifies customer messages into bug reports, feature requests, or general inquiries using OpenAI's GPT models.

## Features

- **Message Classification**: Automatically categorizes customer messages
- **Structured Responses**: Generates appropriate data for each message type
- **AI-Powered**: Uses OpenAI's GPT-4 for intelligent processing
- **Confidence Scores**: Provides confidence levels for classifications
- **Fallback Handling**: Graceful error handling with default responses

## Quick Start

1. Install dependencies:

   ```bash
   poetry install
   ```

2. Create `.env` file:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Run the server:

   ```bash
   poetry run uvicorn main:app --reload
   ```

4. Access the API at http://localhost:8000

## API Usage

### Process Customer Message

**POST** `/process-customer-message`

**Request:**

```json
{
  "customer_id": "user_123",
  "message": "The app crashes when I upload photos",
  "product": "1440 Mobile App"
}
```

**Response:**

```json
{
  "message_type": "bug_report",
  "confidence_score": 0.9,
  "response_data": {
    "ticket": {
      "id": "BUG-A1B2",
      "title": "App crashes on photo upload",
      "severity": "High",
      "affected_components": ["Mobile App"],
      "reproduction_steps": ["Open app", "Try to upload photo", "App crashes"],
      "priority": "High",
      "assigned_team": "Engineering Team"
    }
  },
  "customer_response": "Thank you for reporting this issue. I've created a ticket (ID: BUG-A1B2) and assigned it to our Engineering Team team. They'll investigate this high priority issue and get back to you soon."
}
```

## Message Types & Responses

### Bug Reports

- **Triggers**: Issues, errors, crashes, malfunctions
- **Response**: Creates tickets with severity, priority, reproduction steps
- **Example**: "The app crashes when I try to upload photos"

### Feature Requests

- **Triggers**: New features, improvements, enhancements
- **Response**: Creates product requirements with user stories and business value
- **Example**: "Can you add dark mode to the app?"

### General Inquiries

- **Triggers**: Questions, account issues, billing, usage help
- **Response**: Provides categorization and suggested resources
- **Example**: "How do I change my password?"

## Response Examples

### Feature Request Response

```json
{
  "message_type": "feature_request",
  "confidence_score": 0.85,
  "response_data": {
    "product_requirement": {
      "id": "FR-E5F6",
      "title": "Dark mode support",
      "description": "Add dark mode theme option to the mobile app",
      "user_story": "As a user, I want dark mode so I can use the app comfortably at night",
      "business_value": "High - Improves user experience and accessibility",
      "complexity_estimate": "Medium",
      "affected_components": ["Mobile App"],
      "status": "Under Review"
    }
  },
  "customer_response": "Thank you for your feature request! I've logged this as requirement FR-E5F6 and our product team will review it."
}
```

### General Inquiry Response

```json
{
  "message_type": "general_inquiry",
  "confidence_score": 0.8,
  "response_data": {
    "inquiry_category": "Account Management",
    "requires_human_review": false,
    "suggested_resources": [
      {
        "title": "Account Management Guide",
        "url": "https://help.example.com/account"
      }
    ]
  },
  "customer_response": "Thank you for your question about 1440 Mobile App! I hope the information provided helps."
}
```

## Documentation

- Interactive docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## Testing

```bash
curl -X POST "http://localhost:8000/process-customer-message" \
     -H "Content-Type: application/json" \
     -d '{
       "customer_id": "test_user",
       "message": "The app keeps crashing",
       "product": "1440 Mobile App"
     }'
```

## Dependencies

- `fastapi[standard]`: Web framework
- `openai`: OpenAI API client
- `pydantic`: Data validation
- `python-dotenv`: Environment variable management
