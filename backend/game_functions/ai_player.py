import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from backend.game_functions.tickets import Tickets
# Load environment variables from .env file
load_dotenv()

from backend.game_functions.player import Player


class AIPlayer(Player):
    def __init__(self, name, player_type, location):
        self.api_key = os.getenv("AI_API_KEY")
        self.api_version = '2024-08-01-preview'
        self.model_name ="gpt-4o"
        self.endpoint = os.getenv("AI_API_ENDPOINT")
        super().__init__(name, player_type, location, is_computer=1)

    def remaining_tickets(self):
        tickets = Tickets().player_tickets(self.id)
        return tickets

    def criminal_move(self,own_loc,det_loc):
        tickets = self.remaining_tickets()

        client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.endpoint
        )

        message = f"""
            Airports: BIKF, EBBR, EDDB, EFHK, EGLL, EIDW, ENGM, EPWA, ESSA, LBSF, LEMD, LFPG, LGAV, LHBP, LIRF, LKPR, LOWW, LPPT, LROP, LYBE, UKBB
            You: {own_loc}
            Detectives: {det_loc[0]}, {det_loc[1]}
            Tickets: {tickets['matkustajakone']}x Closest (C), {tickets['potkurikone']}x Near (N), {tickets['yksityiskone']}x Farthest (F)
            Goal: Avoid being caught by the detectives

            Important: Avoid airports close to the detectives. Do not fly directly to or near {det_loc[0]} or {det_loc[1]}. Choose an airport that is not near the detectives, even if it means selecting a farther airport.

            Only respond with one ICAO code and the ticket used (C, N, F), one at a time. For example:
            EPWA,C

            Do not list multiple answers. Prioritize staying far from the detectives.
        """

        chat_completion = client.chat.completions.create(
            model=self.model_name,  # model = "deployment_name".
            messages=[
                {"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": message}
            ]
        )

        response = chat_completion.choices[0].message.content
        split_response = response.split(',')
        ticket_id = 0
        if split_response == 'C':
            ticket_id = 1
        elif split_response == 'N':
            ticket_id = 2
        elif split_response == 'F':
            ticket_id = 3

        self.add_player_past_movement(self.location,ticket_id,self.id)
        self.update_location(split_response[0])

        return split_response[0]

    def detective_move(self, own_loc, criminal_loc, round):
        tickets = self.remaining_tickets()

        client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.endpoint
        )
        if round == 1:
            tickets['yksityiskone'] = 0
        message = f"""
                    Airports: BIKF, EBBR, EDDB, EFHK, EGLL, EIDW, ENGM, EPWA, ESSA, LBSF, LEMD, LFPG, LGAV, LHBP, LIRF, LKPR, LOWW, LPPT, LROP, LYBE, UKBB
                    You: {own_loc}
                    Criminals last known location: {criminal_loc}
                    Tickets: {tickets['matkustajakone']}x Closest (C), {tickets['potkurikone']}x Near (N), {tickets['yksityiskone']}x Farthest (F)
                    Goal: To catch the criminal by flying to the same airport 

                    Only respond with one ICAO code and the ticket used (C, N, F), one at a time. For example:
                    EPWA,C

                    Do not list multiple answers.
                """

        chat_completion = client.chat.completions.create(
            model=self.model_name,  # model = "deployment_name".
            messages=[
                {"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": message}
            ]
        )


        response = chat_completion.choices[0].message.content
        split_response = response.split(',')
        ticket_id=0
        if split_response == 'C':
            ticket_id = 1
        elif split_response == 'N':
            ticket_id = 2
        elif split_response == 'F':
            ticket_id = 3
        self.update_location(split_response[0])
        Tickets().delete_ticket(ticket_id, self.id)

        return split_response[0]

