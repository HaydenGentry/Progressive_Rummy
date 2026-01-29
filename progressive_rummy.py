# v1.0.2
# v1 = number of files (only file is for game logic right now)
# v1.0 = number of rounds completed (working on first round, not complete yet)
# v1.0.2 = number of commits since previous round complete milestone

import random

two_full_decks = ["A-S", "2-S", "3-S", "4-S", "5-S", "6-S", "7-S", "8-S", "9-S", "10-S", "J-S", "Q-S", "K-S",
                  "A-S", "2-S", "3-S", "4-S", "5-S", "6-S", "7-S", "8-S", "9-S", "10-S", "J-S", "Q-S", "K-S",
                  "A-D", "2-D", "3-D", "4-D", "5-D", "6-D", "7-D", "8-D", "9-D", "10-D", "J-D", "Q-D", "K-D",
                  "A-D", "2-D", "3-D", "4-D", "5-D", "6-D", "7-D", "8-D", "9-D", "10-D", "J-D", "Q-D", "K-D",
                  "A-C", "2-C", "3-C", "4-C", "5-C", "6-C", "7-C", "8-C", "9-C", "10-C", "J-C", "Q-C", "K-C",
                  "A-C", "2-C", "3-C", "4-C", "5-C", "6-C", "7-C", "8-C", "9-C", "10-C", "J-C", "Q-C", "K-C",
                  "A-H", "2-H", "3-H", "4-H", "5-H", "6-H", "7-H", "8-H", "9-H", "10-H", "J-H", "Q-H", "K-H",
                  "A-H", "2-H", "3-H", "4-H", "5-H", "6-H", "7-H", "8-H", "9-H", "10-H", "J-H", "Q-H", "K-H",
                  "JOKER", "JOKER", "JOKER", "JOKER"]
players_hands = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}
num_players = 2

# Progressive Rummy Rounds:
# Round 1. 2 sets
# Round 2. 1 set and 1 run
# Round 3. 2 runs
# Round 4. 3 sets
# Round 5. 2 sets, 1 run, and no discard


# Every player is dealt 9 cards at the beginning of each round
def shuffle_and_deal(decks):
    random.shuffle(decks)
    # debugging
    print(decks)
    for player in range(num_players):
        for card in range(9):
            players_hands[player].append(decks[player + (num_players * card)])
    # debugging
        print("Player " + str(player + 1) + ": " + str(players_hands[player]))
    print("First Card: " + str(decks[num_players * 9]))


# Return True if value is a number card. Return False if value is not a number card
def a_number_card(card):
    # Joker
    if len(card) == 5:
        return False
    else:
        # Number card
        try:
            int(card[0])
            return True
        # Face card
        except ValueError:
            return False


# Return the value and suit of a card. If a joker, only return the value
def value_and_suit(card):
    sep = "-"
    value_arr, suit_arr = [], []
    # Joker return arr of length 1 (no suit)
    if len(card) == 5:
        value_arr.append("JOKER")
    else:
        value, dash, suit = card.partition(sep)
        # Number card returns int value and suit arr of length 2
        if a_number_card(value):
            value_arr.append(int(value))
            suit_arr.append(suit)
        # Face card returns face value and suit arr of length 2
        else:
            value_arr.append(value)
            suit_arr.append(suit)
    # debugging
    # print(value_arr + suit_arr)
    return value_arr + suit_arr


# Return the count of jokers in a players hand
def joker_count(p_hand):
    jokers = 0
    for card in p_hand:
        if value_and_suit(card)[0] == "JOKER":
            jokers += 1
    # debugging
    # print("1 jokers: " + str(p_hand) + str(joker_count))
    return jokers


