import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from backend.game_functions.tickets import Tickets
from backend.game_functions.player import Player

# Load environment variables from .env file
load_dotenv()


# AI Player class
class AIPlayer(Player):
    def __init__(self, name, player_type, location):
        self.api_key = os.getenv("AI_API_KEY")
        self.api_version = '2024-08-01-preview'
        self.model_name = "gpt-4o"
        self.endpoint = os.getenv("AI_API_ENDPOINT")
        super().__init__(name, player_type, location, is_computer=1)

    def remaining_tickets(self):
        tickets = Tickets().player_tickets(self.id)
        return tickets

    def criminal_move(self, own_loc, det_loc):
        tickets = self.remaining_tickets()

        client = AzureOpenAI(api_key=self.api_key, api_version=self.api_version, azure_endpoint=self.endpoint)

        ticket_info = []
        if 'matkustajakone' in tickets:
            ticket_info.append(f"{tickets['matkustajakone']}x Closest (C)")
        if 'potkurikone' in tickets:
            ticket_info.append(f"{tickets['potkurikone']}x Near (N)")
        if 'yksityiskone' in tickets:
            ticket_info.append(f"{tickets['yksityiskone']}x Farthest (F)")

        ticket_info_str = ', '.join(ticket_info)

        message = f""" Possible airports: BIKF, EBBR, EDDB, EFHK, EGLL, EIDW, ENGM, EPWA, ESSA, LBSF, LEMD, LFPG, 
        LGAV, LHBP, LIRF, LKPR, LOWW, LPPT, LROP, LYBE, UKBB You: {own_loc}
            Detectives: {det_loc[0]}, {det_loc[1]}
            Tickets: {ticket_info_str}
            Goal: Avoid being caught by the detectives

            Important: Avoid airports close to the detectives. Do not fly directly to or near {det_loc[0]} or {det_loc[1]}. Choose an airport that is not near the detectives, even if it means selecting a farther airport.

            Important: You must choose only one ICAO code from the possible airports listed above and the ticket used 
            (C, N, F). For example: EPWA,C

            Do not list multiple answers. Prioritize staying far from the detectives.
        """

        max_retries = 3
        for _ in range(max_retries):
            chat_completion = client.chat.completions.create(model=self.model_name, messages=[
                {"role": "system", "content": "You are an AI assistant."}, {"role": "user", "content": message}])

            response = chat_completion.choices[0].message.content.strip()
            split_response = response.split(',')
            ticket = split_response[1]
            filtered = filter(str.isalpha, ticket)
            filtered_t = "".join(filtered)
            if len(split_response) == 2 and split_response[0] in ["BIKF", "EBBR", "EDDB", "EFHK", "EGLL", "EIDW",
                                                                  "ENGM", "EPWA", "ESSA", "LBSF", "LEMD", "LFPG",
                                                                  "LGAV", "LHBP", "LIRF", "LKPR", "LOWW", "LPPT",
                                                                  "LROP", "LYBE", "UKBB"] and filtered_t in ["C", "N", "F"]:
                ticket_id = {"C": 1, "N": 2, "F": 3}[filtered_t]
                self.add_player_past_movement(self.location, ticket_id, self.id)
                self.update_location(split_response[0])
                return split_response[0]
            print(f"Invalid response format or values: {response}. Retrying...")

        raise ValueError("Failed to get a valid response after multiple attempts")

    # Method to handle detective movement
    def detective_move(self, own_loc, criminal_id, round):
        tickets = self.remaining_tickets()
        criminal_loc = self.get_criminal_movements(criminal_id)
        client = AzureOpenAI(api_key=self.api_key, api_version=self.api_version, azure_endpoint=self.endpoint)
        if round == 1:
            tickets['yksityiskone'] = 0

        ticket_info = []
        if 'matkustajakone' in tickets:
            ticket_info.append(f"{tickets['matkustajakone']}x Closest (C)")
        if 'potkurikone' in tickets:
            ticket_info.append(f"{tickets['potkurikone']}x Near (N)")
        if 'yksityiskone' in tickets:
            ticket_info.append(f"{tickets['yksityiskone']}x Farthest (F)")

        ticket_info_str = ', '.join(ticket_info)

        message = f""" Possible airports: BIKF, EBBR, EDDB, EFHK, EGLL, EIDW, ENGM, EPWA, ESSA, LBSF, LEMD, LFPG, 
        LGAV, LHBP, LIRF, LKPR, LOWW, LPPT, LROP, LYBE, UKBB You: {own_loc}
                    Criminals last known location: {criminal_loc}
                    Tickets: {ticket_info_str}
                    Goal: To catch the criminal by flying to the same airport 
                    
                    Important: You must choose only one ICAO code from the possible airports listed above and the 
                    ticket used (C, N, F). For example: EPWA,C

                    Do not list multiple answers.
                """

        max_retries = 3
        for _ in range(max_retries):
            chat_completion = client.chat.completions.create(model=self.model_name, messages=[
                {"role": "system", "content": "You are an AI assistant."}, {"role": "user", "content": message}])

            response = chat_completion.choices[0].message.content.strip()
            split_response = response.split(',')
            ticket = split_response[1]
            filtered = filter(str.isalpha, ticket)
            filtered_t = "".join(filtered)
            if len(split_response) == 2 and split_response[0] in ["BIKF", "EBBR", "EDDB", "EFHK", "EGLL", "EIDW",
                                                                  "ENGM", "EPWA", "ESSA", "LBSF", "LEMD", "LFPG",
                                                                  "LGAV", "LHBP", "LIRF", "LKPR", "LOWW", "LPPT",
                                                                  "LROP", "LYBE", "UKBB"] and filtered_t in ["C", "N",
                                                                                                             "F"]:
                ticket_id = {"C": 1, "N": 2, "F": 3}[filtered_t]
                self.update_location(split_response[0])
                Tickets().delete_ticket(ticket_id, self.id)
                print(response)
                return split_response[0]
            print(f"Invalid response format or values: {response}. Retrying...")

        raise ValueError("Failed to get a valid response after multiple attempts")
