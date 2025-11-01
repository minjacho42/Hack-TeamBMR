from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/stt")


@router.websocket("/ws")
async def stt_websocket(websocket: WebSocket):
    await websocket.accept()

    await websocket.send_json(
        {"event": "session.ready", "data": {"sessionId": "ses_1"}, "ts": 1730360000}
    )

    try:
        while True:
            message = await websocket.receive_json()
            event = message.get("event")

            if event == "session.close":
                await websocket.close()
                break

            if event == "rtc.offer":
                await websocket.send_json(
                    {
                        "event": "rtc.answer",
                        "data": {"sdp": "...", "type": "answer"},
                        "ts": 1730360001,
                    }
                )
            elif event == "rtc.candidate":
                # Echo ICE candidates for signaling confirmation
                await websocket.send_json(
                    {"event": "rtc.candidate", "data": message.get("data"), "ts": 1730360002}
                )
            elif event == "rtc.stop":
                await websocket.close()
                break
            else:
                await websocket.send_json(
                    {
                        "event": "error",
                        "data": {
                            "code": "UNHANDLED_EVENT",
                            "message": f"Unhandled event {event}",
                        },
                        "ts": 1730360003,
                    }
                )
    except WebSocketDisconnect:
        pass
