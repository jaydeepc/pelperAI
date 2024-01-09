import streamlit as st
from poker import Hand, Card, Combo
from pelper_ai import ai_suggestion

st.title('Pelper Calculator')

# Hand Input
player_hand_input = st.text_input("Enter your hand (e.g., 'Ah Kh')")

# Community Cards Input
community_cards_input = st.text_input(
    "Enter community cards (e.g., 'Qs Js Ts')")

# Parsing and Validating Inputs
try:
    if player_hand_input:
        try:
            player_hand = Combo(player_hand_input)
            st.write(f'Your Hand: {player_hand}')
            # Proceed with further calculations
        except ValueError as e:
            st.error(f'Invalid hand format: {e}')    
    
    community_cards = [Card(card) for card in community_cards_input.split()]
    st.write(
        f'Community Cards: {", ".join(str(card) for card in community_cards)}')

    # Your logic for calculating odds and making decisions goes here

except ValueError as e:
    st.error(f'Invalid input: {e}')

pot_size = st.text_input("Enter pot size")
raise_amount = st.text_input("Enter raise amount")
my_position = st.text_input("Enter your position")
blind_size = st.text_input("Enter blind size")
current_bank_roll = st.text_input("Enter your current bank roll")

if st.button('AI Suggest'):
    st.write("Thinking . . . ")
    st.write(ai_suggestion(player_hand_input, community_cards_input, pot_size, raise_amount, my_position, blind_size, current_bank_roll))