import enum
import random
from collections import Counter


class PlayingCard():
    def __init__(self, suit):
        self.suit = suit

    def __lt__(self, other):
        return (self.get_value(), self.suit) < (other.get_value(), other.suit)

    def __eq__(self, other):
        return (self.get_value(), self.suit) == (other.get_value(), other.suit)

class Suit(enum.IntEnum):
    Hearts = 0
    Spades = 1
    Clubs = 2
    Diamonds = 3

class NumberedCard(PlayingCard):
    def __init__(self, value, suit):
        super().__init__(suit)
        self.value = value

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit

class JackCard(PlayingCard):
    def __init__(self, suit):
        super().__init__( suit)
        self.value = 11

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value

class QueenCard(PlayingCard):
    def __init__(self, suit):
        super().__init__(suit)
        self.value = 12
    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value

class KingCard(PlayingCard):
    def __init__(self, suit):
        super().__init__(suit)
        self.value = 13

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value

class AceCard(PlayingCard):
    def __init__(self, suit):
        super().__init__(suit)
        self.value = 1

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value

class StandardDeck:
    def __init__(self):
        self.cards = []
        for s in Suit:
            for i in [2,11]:
                self.cards.append(NumberedCard(value=i,suit=s))
            self.cards.append(JackCard(suit=s))
            self.cards.append(QueenCard(suit=s))
            self.cards.append(KingCard(suit=s))
            self.cards.append(AceCard(suit=s))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def sort(self):
        self.cards.sort()

    def drop_cards(self, index):
        for i in sorted(index, reverse=True):
            del self.cards[i]

    def best_poker_hand(self, cards=[]):
        return PokerHand(cards + self.cards)

class Pokerhands(enum.IntEnum):
    High_Card = 0
    One_Pair = 1
    Two_Pair = 2
    Three_of_a_kind = 3
    Straight = 4
    Flush = 5
    Full_House = 6
    Four_of_a_Kind = 7
    Straight_Flush = 8
    Royal_Flush = 9

class PokerHand:
    def __init__(self, cards):
        self.cards = cards
        pokerhands = [check_straight_flush, check_straight_flush, check_four_of_a_kind, check_full_house, check_flush,
                      check_straight, check_three_of_a_kind, check_two_pairs, check_one_pairs, check_high_card]

        for hand in pokerhands:
            self.pokerhand = hand(cards)
            if self.pokerhand:
                break

    def __lt__(self, other):
        return (self.pokerhand < other.pokerhand)

    def __eq__(self, other):
        return (self.pokerhand == other.pokerhand)

def check_straight_flush(cards):
        """
        Checks for the best straight flush in a list of cards (may be more than just 5)

        :param self: A list of playing cards.
        :return: None if no straight flush is found, else the value of the top card.
        """
        vals = [(c.get_value(), c.suit) for c in cards] \
               + [(1, c.suit) for c in cards if c.get_value() == 14]  # Add the aces!
        for c in reversed(cards):  # Starting point (high card)
            # Check if we have the value - k in the set of cards:
            found_straight = True
            for k in range(1, 5):
                if (c.get_value() - k, c.suit) not in vals:
                    found_straight = False
                    break
            if found_straight:
                straight_flush = c.get_value()
                return (Pokerhands.Straight_Flush.value, straight_flush), sorted(cards, reverse=True)

def check_four_of_a_kind(cards):
    """
    Checks for four of a kind in a list of cards

    :param cards: A list of playing cards.
    :return: None if no for of a kind is found, else the value of the top card.
    """
    value_count = Counter()

    for c in cards:
        value_count[c.get_value()] += 1
    fours = [v[0] for v in value_count.items() if v[1] == 4]
    fours.sort(reverse=True)

    if fours:
        return (Pokerhands.Four_of_a_Kind, fours), sorted(cards, reverse=True)

def check_full_house(cards):

    value_count = Counter()
    for c in cards:
        value_count[c.get_value()] += 1
    # Find the card ranks that have at least three of a kind
    threes = [v[0] for v in value_count.items() if v[1] >= 3]
    threes.sort()
    if not threes: # If no threes found get the f out
        return
    # Find the card ranks that have at least a pair
    twos = [v[0] for v in value_count.items() if v[1] >= 2]
    twos.sort()
    if not twos: # If no pairs found get the f out
        return

    # Threes are dominant in full house, lets check that value first:
    for three in reversed(threes):
        for two in reversed(twos):
            if two != three:
                return (Pokerhands.Full_House.value, three, two), sorted(cards,reverse=True)

def check_flush(cards):
    values = [(c.get_value(), c.suit) for c in cards] \
           + [(1, c.suit) for c in cards if c.get_value() == 14]  # Add the aces!
    values.sort(reverse=True)
    flush_cards = []
    value_count = Counter()
    for c in sorted(cards, reverse=True):
        value_count[c.suit] += 1
        flush = [v[0] for v in value_count.items() if v[1] == 5]

    if not flush:
        return

    for a,c in enumerate(sorted(cards,reverse=True)):
        if values[a][1] == flush[0]:

            flush_cards.append(c)
    for i in range(len(flush_cards)):
        pass
    return (Pokerhands.Flush.value, flush_cards[0:5]), sorted(cards, reverse=True)

def check_straight(cards):
    scards = sorted(cards,reverse=True)
    values = [c.get_value() for c in cards] \
            + [1 for c in cards if c.get_value() == 14]  # Add the aces!
    for c in reversed(cards):
        found_straight = True
        for k in range(1, 5):
            if (c.get_value() - k) not in values:
                found_straight = False
                break
        if found_straight:
            straight = c.get_value()
            return (Pokerhands.Straight.value, straight), scards

def check_three_of_a_kind(cards):
    value_count = Counter()

    for c in cards:
        value_count[c.get_value()] += 1
    threes = [v[0] for v in value_count.items() if v[1] == 3]
    threes.sort(reverse=True)
    if threes:
        return (Pokerhands.Three_of_a_kind, threes[0]), sorted(cards, reverse=True)

def check_two_pairs(cards):
    value_count = Counter()

    for c in cards:
        value_count[c.get_value()] +=1
    pairs = [v[0] for v in value_count.items() if v[1] == 2]
    pairs.sort(reverse=True)

    if len(pairs) >=2:
        return (Pokerhands.Two_Pair.value, pairs[0:2]), sorted(cards, reverse=True)

def check_one_pairs(cards):
    value_count = Counter()

    for c in cards:
        value_count[c.get_value()] += 1
    pairs = [v[0] for v in value_count.items() if v[1] == 2]

    if pairs:
        return (Pokerhands.One_Pair.value, pairs), sorted(cards, reverse=True)

def check_high_card(cards):
    card = [(c.get_value(), c.suit.value) for c in cards]
    card.sort(reverse=True)
    return card








