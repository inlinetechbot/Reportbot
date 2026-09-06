import sys
from pyrogram import Client, filters
import asyncio
import json
from pyrogram.raw.functions.account import ReportPeer
from pyrogram.raw.types import *


def get_reason(text):
    if text == "Report for child abuse":
        return InputReportReasonChildAbuse()
    elif text == "Report for impersonation":
        return InputReportReasonFake()
    elif text == "Report for copyrighted content":
        return InputReportReasonCopyright()
    elif text == "Report an irrelevant geogroup":
        return InputReportReasonGeoIrrelevant()
    elif text == "Reason for Pornography":
        return InputReportReasonPornography()
    elif text == "Report an illegal durg":
        return InputReportReasonIllegalDrugs()
    elif text == "Report for offensive person detail":
        return InputReportReasonPersonalDetails()
    elif text == "Report for spam":
        return InputReportReasonSpam()
    elif text == "Report for Violence":
        return InputReportReasonViolence()
    else:
        return None


async def main(reason_text):
    try:
        config = json.load(open("config.json"))
    except FileNotFoundError:
        print("Error: config.json not found!")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON in config.json!")
        return

    resportreason = get_reason(reason_text)
    if resportreason is None:
        print(f"Error: Invalid reason provided: {reason_text}")
        return

    target = config.get('Target')
    if not target:
        print("Error: 'Target' not specified in config.json")
        return

    accounts = config.get("accounts", [])
    if not accounts:
        print("Error: No accounts found in config.json")
        return

    for account in accounts:
        string = account.get("Session_String")
        Name = account.get('OwnerName', 'Unknown')
        
        if not string:
            print(f"Error: No Session_String for account {Name}")
            continue
        
        async with Client(name="Session", session_string=string) as app:
            try:
                peer = await app.resolve_peer(target)
                
                # Handle different peer types
                if hasattr(peer, 'channel_id'):
                    input_peer = InputPeerChannel(
                        channel_id=peer.channel_id,
                        access_hash=peer.access_hash
                    )
                elif hasattr(peer, 'user_id'):
                    input_peer = InputPeerUser(
                        user_id=peer.user_id,
                        access_hash=peer.access_hash
                    )
                elif hasattr(peer, 'chat_id'):
                    input_peer = InputPeerChat(chat_id=peer.chat_id)
                else:
                    print(f"Error: Unknown peer type for {target}")
                    continue
                
                report_peer = ReportPeer(
                    peer=input_peer,
                    reason=resportreason,
                    message=reason_text
                )
                
                result = await app.invoke(report_peer)
                print(f"Successfully Reported by Account: {Name}")
                 
            except Exception as e:
                print(f"Error for account {Name}: {e}")
                print(f"Failed to report from: {Name}")
                
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python report.py <reason>")
        print("Available reasons:")
        print("  - Report for child abuse")
        print("  - Report for impersonation")
        print("  - Report for copyrighted content")
        print("  - Report an irrelevant geogroup")
        print("  - Reason for Pornography")
        print("  - Report an illegal durg")
        print("  - Report for offensive person detail")
        print("  - Report for spam")
        print("  - Report for Violence")
        sys.exit(1)

    input_string = sys.argv[1]
    asyncio.run(main(input_string))
