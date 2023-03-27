import pytest
import logging
from handlers.time_parser import TimeParser


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("12:00", "midday"),
        ("00:00", "midnight"),
        ("24:00", "midnight"),
        ("12:30", "half past twelve pm"),
        ("13:00", "one o'clock pm"),
        ("13:50", "ten to two pm"),
        ("09:10", "ten past nine am"),
        ("09:23", "twenty-three past nine am")
    ],
)
async def test_print_time(test_input, expected):
    resp = await TimeParser(test_input).print_time()

    assert resp == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "test_input",
    [
        "25::15",
        "2023-03-27 15:53:07.646354",
    ],
)
async def test_print_time_ValueError(caplog, test_input):
    with caplog.at_level(logging.INFO):
        with pytest.raises(ValueError):
            resp = await TimeParser(test_input).print_time()
            assert "Time input failed regex validation" in caplog.text

