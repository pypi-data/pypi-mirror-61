# Broadcaster

Broadcaster helps you develop realtime streaming functionality in by providing
a simple broadcast API onto a number of different backend services.

It currently supports Redis PUB/SUB, and Postgres LISTEN/NOTIFY, plus a simple
in-memory backend, that you can use for local development or during testing.

Here's a complete example of the backend code for a simple websocket chat app:

**app.py**

```python
# Requires: `starlette`, `uvicorn`, `jinja2`
# Run with `uvicorn example:app`
from broadcaster import Broadcast
from starlette.applications import Starlette
from starlette.concurrency import run_until_first_complete
from starlette.routing import Route, WebSocketRoute
from starlette.templating import Jinja2Templates


broadcast = Broadcast("redis://localhost:6379")
templates = Jinja2Templates("templates")


async def homepage(request):
    template = "index.html"
    context = {"request": request}
    return templates.TemplateResponse(template, context)


async def chatroom_ws(websocket):
    await websocket.accept()
    await run_until_first_complete(
        (chatroom_ws_receiver, {"websocket": websocket}),
        (chatroom_ws_sender, {"websocket": websocket}),
    )


async def chatroom_ws_receiver(websocket):
    async for message in websocket.iter_text():
        await broadcast.publish(channel="chatroom", message=message)


async def chatroom_ws_sender(websocket):
    async with broadcast.subscribe(channel="chatroom") as subscriber:
        async for event in subscriber:
            await websocket.send_text(event.message)


routes = [
    Route("/", homepage),
    WebSocketRoute("/", chatroom_ws, name='chatroom_ws'),
]


app = Starlette(
    routes=routes, on_startup=[broadcast.connect], on_shutdown=[broadcast.disconnect],
)
```

## Installation

* `pip install broadcaster`
* `pip install broadcaster[redis]`
* `pip install broadcaster[postgres]`

## Available backends

* `Broadcast('memory://')`
* `Broadcast("redis://localhost:6379")`
* `Broadcast("postgres://localhost:5432/hostedapi")`

## Where next?

* Serialization / deserialization to support broadcasting structured data.
* Backends for Redis Streams, Apache Kafka, and RabbitMQ.
* Add support for `subscribe('chatroom', history=100)` for backends which provide persistence. (Redis Streams, Apache Kafka) This will allow applications to subscribe to channel updates, while also being given an initial window onto the most recent events.
