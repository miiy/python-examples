# coze api

## curl

```bash
# conversation
curl --location --request curl -X GET "http://127.0.0.1:8888/v1/conversations?bot_id=7579096325656936448&page_num=1&page_size=20" -H "Authorization: Bearer pat_xxx"

# chat
curl --location --request POST 'http://127.0.0.1:8888/v3/chat' \
--header 'Authorization: Bearer pat_xxx' \
--header 'Content-Type: application/json' \
--data-raw '{
    "bot_id": "7575148374337257472",
    "user_id": "123456789",
    "stream": true,
    "auto_save_history":true,
    "additional_messages":[
        {
            "role":"user",
            "content":"2024年10月1日是星期几",
            "content_type":"text"
        }
    ]
}'

# workflow
curl --location --request POST 'http://127.0.0.1:8888/v1/workflow/run' \
--header 'Authorization: Bearer pat_xxx' \
--header 'Content-Type: application/json' \
--data-raw '{
    "workflow_id": "7574387685809192960",
    "parameters":{"question":"hello"},
    "space_id":"7574380105284190208"
}'
```