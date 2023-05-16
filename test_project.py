import project
import pytest

def test_command_line_arg():
    with pytest.raises(SystemExit):
        project.validate_arguments()

def test_player_name():
    with pytest.raises(SystemExit):
        project.validate_player("Robert Lewandowski")

def test_season_validate():
    assert project.validate_season(203999, 2030) == False
    assert project.validate_season(203999, 1535) == False