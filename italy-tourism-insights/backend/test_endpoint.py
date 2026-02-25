#!/usr/bin/env python
from routes.chatbot import ChatMessage, chat
import asyncio
import json

async def test_greeting():
    """Test with greeting message without language override"""
    request = ChatMessage(message="Hello! I'm ready to help you explore Italy!", language=None)
    result = await chat(request)
    print('Response:', result.response[:100])
    print('Recommendations count:', len(result.recommendations))
    print('Message type:', result.message_type)
    print('Language:', result.language)

if __name__ == '__main__':
    asyncio.run(test_greeting())
