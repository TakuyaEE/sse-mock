# dify-mock
## 起動
```
pip install -r requirements.txt 
python main.py
```

## blocking
```
curl -N -X POST \
-H "Content-Type: application/json" \
-H "accept: text/event-stream" \
-d '{"inputs": "sample", "response_mode":"blocking","user": "test"}' \
http://localhost:8000/v1/workflows/run
```

## streaming
```
curl -N -X POST \
-H "Content-Type: application/json" \
-H "accept: text/event-stream" \
-d '{"inputs": "sample", "response_mode":"streaming","user": "test"}' \
http://localhost:8000/v1/workflows/run
```