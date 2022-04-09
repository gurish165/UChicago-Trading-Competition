import proto.utc_bot as pb
# case 1 config

# starting fair spot price
# enter each round!
START_BID = 550
START_ASK = 100

# NOT USED
START_FAIR = 330
FADE = 0.02
SLACK = 0.02

CONTRACTS = ["LBSJ","LBSM", "LBSQ", "LBSV", "LBSZ"]


def book_prices(book,update):
    print("--------------------------------")
    for contract in CONTRACTS:
        book = update.market_snapshot_msg.books[contract]
        print("bid\t\t","ask\t",contract)
        for i in range(max(len(book.bids),len(book.asks))):

            if i < len(book.bids):
                print(book.bids[i].px,book.bids[i].qty,end="")
            else:
                print("---","---",end="")

            print('\t',end='')

            if i < len(book.asks):
                print(book.asks[i].px,book.asks[i].qty)
            else:
                print("---","---",end="")
    print("--------------------------------")