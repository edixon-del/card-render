import curses
import random
import locale

locale.setlocale(locale.LC_ALL, '')

RANKS = ("A","2","3","4","5","6","7","8","9","T","J","Q","K")
SUITS = ("♣","♦","♥","♠")
RED_SUITS = {"♦","♥"}

CARD_W, CARD_H = 7, 6

def build_deck():
    return [(r, s) for s in SUITS for r in RANKS]

def init_colors():
    curses.start_color()
    try:
        curses.use_default_colors()
    except curses.error:
        pass
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_RED,   curses.COLOR_WHITE)
    return {
        "CARD_BG": curses.color_pair(1),
        "BLACK_ON_WHITE": curses.color_pair(2),
        "RED_ON_WHITE": curses.color_pair(3),
    }

def safe_add(win, y, x, s, attr=0):
    try:
        win.addstr(y, x, s, attr)
    except curses.error:
        pass

def draw_card(stdscr, y0, x0, rank, suit, colors):
    try:
        win = stdscr.subwin(CARD_H, CARD_W, y0, x0)
    except curses.error:
        return
    win.bkgd(' ', colors["CARD_BG"])
    win.erase()
    black_on_w = colors["BLACK_ON_WHITE"]
    suit_attr  = colors["RED_ON_WHITE"] if suit in RED_SUITS else black_on_w
    bold = curses.A_BOLD
    safe_add(win, 1, 1, rank, black_on_w | bold)
    safe_add(win, 1, 2, suit, suit_attr)
    safe_add(win, CARD_H - 2, CARD_W - 3, suit, suit_attr)
    safe_add(win, CARD_H - 2, CARD_W - 2, rank, black_on_w | bold)

def render_hand(stdscr, cards, colors, gap=2):
    max_y, max_x = stdscr.getmaxyx()
    n = len(cards)
    total_w = n * CARD_W + (n - 1) * gap
    x0 = max(0, (max_x - total_w) // 2)
    y0 = max(0, max_y - CARD_H - 1)
    if total_w > max_x or CARD_H + 1 > max_y:
        stdscr.clear()
        msg = "Terminal too small. Resize and try again."
        safe_add(stdscr, max_y // 2, max(0, (max_x - len(msg)) // 2), msg)
        stdscr.refresh()
        stdscr.getch()
        return
    for i, (rank, suit) in enumerate(cards):
        draw_card(stdscr, y0, x0 + i * (CARD_W + gap), rank, suit, colors)

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    if not curses.has_colors():
        safe_add(stdscr, 0, 0, "Your terminal doesn't support colors.")
        stdscr.refresh()
        stdscr.getch()
        return
    colors = init_colors()
    hand = random.sample(build_deck(), 6)
    render_hand(stdscr, hand, colors)
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)
