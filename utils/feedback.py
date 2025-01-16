def send_feedback(player_id: int, total_points: int):
    """
    Send feedback to the player based on their total points.
    """
    if total_points < 10:
        feedback = f"Player {player_id}: Keep it up! You're almost there. Try to push harder!"
    elif 10 <= total_points < 20:
        feedback = f"Player {player_id}: Great job! You're showing good progress."
    else:
        feedback = f"Player {player_id}: Excellent! You've earned a high score. Keep it going!"
    
    print(feedback)  # This will print feedback to the console
    return feedback  # Feedback could also be saved or sent via email, etc.
