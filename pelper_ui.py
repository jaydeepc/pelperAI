import streamlit as st
from poker import Combo, Card
from pelper_ai import ai_suggestion
import os

st.title('Pelper Calculator')
st.text("- Created by Jaydeep Chakrabarty")
# Define card options
card_options = [f'{rank}{suit}' for rank in ['A', 'K', 'Q', 'J', 'T',
                                             '9', '8', '7', '6', '5', '4', '3', '2'] for suit in ['s', 'h', 'd', 'c']]

# Function to get image path for a card


def get_card_image_path(card):
    rank, suit = card[:-1], card[-1]
    suit_name = {'s': 'spades', 'h': 'hearts', 'd': 'diamonds', 'c': 'clubs'}

    # Mapping for special card names
    special_names = {'A': 'ace', 'K': 'king',
                     'Q': 'queen', 'J': 'jack', 'T': '10'}
    # Use special name if exists, else use rank directly
    rank_name = special_names.get(rank, rank)

    return os.path.join('assets', 'images', 'cards', f'{rank_name}_of_{suit_name[suit]}.png')


# Hand Selection using multiselect
selected_hand_cards = st.multiselect(
    "Select Your Hand (2 cards):", card_options, key='hand')

# Display selected hand cards as images
if len(selected_hand_cards) == 2:
    cols = st.columns(2)
    for idx, card in enumerate(selected_hand_cards):
        cols[idx].image(get_card_image_path(card), width=100)
    # Concatenate the two card strings
    player_hand_input = ''.join(selected_hand_cards)
    player_hand = Combo(player_hand_input)
else:
    st.warning("Please select exactly 2 cards for your hand.")

# Community Cards Selection using multiselect
selected_community_cards = st.multiselect(
    "Select Community Cards (up to 5 cards):", card_options, key='community')

# Display selected community cards as images
if selected_community_cards:
    cols = st.columns(len(selected_community_cards))
    for idx, card in enumerate(selected_community_cards):
        cols[idx].image(get_card_image_path(card), width=100)
    community_cards_input = ' '.join(selected_community_cards)
    community_cards = [Card(card) for card in community_cards_input.split()]
else:
    community_cards = []

# Additional inputs for pot size, raise amount, etc.
pot_size = st.text_input("Enter pot size")
raise_amount = st.text_input("Enter raise amount")
position_options = ["SB", "BB", "UTG", "MP", "CO", "BTN"]
my_position = st.selectbox("Select your position", position_options)

# Display image of position
position_image_path = 'assets/images/position.jpeg'
st.image(position_image_path, use_column_width=True)

# ... remaining code ...

blind_size_options = ["0.5/1", "1/2", "5/10", "10/20", "25/100"]
blind_size = st.selectbox("Select blind size", blind_size_options)
current_bank_roll = st.text_input("Enter your current bank roll")

# AI Suggestion Button
if st.button('AI Suggest'):
    st.write("Thinking . . . ")
    if player_hand_input and community_cards_input:
        player_hand = Combo(player_hand_input)
        community_cards = [Card(card)
                           for card in community_cards_input.split()]
        suggestion = ai_suggestion(player_hand, community_cards, pot_size,
                                   raise_amount, my_position, blind_size, current_bank_roll)
        st.write(suggestion)
    else:
        st.error("Please select your hand and community cards.")
