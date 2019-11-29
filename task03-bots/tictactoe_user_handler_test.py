import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_github_sample(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('hi')
    handler.handle_message('X 1 1')
    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('O 0 1')
    handler.handle_message('O 0 0')
    handler.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\nOX.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('...\n...\n...'),
    ]


def test_multiple_start(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start')
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('start')
    handler.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n...'),
    ]


def test_win(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 1 0')
    handler.handle_message('X 0 1')
    handler.handle_message('O 1 1')
    handler.handle_message('X 0 2')
    handler.handle_message('O 1 2')
    handler.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XO.\nX..\n...'),
        mocker.call('XO.\nXO.\n...'),
        mocker.call('Game is finished, X wins'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
    ]
