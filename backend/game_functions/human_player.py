from backend.game_functions.airport import Airport
from backend.game_functions.player import Player
from backend.game_functions.tickets import Tickets

class HumanPlayer(Player):
    def __init__(self, name, player_type, location, database):
        super().__init__(name, player_type, location, database, is_computer=0)

    def player_move(self, name, round, player_ids, screen_names, selected_index):
        # Fetch data
        recommended_airports = get_recommended_airports(name)
        player_info = get_players_info(name)
        player_id = player_info.get('id')
        player_type = player_info.get('type')
        old_location = player_info.get('location')

        # Validate selected_index
        recommended_keys = list(recommended_airports.keys())
        if not (1 <= selected_index <= len(recommended_keys)):
            raise ValueError(f"Selected index {selected_index} is out of range. Valid range is 1 to {len(recommended_keys)}.")

        # Determine selected airport and process movement
        selected_key = recommended_keys[selected_index - 1]
        selected_airport = recommended_airports[selected_key]
        new_location = selected_key
        ticket_type = selected_airport['ticket_type']

        # Update location and manage tickets
        update_location(new_location, name)
        if player_type == 0:  # Human player
            add_player_past_movement(player_id, old_location, ticket_type)
        else:  # AI or detective
            Tickets.delete_ticket(ticket_type, player_id)

        # Return only the selected index
        return selected_index
