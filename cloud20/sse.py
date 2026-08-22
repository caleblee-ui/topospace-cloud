
import json
def encode_sse(event,data):
    return f"event: {event}\ndata: {json.dumps(data,separators=(',',':'))}\n\n".encode()
