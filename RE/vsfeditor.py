#!/usr/bin/env python3
"""
VSF Editor - Client for Virtual File System Server
"""

import argparse
import asyncio
import json
import struct
import sys
from pathlib import Path
from typing import Dict, List, Any

class VSFClient:
    def __init__(self, host: str = 'localhost', port: int = 8888):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
    
    async def connect(self):
        """Connect to the server"""
        try:
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            print(f"Connected to {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    async def send_command(self, command: str, args: Dict = None) -> Dict:
        """Send command to server and get response"""
        if not self.writer:
            if not await self.connect():
                return {"success": False, "error": "Connection failed"}
        
        try:
            message = {
                "command": command,
                "args": args or {}
            }
            
            message_data = json.dumps(message).encode('utf-8')
            
            # Send message length
            self.writer.write(struct.pack('!I', len(message_data)))
            # Send message
            self.writer.write(message_data)
            await self.writer.drain()
            
            # Read response length
            length_data = await self.reader.read(4)
            if not length_data:
                raise ConnectionError("Connection closed")
                
            length = struct.unpack('!I', length_data)[0]
            
            # Read response
            response_data = await self.reader.read(length)
            if not response_data:
                raise ConnectionError("Connection closed")
                
            response = json.loads(response_data.decode('utf-8'))
            return response
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def list_files(self, path: str = "") -> List[Dict]:
        """List files on server"""
        response = await self.send_command('list', {'path': path})
        if response.get('success'):
            return response.get('data', [])
        else:
            print(f"Error: {response.get('error')}")
            return []
    
    async def read_file(self, path: str) -> bytes:
        """Read file from server"""
        response = await self.send_command('read', {'path': path})
        if response.get('success'):
            return bytes.fromhex(response.get('data', ''))
        else:
            print(f"Error: {response.get('error')}")
            return b''
    
    async def extract_files(self, output_dir: str, files: List[str] = None) -> bool:
        """Extract files from server"""
        response = await self.send_command('extract', {
            'output_dir': output_dir,
            'files': files or []
        })
        
        if response.get('success'):
            result = response.get('data', {})
            extracted = result.get('extracted', 0)
            errors = result.get('errors', [])
            
            print(f"Extracted {extracted} files to {output_dir}")
            if errors:
                print("Errors:")
                for error in errors:
                    print(f"  {error}")
            return True
        else:
            print(f"Error: {response.get('error')}")
            return False
    
    async def get_info(self) -> Dict:
        """Get server information"""
        response = await self.send_command('info')
        if response.get('success'):
            return response.get('data', {})
        else:
            print(f"Error: {response.get('error')}")
            return {}
    
    async def close(self):
        """Close connection"""
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()

async def cmd_list(args):
    """List files command"""
    client = VSFClient(args.host, args.port)
    if not await client.connect():
        return
    
    files = await client.list_files(args.path)
    
    print(f"Files on {args.host}:{args.port}:")
    print("-" * 60)
    for file_info in files:
        icon = "📁" if file_info['is_dir'] else "📄"
        size = f"{file_info['size']:>10}" if not file_info['is_dir'] else " " * 10
        print(f"{icon} {size}  {file_info['path']}")
    
    await client.close()

async def cmd_cat(args):
    """Cat file command"""
    client = VSFClient(args.host, args.port)
    if not await client.connect():
        return
    
    content = await client.read_file(args.path)
    
    try:
        # Try to decode as text
        text = content.decode('utf-8', errors='replace')
        print(text)
    except UnicodeDecodeError:
        # Binary file, show hex preview
        print(f"Binary file ({len(content)} bytes)")
        if len(content) > 0:
            print(f"First 16 bytes: {content[:16].hex()}")
    
    await client.close()

async def cmd_extract(args):
    """Extract files command"""
    client = VSFClient(args.host, args.port)
    if not await client.connect():
        return
    
    success = await client.extract_files(args.output, args.files)
    await client.close()
    
    if success:
        print("Extraction completed")
    else:
        print("Extraction failed")

async def cmd_info(args):
    """Server info command"""
    client = VSFClient(args.host, args.port)
    if not await client.connect():
        return
    
    info = await client.get_info()
    
    print("Server Information:")
    print("-" * 40)
    for key, value in info.items():
        print(f"{key:15}: {value}")
    
    await client.close()

async def cmd_shell(args):
    """Interactive shell"""
    client = VSFClient(args.host, args.port)
    if not await client.connect():
        return
    
    print(f"VSF Editor Shell - Connected to {args.host}:{args.port}")
    print("Type 'help' for commands, 'exit' to quit")
    
    while True:
        try:
            command = input(f"vsf@{args.host}> ").strip().split()
            if not command:
                continue
                
            cmd = command[0].lower()
            
            if cmd == 'exit' or cmd == 'quit':
                break
            elif cmd == 'help':
                print_help()
            elif cmd == 'list' or cmd == 'ls':
                path = command[1] if len(command) > 1 else ""
                files = await client.list_files(path)
                for file_info in files:
                    icon = "📁" if file_info['is_dir'] else "📄"
                    size = f"{file_info['size']:>10}" if not file_info['is_dir'] else " " * 10
                    print(f"{icon} {size}  {file_info['path']}")
            elif cmd == 'cat':
                if len(command) > 1:
                    content = await client.read_file(command[1])
                    try:
                        text = content.decode('utf-8', errors='replace')
                        print(text)
                    except UnicodeDecodeError:
                        print(f"Binary file ({len(content)} bytes)")
                else:
                    print("Usage: cat <file>")
            elif cmd == 'info':
                info = await client.get_info()
                for key, value in info.items():
                    print(f"{key:15}: {value}")
            elif cmd == 'ping':
                response = await client.send_command('ping')
                print(response.get('data', 'No response'))
            else:
                print("Unknown command. Type 'help' for available commands.")
                
        except (KeyboardInterrupt, EOFError):
            print()
            break
        except Exception as e:
            print(f"Error: {e}")
    
    await client.close()

def print_help():
    """Print shell help"""
    help_text = """
Available commands:
  help          - Show this help
  list [path]   - List files in directory
  cat <file>    - Display file content
  info          - Show server information
  ping          - Test connection
  exit/quit     - Exit shell
"""
    print(help_text)

def main():
    parser = argparse.ArgumentParser(description="VSF Editor Client")
    parser.add_argument('--host', default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=8888, help='Server port')
    
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # List command
    list_parser = subparsers.add_parser('list', help='List files')
    list_parser.add_argument('path', nargs='?', default='', help='Directory path')
    list_parser.set_defaults(func=cmd_list)
    
    # Cat command
    cat_parser = subparsers.add_parser('cat', help='Display file content')
    cat_parser.add_argument('path', help='File path')
    cat_parser.set_defaults(func=cmd_cat)
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract files')
    extract_parser.add_argument('output', help='Output directory')
    extract_parser.add_argument('files', nargs='*', help='Files to extract')
    extract_parser.set_defaults(func=cmd_extract)
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Server information')
    info_parser.set_defaults(func=cmd_info)
    
    # Shell command
    shell_parser = subparsers.add_parser('shell', help='Interactive shell')
    shell_parser.set_defaults(func=cmd_shell)
    
    args = parser.parse_args()
    
    # Add host/port to args for subcommands
    args.host = parser.parse_known_args()[0].host
    args.port = parser.parse_known_args()[0].port
    
    asyncio.run(args.func(args))

if __name__ == "__main__":
    main()
