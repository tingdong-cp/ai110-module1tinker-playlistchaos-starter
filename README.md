# Playlist Chaos - Week 1 Tinker Activity

## Activity Summary
The core concept of this activity was to practice AI-assisted debugging by navigating a codebase to improve logic and consistency. I explored how data flows between the Streamlit UI and the backend logic, specifically regarding song classification and statistics. I found that students are most likely to struggle with the classification logic, where overlapping energy thresholds and keyword searches can lead to songs being mislabeled. While AI was extremely helpful for explaining complex list comprehensions, it was occasionally misleading by suggesting fixes that ignored specific profile settings, leading to even more "chaos." To guide a student without giving the answer, I would ask them to use `st.write()` to print the song dictionary to the screen to visualize exactly which data fields are being passed to the classification function.

---

## 1. Investigation: Observed Issues
As a "curious investigator," I identified the following five bugs/inconsistencies in the original app:
1. **Search Failure:** Searching for an artist (e.g., "AC/DC") returned no results even when the song was clearly in the list.
2. **Incorrect Average Energy:** The average energy statistic only reflected the "Hype" playlist rather than the whole library.
3. **Skewed Hype Ratio:** The ratio was calculated incorrectly, often showing 100% or causing a division-by-zero error.
4. **Lucky Pick Exclusion:** The "any" mode in the Lucky Pick feature ignored all songs categorized as "Mixed."
5. **Normalization Side-Effects:** Artist names were being lowercased during normalization, making the display inconsistent with the input.

---

## 2. Technical Fixes
I implemented the following four fixes in `playlist_logic.py` to stabilize the app:

### Fix 1: Search Logic Correction
* **Source:** `search_songs()` function.
* **Problem:** The code checked `if value in q`, which meant it was checking if the artist name was inside the search query.
* **Correction:** Flipped the logic to `if q in value` so the app searches for your text inside the artist name.

### Fix 2: Global Average Energy Calculation
* **Source:** `compute_playlist_stats()` function.
* **Problem:** `total_energy` was only being calculated for the `hype` list.
* **Correction:** Changed the loop to iterate through `all_songs` to get a true library average.

### Fix 3: Hype Ratio Denominator
* **Source:** `compute_playlist_stats()` function.
* **Problem:** The code used `total = len(hype)`, which incorrectly set the scale for the ratio.
* **Correction:** Updated `total` to `len(all_songs)` to show how "Hype" songs compare to the entire collection.

### Fix 4: Inclusive Lucky Pick
* **Source:** `lucky_pick()` function.
* **Problem:** The "any" mode combined Hype and Chill but left out Mixed songs.
* **Correction:** Added `playlists.get("Mixed", [])` to the combined list.

---

## 3. How the code is organized

### `app.py`  
The Streamlit user interface handling the Mood profile, Song addition, Playlist tabs, and Stats metrics.

### `playlist_logic.py`  
The backend engine handling song normalization, classification logic, and the mathematical computations for stats.

---

## 4. Tips for Success
- **Use AI as a Rubber Duck:** I found that asking the AI "What does this specific line of logic do?" was more helpful than asking "Fix this code."
- **Test Frequently:** After every small change to `playlist_logic.py`, I refreshed the Streamlit app to ensure the UI metrics updated correctly.
- **Visual Debugging:** Using `st.write(st.session_state)` is a great way to see if your "Add Song" feature is actually working behind the scenes.

---

---

# Week 2 – Game Glitch Investigator

## Bugs Fixed

### Fix 5: Artist Display Casing
* **Source:** `normalize_song()` function.
* **Problem:** `normalize_artist()` lowercased the artist name, which was then stored and displayed in the UI. A user who typed "AC/DC" would see "ac/dc" on screen.
* **Correction:** Captured the original artist string in `artist_raw` before normalization, then added an `artist_display` field to the returned song dict to preserve original casing for the UI while keeping `artist` lowercased for search and comparison logic.

### Fix 6: Lucky Pick Crash on Empty Playlist
* **Source:** `random_choice_or_none()` function.
* **Problem:** `random.choice()` raises an `IndexError` when passed an empty list, meaning Lucky Pick would crash if no songs existed in the selected playlist.
* **Correction:** Added an empty list guard — if `songs` is empty, return `None` instead of calling `random.choice()`.

---

## AI Skepticism Note
When asked to fix the artist casing bug, AI suggested simply removing `.lower()` from `normalize_artist()`. This appears correct at first glance but breaks `search_songs()`, which depends on artist values being lowercased for case-insensitive matching. The correct fix preserves `.lower()` for comparison while storing a separate `artist_display` field for the UI.

---

## Student Hint
> "When a user types 'AC/DC' and it shows up differently on screen, where in the code do you think that transformation is happening? Try printing the song dictionary right after normalization and compare it to what the user originally typed."

---

## Tests
Pytest cases for both fixes are in `test_playlist_logic.py`. All 7 tests pass.