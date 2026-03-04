from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
# -------------------------
# HTTP Health Check Endpoint
# -------------------------
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

def run_health_server():
    server = HTTPServer(('0.0.0.0', 10000), HealthHandler)
    server.serve_forever()

import asyncio
import json
import websockets
import NodeClass
from spawner import spawn_agents

connected_clients = set()
event_loop = None  


# -------------------------
# WebSocket handler (Frontend → Python)
# -------------------------
## handler function is not needed with aiohttp refactor, so remove it

            def on_udp_message(msg, addr):
                print(f"Node received message: {msg} from {addr}")
                asyncio.run_coroutine_threadsafe(
                    broadcast(msg),
                    event_loop
                )
            node.on_message = on_udp_message

            async def broadcast(message):
                if not connected_clients:
                    return
                try:
                    payload = json.loads(message)
                except Exception:
                    payload = {
                        "type": "node_message",
                        "payload": message
                    }
                msg_str = json.dumps(payload)
                for ws in connected_clients:
                    await ws.send_str(msg_str)
            # Package the agent's current state
            agent_data.append({
                "id": agent.agent_id,
                "position": agent.current_position,
                "target_frontier": agent.target_frontier,
                "cells_discovered": len(agent.local_map)
            })

        # Calculate exploration percentage
        explored = set()
        for agent in agents:
            explored.update(agent.local_map.keys())
        total_open = sum(1 for row in maze for cell in row if cell == 0)
        explored_pct = (len(explored) / total_open * 100) if total_open > 0 else 0

        # 3. Create the JSON payload for the frontend
        payload = {
            "type": "tick_update",
            "tick": tick,
            "goal_reached": goal_reached,
            "explored_pct": round(explored_pct, 1),
            "discovered_cell_positions": [list(cell) for cell in explored],
            "agents": agent_data
        }
        
        # 4. Send the data to the frontend
        await websocket.send(json.dumps(payload))
        
        # 5. Pause briefly to allow the frontend to render the frame smoothly
        await asyncio.sleep(0.1)

    # Compute coverage across all agents and send simulation summary
    explored = set()
    for agent in agents:
        explored.update(agent.local_map.keys())

    total_open = sum(1 for row in maze for cell in row if cell == 0)
    explored_pct = (len(explored) / total_open * 100) if total_open > 0 else 0

    await websocket.send(json.dumps({
        "type": "simulation_complete",
        "goal_reached": goal_reached,
        "tick": tick,
        "explored_cells": len(explored),
        "total_cells": total_open,
        "explored_pct": round(explored_pct, 1)
    }))

# -------------------------
# Main entry point
# -------------------------
async def main():
    global event_loop
    event_loop = asyncio.get_running_loop()  

    global event_loop
    event_loop = asyncio.get_running_loop()
    app = web.Application()
    app.router.add_get('/ws', websocket_handler)
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()
    print("🚀 aiohttp server running on http://0.0.0.0:10000 (WebSocket at /ws)")
    udp_listener = asyncio.create_task(node.web_listen())
    await udp_listener


if __name__ == "__main__":
    asyncio.run(main())
