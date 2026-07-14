"""
play - Terminal mini games collection

This module is a thin backwards-compatible shim: the real implementation now
lives in the terminal_games package. It re-exports the public names so
`python play.py` and existing scripts/tests that do `import play` keep
working unchanged. See terminal_games/main.py for the CLI docstring/usage.
"""
from terminal_games._version import __version__
from terminal_games import config
from terminal_games.config import (
    CONFIG_DIR, SCORES_FILE, GAME_STATE_FILE,
    load_high_score, save_high_score,
)
from terminal_games.game import Game
from terminal_games.games.snake import SnakeGame
from terminal_games.games.tetris import TetrisGame
from terminal_games.games.g2048 import Game2048
from terminal_games.games.dino import DinoGame, _CACTUS_SM, _CACTUS_LG, _CACTUS_XL
from terminal_games.games.breakout import BreakoutGame
from terminal_games.games.shooter import ShooterGame
from terminal_games.games.pong import PongGame
from terminal_games.games.flappy import FlappyGame
from terminal_games.games.minesweeper import MinesweeperGame
from terminal_games.games.pacman import PacManGame
from terminal_games.games.sokoban import SokobanGame
from terminal_games.games.reversi import ReversiGame
from terminal_games.games.frogger import FroggerGame
from terminal_games.games.connect4 import ConnectFourGame
from terminal_games.registry import _ICONS, _GAMES, _GAME_MAP, _TITLE, _NET_GAMES
from terminal_games.menu import _menu, _run_game
from terminal_games.net import _NetLink, _net_menu
from terminal_games.cli import (
    _cli_snake_move, _cli_snake_init, _cli_snake_render,
    _cli_2048_init, _cli_2048_move, _cli_2048_render,
    _cli_ms_init, _cli_ms_move, _cli_ms_render,
    _cli_c4_init, _cli_c4_move, _cli_c4_render, _cli_c4_check_win,
    _cli_c4_ai_move, _cli_mode,
)
from terminal_games.main import main

if __name__ == '__main__':
    main()