# Return the players hand sorted only by the value of the cards in ascending order
def sort_values(p_hand):
    # 1. Naive sort of all players hands
    p_hand.sort()
    # debugging
    # print("1 pre: " + str(p_hand))
    # 2. Split hand into number and face cards
    number_cards, face_cards = [], []
    for card in p_hand:
        if a_number_card(card):
            number_cards.append(card)
        else:
            face_cards.append(card)
    # debugging
    # print("2 nums: " + str(number_cards))
    # print("2 faces: " + str(face_cards))
    # 3. Re-sort number cards with 10 in the back (currently in front)
    i = 0
    for card in number_cards:
        if value_and_suit(card)[0] == 10:
            i += 1
    ten_cards = number_cards[:i]
    number_cards = number_cards[i:] + ten_cards
    # debugging
    # print("3 nums: " + str(number_cards))
    # 4. Re-sort face cards. Use switch case J-Q-K-A-JOK (push A and JOK to the back)
    j_cards, q_cards, k_cards, a_cards, jok_cards = [], [], [], [], []
    for card in face_cards:
        match value_and_suit(card)[0]:
            case "J":
                j_cards.append(card)
            case "Q":
                q_cards.append(card)
            case "K":
                k_cards.append(card)
            case "A":
                a_cards.append(card)
            case "JOKER":
                jok_cards.append(card)
    face_cards = j_cards + q_cards + k_cards + a_cards + jok_cards
    # debugging
    # print("4 faces: " + str(face_cards))
    # 5. Combine lists and print results
    p_hand = number_cards + face_cards
    # debugging
    # print("5 post: " + str(p_hand))
    return p_hand


# H-C-D-S
# Sort into suits
def sort_suits(p_hand):
    h_suits, c_suits, d_suits, s_suits, jok_cards = [],  [],  [], [], []
    value_sorted = sort_values(p_hand)
    # debugging
    # print("Value sorted: " + str(value_sorted))
    for card in value_sorted:
        if len(value_and_suit(card)) == 1:
            jok_cards.append(card)
        else:
            match value_and_suit(card)[-1]:
                case "H":
                    h_suits.append(card)
                case "C":
                    c_suits.append(card)
                case "D":
                    d_suits.append(card)
                case "S":
                    s_suits.append(card)
    p_hand = h_suits + c_suits + d_suits + s_suits + jok_cards
    # debugging
    print("Suits: " + str(p_hand))


