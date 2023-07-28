import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta

def get_not_closed_or_resolved_tickets():
    url = "https://azion.freshdesk.com/api/v2/tickets"
  #AQUI VAI A CHAVE DA API
    auth = HTTPBasicAuth("FRESHDESK_API_KEY_HERE", "X")

    six_months_ago = datetime.now() - timedelta(days=6*30)
    six_months_ago_str = six_months_ago.strftime("%Y-%m-%d")
    params = {'updated_since': six_months_ago_str, 'per_page': 100}

    not_closed_or_resolved_tickets = []

    page = 1
    while True:
        params['page'] = page
        response = requests.get(url, auth=auth, params=params)

        if response.status_code != 200:
            raise Exception("Failed to get tickets: status code {}".format(response.status_code))

        tickets = response.json()
        if not tickets:
            break

        for ticket in tickets:
            if ticket['status'] not in [5, 4] and ticket['type'] == "Question":
                ticket_data = {'id': ticket['id'], 'tags': ticket['tags']}
                not_closed_or_resolved_tickets.append(ticket_data)
        
        page += 1

    return not_closed_or_resolved_tickets

tickets = get_not_closed_or_resolved_tickets()
print(tickets)
