import requests

# Get all open markets for the KXHIGHNY series
markets_url = "https://external-api.kalshi.com/trade-api/v2/markets?series_ticker=KXHIGHNY&status=open"
markets_response = requests.get(markets_url)
markets_data = markets_response.json()

print("\nActive markets in KXHIGHNY series:")
for market in markets_data["markets"]:
    print(f"- {market['ticker']}: {market['title']}")
    print(f"  Event: {market['event_ticker']}")
    print(f"  Yes Price: ${market['yes_bid_dollars']} | Volume: {market['volume_fp']}")
    print()

# Get details for a specific event if you have its ticker
if markets_data["markets"]:
    # Let's get details for the first market's event
    event_ticker = markets_data["markets"][0]["event_ticker"]
    event_url = f"https://external-api.kalshi.com/trade-api/v2/events/{event_ticker}"
    event_response = requests.get(event_url)
    event_data = event_response.json()

    print("Event Details:")
    print(f"Title: {event_data['event']['title']}")
    print(f"Category: {event_data['event']['category']}")
