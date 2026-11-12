from scr.snake.game import SnakeGame


def test_initial_score():
    game = SnakeGame()
    assert game.score == 0
