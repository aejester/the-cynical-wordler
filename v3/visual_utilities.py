"""
⬜⬜⬜⬜⬜
⬜🟩⬜⬜⬜
⬜🟩⬜⬜⬜
⬜🟩🟨⬜⬜
⬜🟩⬜⬜🟩
🟩🟩🟩🟩🟩
"""

"""
⬛⬛⬛⬛⬛
⬛🟨🟨🟨⬛
🟨🟩⬛🟩⬛
⬛🟩🟩🟩⬛
⬛⬛⬛⬛⬛
🟩🟩🟩🟩🟩
"""

def build_wordle_grid(guesses: list[list[tuple]], probable_guess: list[tuple] = []):
    built = []
    chars = {"2": "🟩", "1": "🟨", "0": "⬜", "empty": "⬛"}
    for guess in guesses:
        row = ""
        for char in guess:
            row += chars[str(char[0])]
        built.append(row)
    if probable_guess != []:
        row = ""
        for char in probable_guess:
            row += chars[str(char)]
        built.append(row)
        
    return "\n".join(built)