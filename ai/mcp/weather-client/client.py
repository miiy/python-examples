import os
import sys
import json
import asyncio
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

class MCPClient:
    # Initialize session and client objects
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.openai_client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith(".py")
        if not is_python:
            raise ValueError("Server script must be a Python file")

        command = "../weather-server/.venv/bin/python"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List avaliable tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        messages = [
            {
                "role": "user",
                "content": query,
            }
        ]
        response = await self.session.list_tools()
        available_tools = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema,
            },
        } for tool in response.tools]


        # Initial OpenAI API call
        response = self.openai_client.chat.completions.create(
            model="deepseek-chat",
            max_tokens=1000,
            messages=messages,
            tools=available_tools
        )

        # Process response and handle tool calls
        final_text = []

        # response.choices[0].message
        # ChatCompletionMessage(content='I can help you get the latest alerts for New York. Let me fetch that information for you.', refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_00_iFEwLSWbpsLNZgiG5AIfWoR6', function=Function(arguments='{"state": "new york"}', name='get_alerts'), type='function', index=0)])

        for content in response.choices:
            print(content.finish_reason)
            if content.finish_reason == "stop":
                final_text.append(content.message.content)
            elif content.finish_reason == "tool_calls":
                tool = content.message.tool_calls[0]
                tool_name = tool.function.name
                tool_arguments = str(tool.function.arguments)
                try:
                    tool_args = json.loads(tool_arguments)
                except Exception as e:
                    print(f"Error: {e}")
                    tool_args = {}

                # Execute tool call
                result = await self.session.call_tool(tool_name, tool_args)
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                messages.append({
                    "role": "assistant",
                    "content": content.message.content,
                })
                messages.append({
                    "role": "user",
                    "content": result.content,
                })

            # Get next response from OpenAI
            response = self.openai_client.chat.completions.create(
                model="deepseek-chat",
                max_tokens=1000,
                messages=messages
            )

            final_text.append(response.choices[0].message.content)

        return "".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nUser: ").strip()

                if query.lower() == "quit":
                    break

                response = await self.process_query(query)
                print("\n", response)
            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())