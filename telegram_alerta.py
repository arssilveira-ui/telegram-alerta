# -*- coding: utf-8 -*-
import asyncio
import re
from telethon import TelegramClient, events

api_id = 33548874
api_hash = "acc2ca80bdf1d2b52ad2a1d1465aed78"

# palavras urgentes
palavras_urgentes = ["suma", "aireuropa", "air europa"]

# regex para detectar palavras
padrao_urgente = re.compile(r'(' + '|'.join(map(re.escape, palavras_urgentes)) + r')', re.IGNORECASE)

async def main():

    client = TelegramClient("session", api_id, api_hash)

    await client.start()

    print("Conectado ao Telegram")

    me = await client.get_me()

    print("Monitorando grupos...")

    @client.on(events.NewMessage)
    async def handler(event):

        # ignora suas próprias mensagens
        if event.sender_id == me.id:
            return

        texto = event.raw_text

        if not texto:
            return

        match = padrao_urgente.search(texto)

        if match:

            palavra_detectada = match.group(0)

            chat = await event.get_chat()
            sender = await event.get_sender()

            # identifica nome do grupo ou chat
            if hasattr(chat, "title"):
                nome_chat = chat.title
            else:
                nome_chat = chat.first_name

            mensagem_id = event.message.id

            # cria link da mensagem
            if getattr(chat, "username", None):
                link = f"https://t.me/{chat.username}/{mensagem_id}"
            else:
                link = "grupo privado"

            alerta = f"""
🚨🚨 ALERTA URGENTE 🚨🚨

Palavra: {palavra_detectada}
Grupo: {nome_chat}
Usuario: {sender.first_name}

Mensagem:
{texto}

Link:
{link}
"""

            print(alerta)

            await client.send_message("me", alerta)

    await client.run_until_disconnected()

asyncio.run(main())