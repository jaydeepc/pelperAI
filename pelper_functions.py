from poker import Card, Rank

# Function to count outs for a flush draw


def count_outs_for_flush_draw(hand, community_cards):
    suits = [card.suit for card in hand + community_cards]
    for suit in set(suits):
        if suits.count(suit) == 4:  # Flush draw
            return 9  # 9 outs for a flush draw
    return 0

# Function to count outs for a straight draw


def count_outs_for_straight_draw(hand, community_cards):
    all_ranks = [card.rank for card in hand + community_cards]
    rank_values = [Rank(r).value for r in all_ranks]

    # Simplified logic for gutshot straight draw
    if Rank('Q').value not in rank_values:
        if (Rank('J').value in rank_values and Rank('T').value in rank_values) or \
           (Rank('A').value in rank_values and Rank('K').value in rank_values):
            return 4  # Four Queens in the deck
    return 0

# Function to count total outs for draws


def count_outs_for_draws(hand, community_cards):
    return count_outs_for_flush_draw(hand, community_cards) + count_outs_for_straight_draw(hand, community_cards)

# Function to calculate equity using the "4 and 2" rule


def calculate_equity_4_and_2_method(hand, community_cards):
    outs = count_outs_for_draws(hand, community_cards)
    if len(community_cards) == 3:  # After the flop
        return min(100, outs * 4)  # Cap at 100%
    elif len(community_cards) == 4:  # After the turn
        return min(100, outs * 2)  # Cap at 100%
    else:
        return 0  # Before the flop or after the river, the rule doesn't apply

# Function to make a decision (call, fold, or raise)


def make_decision(player_hand, community_cards, current_pot, raise_amount):
    equity = calculate_equity_4_and_2_method(player_hand, community_cards)
    pot_odds = raise_amount / (current_pot + raise_amount)
    pot_after_call = current_pot + 2 * raise_amount
    ev = (equity / 100) * pot_after_call - (1 - equity / 100) * raise_amount

    print(f'Equity: {equity}')
    print(f'Pot Odds: {pot_odds}')
    print(f'EV: {ev}')

    if ev > 0:
        if equity > pot_odds:
            return "Raise"
        else:
            return "Call"
    else:
        return "Fold"


# Example usage
player_hand = [Card('Ah'), Card('Kh')]
flop_cards = [Card('5h'), Card('Js'), Card('2h')]
current_pot = 1000
raise_amount = 500

decision = make_decision(player_hand, flop_cards, current_pot, raise_amount)
print(f'Decision: {decision}')
