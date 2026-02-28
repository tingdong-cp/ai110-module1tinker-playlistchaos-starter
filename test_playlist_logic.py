import pytest
from playlist_logic import normalize_song, random_choice_or_none


def test_artist_display_preserves_casing():
    """artist_display should keep original casing."""
    song = normalize_song({"title": "Back in Black", "artist": "AC/DC", "genre": "rock", "energy": 9})
    assert song["artist_display"] == "AC/DC"

def test_artist_lowercase_for_comparison():
    """artist field should be lowercased for search/logic."""
    song = normalize_song({"title": "Back in Black", "artist": "AC/DC", "genre": "rock", "energy": 9})
    assert song["artist"] == "ac/dc"

def test_artist_display_strips_whitespace():
    """artist_display should strip leading/trailing whitespace."""
    song = normalize_song({"title": "T", "artist": "  Queen  ", "genre": "rock", "energy": 8})
    assert song["artist_display"] == "Queen"

def test_artist_display_and_artist_are_different():
    """artist and artist_display should differ when input has uppercase."""
    song = normalize_song({"title": "T", "artist": "The Beatles", "genre": "rock", "energy": 5})
    assert song["artist"] != song["artist_display"]



def test_random_choice_returns_none_on_empty():
    """Should return None when given an empty list, not crash."""
    assert random_choice_or_none([]) is None

def test_random_choice_returns_a_song():
    """Should return a song from the list."""
    songs = [{"title": "Song A"}, {"title": "Song B"}]
    result = random_choice_or_none(songs)
    assert result in songs

def test_random_choice_returns_only_song_in_single_item_list():
    """Should return the only song when list has one item."""
    songs = [{"title": "Only Song"}]
    assert random_choice_or_none(songs) == {"title": "Only Song"}