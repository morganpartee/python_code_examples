from random import shuffle


class Deck:
    def __init__(self, num_decks=6):
        self.cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 11] * 4 * num_decks
        shuffle(self.cards)

    def get_card(self) -> int:
        return self.cards.pop()


class UserHand:
    def __init__(self):
        self.hand = []
        self.bust = False
        self.sum = 0

    def eval_hand(self) -> bool:
        if sum(self.hand) < 21:
            return True
        if 11 in self.hand:
            return sum(i for i in self.hand if i != 11) + self.hand.count(11) > 21
        self.bust = True
        return False

    def hit(self, deck: Deck) -> None:
        card = deck.getCard()
        self.sum += card
        self.hand.append(card)


class DealerHand:
    def __init__(self):
        self.hand = []
        self.bust = False
        self.sum = 0

    def eval_hand(self) -> bool:
        if sum(self.hand) < 21:
            return True
        if 11 in self.hand:
            return sum(i for i in self.hand if i != 11) + self.hand.count(11) > 21
        return False

    def hit(self, deck: Deck) -> None:
        card = deck.getCard()
        self.sum += card
        self.hand.append(card)

    def deal_self(self, deck: Deck) -> None:
        while True:
            val = sum(self.hand)
            if val < 17 or (val == 17 and 11 in self.hand):  # dealer hits on soft 17
                self.hit(deck)
                continue
            return


class BlackJack:
    def __init__(self, num_decks, num_players):
        self.decks = Deck(num_decks)
        self.dealer = DealerHand()
        self.players = [UserHand() for _ in range(num_players)]

    def play(self):
        # This is purely an example, input is not practical for real play obviously lol
        for i, player in enumerate(self.players):
            while True:
                strin = input(
                    f"Player {i + 1}, you have {player.hand} in your hand. Hit or stay? "
                ).lower()
                if strin == "hit":
                    player.hit(self.decks)
                else:
                    break
                if player.evalHand() is False:
                    print("Bust!")
                    break
        self.dealer.deal_self(self.decks)
        print(f"Dealer hand is {self.dealer.hand}\n")
        if self.dealer.evalHand() is False:
            return {
                "Winners": [
                    i for i, player in enumerate(self.players) if not player.bust
                ],
                "Losers": [i for i, player in enumerate(self.players) if player.bust],
            }
        return {
            "Winners": [
                i
                for i, player in enumerate(self.players)
                if not player.bust and player.sum > self.dealer.sum
            ],
            "Losers": [
                i
                for i, player in enumerate(self.players)
                if player.bust or player.sum <= self.dealer.sum
            ],
        }


bj = BlackJack(6, 2)
print(bj.play())
