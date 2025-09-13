#!/usr/bin/env python3
"""
VSF Server - Virtual File System Server for remote access
"""

import argparse
import asyncio
import json
import os
import shutil
import signal
import socket
import struct
import sys
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class VfsEntry:
    path: str
    size: int
    is_dir: bool
    mtime: float

@dataclass
class ServerResponse:
    success: bool
    data: Any = None
    error: str = ""

class VSFServer:
    def __init__(self, host: str = 'localhost', port: int = 8888):
        self.host = host
        self.port = port
        self.server = None
        self.clients = set()
        
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """Handle incoming client connections"""
        client_addr = writer.get_extra_info('peername')
        print(f"Client connected: {client_addr}")
        self.clients.add(writer)
        
        try:
            while True:
                # Read message length
                length_data = await reader.read(4)
                if not length_data:
                    break
                    
                length = struct.unpack('!I', length_data)[0]
                
                # Read message data
                message_data = await reader.read(length)
                if not message_data:
                    break
                    
                # Parse and process message
                try:
                    message = json.loads(message_data.decode('utf-8'))
                    response = await self.process_command(message)
                    
                    # Send response
                    response_data = json.dumps(asdict(response)).encode('utf-8')
                    writer.write(struct.pack('!I', len(response_data)))
                    writer.write(response_data)
                    await writer.drain()
                    
                except json.JSONDecodeError:
                    error = ServerResponse(False, error="Invalid JSON")
                    error_data = json.dumps(asdict(error)).encode('utf-8')
                    writer.write(struct.pack('!I', len(error_data)))
                    writer.write(error_data)
                    await writer.drain()
                    
        except (ConnectionResetError, asyncio.IncompleteReadError):
            print(f"Client disconnected: {client_addr}")
        finally:
            self.clients.discard(writer)
            writer.close()
            await writer.wait_closed()
    
    async def process_command(self, message: Dict) -> ServerResponse:
        """Process client commands"""
        cmd = message.get('command')
        args = message.get('args', {})
        
        try:
            if cmd == 'list':
                return await self.cmd_list(args)
            elif cmd == 'read':
                return await self.cmd_read(args)
            elif cmd == 'exists':
                return await self.cmd_exists(args)
            elif cmd == 'extract':
                return await self.cmd_extract(args)
            elif cmd == 'info':
                return await self.cmd_info()
            elif cmd == 'ping':
                return ServerResponse(True, "pong")
            else:
                return ServerResponse(False, error=f"Unknown command: {cmd}")
                
        except Exception as e:
            return ServerResponse(False, error=str(e))
    
    async def cmd_list(self, args: Dict) -> ServerResponse:
        """List files in directory"""
        path = args.get('path', '')
        base_path = Path(path) if path else Path.cwd()
        
        if not base_path.exists():
            return ServerResponse(False, error=f"Path not found: {path}")
        
        entries = []
        try:
            for item in base_path.rglob('*'):
                try:
                    rel_path = str(item.relative_to(base_path))
                    stat = item.stat()
                    entries.append(VfsEntry(
                        path=rel_path,
                        size=stat.st_size,
                        is_dir=item.is_dir(),
                        mtime=stat.st_mtime
                    ))
                except (PermissionError, OSError):
                    continue
        except (PermissionError, OSError):
            pass
            
        return ServerResponse(True, [asdict(entry) for entry in entries])
    
    async def cmd_read(self, args: Dict) -> ServerResponse:
        """Read file content"""
        path = args.get('path')
        if not path:
            return ServerResponse(False, error="No path specified")
        
        file_path = Path(path)
        if not file_path.exists() or file_path.is_dir():
            return ServerResponse(False, error=f"File not found: {path}")
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            return ServerResponse(True, content.hex())
        except (PermissionError, OSError) as e:
            return ServerResponse(False, error=str(e))
    
    async def cmd_exists(self, args: Dict) -> ServerResponse:
        """Check if path exists"""
        path = args.get('path')
        if not path:
            return ServerResponse(False, error="No path specified")
        
        file_path = Path(path)
        return ServerResponse(True, file_path.exists())
    
    async def cmd_extract(self, args: Dict) -> ServerResponse:
        """Extract files"""
        output_dir = args.get('output_dir')
        files = args.get('files', [])
        
        if not output_dir:
            return ServerResponse(False, error="No output directory specified")
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        extracted = 0
        errors = []
        
        if files:
            for file_path in files:
                try:
                    src_path = Path(file_path)
                    dst_path = output_path / src_path.name
                    
                    if src_path.is_dir():
                        shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                    else:
                        shutil.copy2(src_path, dst_path)
                    extracted += 1
                except Exception as e:
                    errors.append(f"{file_path}: {e}")
        else:
            # Extract current directory
            try:
                for item in Path.cwd().rglob('*'):
                    try:
                        rel_path = item.relative_to(Path.cwd())
                        dst_path = output_path / rel_path
                        
                        if item.is_dir():
                            dst_path.mkdir(parents=True, exist_ok=True)
                        else:
                            dst_path.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(item, dst_path)
                            extracted += 1
                    except Exception:
                        continue
            except Exception as e:
                errors.append(str(e))
        
        result = {
            'extracted': extracted,
            'errors': errors
        }
        return ServerResponse(True, result)
    
    async def cmd_info(self) -> ServerResponse:
        """Get server information"""
        info = {
            'hostname': socket.gethostname(),
            'platform': sys.platform,
            'current_dir': str(Path.cwd()),
            'timestamp': time.time()
        }
        return ServerResponse(True, info)
    
    async def start(self):
        """Start the server"""
        self.server = await asyncio.start_server(
            self.handle_client, self.host, self.port
        )
        
        addrs = ', '.join(str(sock.getsockname()) for sock in self.server.sockets)
        print(f"VSF Server listening on {addrs}")
        
        async with self.server:
            await self.server.serve_forever()
    
    async def stop(self):
        """Stop the server"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            print("Server stopped")

async def main():
    parser = argparse.ArgumentParser(description="VSF Server")
    parser.add_argument('--host', default='localhost', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8888, help='Port to listen on')
    parser.add_argument('--password', help='Authentication password')
    
    args = parser.parse_args()
    
    server = VSFServer(args.host, args.port)
    
    # Handle graceful shutdown
    def signal_handler():
        print("\nShutting down server...")
        asyncio.create_task(server.stop())
    
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, signal_handler)
    
    try:
        await server.start()
    except asyncio.CancelledError:
        print("Server stopped")

if __name__ == "__main__":
    asyncio.run(main())