# Third order sort
# Split hand into non/pairs and sets, and pairs and sets
# Recombine with non/pairs and sets in descending order then pairs and sets in ascending order
def first_round_two_sets(p_hand):
    # 1. Sort values in hand
    value_sorted = sort_values(p_hand)
    # debugging
    # print("1. Sort Values: " + str(value_sorted))
    # 2. Count JOK in hand
    jokers = joker_count(p_hand)
    # debugging
    # print("2. Jokers: " + str(p_hand) + str(jokers))
    # 3. Count pairs and sets in hand
    value_dict = {2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [],
                  "J": [], "Q": [], "K": [], "A": [], "JOKER": []}
    value_dict_lens = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0,
                       "J": 0, "Q": 0, "K": 0, "A": 0, "JOKER": 0}
    pairs = []
    pair_count = 0
    sets = []
    set_count = 0
    # 3. Put cards in a dictionary of lists for each value as a key
    for card in value_sorted:
        value_dict[value_and_suit(card)[0]].append(card)
    # debugging
    # print("3. Dict: " + str(value_dict))
    # 4. Count pairs/sets and record cards in pairs/sets
    for key in value_dict:
        value_dict_lens[key] = len(value_dict[key])
        if len(value_dict[key]) == 2:
            pairs.append(key)
            pair_count += 1
        if len(value_dict[key]) >= 3:
            sets.append(key)
            set_count += 1
    # debugging
    # print("3. Value len: " + str(value_dict_lens))
    # print("4. Pairs- " + str(pair_count) + ": " + str(pairs) +
    #       ", Sets- " + str(set_count) + ": " + str(sets) +
    #       ", Jokers- " + str(jokers))
    # Order of hand
    # 5. Non pairs/sets in descending order + pairs in ascending order + sets in ascending order + jokers
    sorted_hand = []
    for key in reversed(value_dict):
        if (value_dict_lens[key] == 1) and not (key == "JOKER"):
            sorted_hand.append(value_dict[key])
    if pair_count >= 1:
        for card in pairs:
            sorted_hand.append(value_dict[card])
    if set_count >= 1:
        for card in sets:
            sorted_hand.append(value_dict[card])
    if jokers >= 1:
        sorted_hand.append(value_dict["JOKER"])
    # Turn a list of lists into one list
    flat_sorted_hand = [element for sublist in sorted_hand for element in sublist]
    # debugging
    print("5. Sort no joker placement: " + str(flat_sorted_hand))
    return flat_sorted_hand
    # Third order sort
    # LD-NP = Lay Down Not Possible (0), LD-P = Lay Down Possible(1+), BOL = Back of list
    # Cannot lay down a set or run with more JOKs than value cards, or consecutive JOKs in a run

    # If LD-P > 1, check is way to find the most valuable move
    # 2 sets/1 pair/1 JOK ???
    # 4-4, J-J, Q-Q: buy 4 from discard and draw JOK
    # 4-4-4, J-J, Q-Q: JOK, on turn draw J
    # 4-4-4, J-J-J, Q-Q, JOK: best move is LD: J-J-J, Q-Q-JOK (1 set/1 pair/1 JOK > 2 sets/1 JOK).

    # 1 set/2+ pairs/2 JOK ???
    # 4-4, 7-7, J-J, Q-Q, JOK: buy 4 from discard and draw JOK
    # 4-4-4, 7-7, J-J, Q-Q, JOK, JOK: on turn draw 4
    # 4-4-4-4, 7-7, J-J, Q-Q, JOK, JOK:  best move is LD: J-J-JOK, Q-Q-JOK (2 sets/2 JOK > 1 set/1 run/2 JOK).

    # If no JOK
    # 2+ sets/ n/a of pairs, LD-P
    # Else, LD-NP

    # If one JOK
    # 0 pairs. LD-NP. JOK BOL
    # 1 pair. LD-NP JOK BOL
    # 2+ pairs. LD-NP. JOK BOL
    # 1 set/0 pairs. LD-NP. JOK BOL
    # 1 set/1 pair. LD-P = 1. Add JOK to the of end of pair
    # 1 set/2+ pairs. LD-P = # of pairs. Add JOK to the end of the highest value pair
    # 2+ sets/0 pairs. LD-P = 1. Add JOK to the end of the highest value set
    # 2+ sets/1 pair. LD-P = 2. See below
    # 2+ sets/2+ pair. See below
        # If 2nd highest value set > highest value pair. Add JOK to the end of the highest value set (7-7-7 > Q-Q)
        # Else. Add JOK to the end of the pair (4-4-4 < Q-Q)

    # If two JOKs
    # 0 pairs. LD-NP. JOKs BOL
    # 1 pair. LD-NP. JOKs BOL
    # 2+ pairs. LD-P. Add a JOK to the end of the two highest value pairs
    # 1 set/0 pairs. LD-NP. JOK BOL
    # 1 set/1 pair. LD-P. Add a JOK to the end of set and a JOK to the end of pair
    # 1 set/2+ pairs. LD-P. Add a JOK to the end of set and a JOK to the end of the highest value pair ???
    # 2+ sets/0 pairs. LD-P = 1. Add a JOK to the end of the highest value set
    # 2+ sets/1 pair. LD-P = 2. See below
    # 2+ sets/2+ pair. See below

    # If three or four JOKs
    # Same LD-NP/LD-P logic as if two JOKs
    # Same JOK placement for first two JOKs as if two JOKs
    # 2+ pairs. 3 on the highest. 4 on the second highest
    # 1 set/1 pair. 3 on the set. 4 on the pair
    # 1 set/2+ pairs.

    # Fourth round - three sets
    # If a JOK and two sets and no pairs, JOK back of the list
    # If a JOK and two sets and one pair, add JOK to the of end of pair
    # If a JOK and two sets and two or more pairs, add JOK to the end of the pair of the highest value


# Start point
shuffle_and_deal(two_full_decks)
for player, hand in players_hands.items():
    if player == num_players:
        break
    # debugging
    print(f"First sort - Player {player + 1}: {first_round_two_sets(hand)}")

# debugging
test_hand1 = ['9-D', '7-D', '10-H', '9-H', 'J-D', '8-C', 'J-S', '3-H', 'JOKER', "10-D", "9-S"]
first_round_two_sets(test_hand1)

# sort_values(test_hand1)
# sort_suits(test_hand1)

# Fourth round - three sets
# If a JOK and two sets and no pairs, JOK back of the list
# If a JOK and two sets and one pair, add JOK to the of end of pair
# If a JOK and two sets and two or more pairs, add JOK to the end of the pair of the highest value

