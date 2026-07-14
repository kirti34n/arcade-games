"""
play - Terminal mini games collection

Usage:
    play              Launch interactive game menu (needs terminal)
    play snake        Play Snake interactively
    play tetris       Play Tetris interactively
    play 2048         Play 2048 interactively
    play dino         Play Dino Runner interactively
    play breakout     Play Breakout interactively
    play shooter      Play Space Shooter interactively
    play pong         Play Pong interactively
    play flappy       Play Flappy Bird interactively
    play mines        Play Minesweeper interactively
    play pacman       Play Pac-Man interactively
    play sokoban      Play Sokoban interactively
    play reversi      Play Reversi / Othello vs AI
    play frogger      Play Frogger interactively
    play connect4     Play Connect Four vs AI

    play mp           LAN multiplayer lobby (Reversi, Connect Four, Pong)

    play cli                    Show in-conversation game menu
    play cli start snake        Start Snake (turn-based)
    play cli start 2048         Start 2048
    play cli start minesweeper  Start Minesweeper
    play cli start connect4     Start Connect4
    play cli <move>             Make a move (up/down/left/right)
    play cli <1-7>              Connect4: drop in column
    play cli reveal <r> <c>     Minesweeper: reveal cell
    play cli flag <r> <c>       Minesweeper: toggle flag
    play cli show               Show current board
    play cli quit               End current game

    play --version    Show version
    play --help       Show this help

Install:
    pip install terminal-games

Note: the full-screen games use Python's curses module. It ships with Python on
Linux/macOS; on Windows `pip install terminal-games` also pulls in windows-curses.
The turn-based `play cli ...` games and text commands work with no curses at all.
"""
import locale
import sys

from . import config
from ._version import __version__
from .cli import _cli_mode, _load_game_state
from .menu import _menu, _run_game
from .net import _net_menu
from .registry import _GAMES, _GAME_MAP
from .terminal import _curses_wrapper


def main():
    # Ensure box-drawing / unicode output doesn't crash on a legacy console
    # (e.g. Windows cp1252). errors='replace' keeps text commands alive.
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(encoding='utf-8', errors='replace')
        except (AttributeError, ValueError):
            pass
    try:
        locale.setlocale(locale.LC_ALL, '')
    except (locale.Error, ValueError):
        pass
    try:
        _main()
    except KeyboardInterrupt:
        # curses.wrapper already restores the terminal on the way out; this
        # just stops Ctrl-C from dumping a raw traceback over it.
        print()
        sys.exit(130)


def _main():
    config._migrate_config()
    args = sys.argv[1:]

    if not args:
        _curses_wrapper(_menu)
        return

    cmd = args[0].lower().strip('-')

    # Quick move shortcuts: play w/a/s/d (no Claude needed, use with ! prefix)
    _shortcuts = {'w': 'up', 'a': 'left', 's': 'down', 'd': 'right',
                  'up': 'up', 'down': 'down', 'left': 'left', 'right': 'right'}
    if cmd in _shortcuts:
        state = _load_game_state()
        if state and not state.get('over'):
            _cli_mode([_shortcuts[cmd]])
            return

    # Connect4 column shortcut: play 3 (drops in column 3). Exclude real game
    # names like "2048" so `play 2048` still launches the interactive game.
    if cmd.isdigit() and cmd not in _GAME_MAP:
        state = _load_game_state()
        if state and state.get('game') == 'connect4' and not state.get('over'):
            _cli_mode([cmd])
            return

    # Direct game commands: play reveal/flag/show/quit/new
    if cmd in ('reveal', 'flag'):
        _cli_mode(args)
        return
    if cmd == 'show':
        _cli_mode(['show'])
        return
    if cmd in ('quit', 'stop', 'end'):
        _cli_mode(['quit'])
        return
    if cmd == 'new':
        game = args[1] if len(args) > 1 else ''
        _cli_mode(['start', game])
        return

    if cmd == 'cli':
        _cli_mode(args[1:])
    elif cmd in ('mp', 'multiplayer', 'net'):
        _curses_wrapper(_net_menu, 'multiplayer')
    elif cmd in ('h', 'help'):
        print(__doc__.strip())
    elif cmd in ('v', 'version'):
        print(f'play {__version__}')
    elif cmd in ('list', 'ls'):
        for name, desc, cls in _GAMES:
            hi = config.load_high_score(cls.name)
            hs = f'  [Best: {hi}]' if hi else ''
            print(f'  {name:<14} {desc}{hs}')
    elif cmd in _GAME_MAP:
        cls = _GAME_MAP[cmd]
        _curses_wrapper(lambda s, c=cls: _run_game(s, c), cmd)
    else:
        print(f'Unknown game: {cmd}')
        print('Available: ' + ', '.join(n for n, _, _ in _GAMES))
        sys.exit(1)
