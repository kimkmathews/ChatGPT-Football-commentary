# Authors : Kim Kuruvilla Mathews and Panagiotis Georgios Pennas
# Importing functions from prompting_gen module
from prompting_gen import match_details, get_ball_position, get_frame_details, random_frame_gen, prompting_details, prompt_generation

def get_input():
    # Function to import match_id and frame_id as integers
    match_id = int(input("Enter the match ID: "))
    frame_id = int(input("Enter the frame ID: "))
    return match_id, frame_id

def main():
    # Main program loop
    while True:
        # Display menu options
        print("Choose an option:")
        print("1. Get random frame")
        print("2. Input match_id and frame_id")
        print("3. Exit")

        # Get user choice
        choice = input("Enter your choice (1/2/3): ")

        # Process user choice
        if choice == '1':
            match_id, frame_id = random_frame_gen()
        elif choice == '2':
            match_id, frame_id = get_input()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

        # Get match details
        home_team_id, home_team, away_team_id, away_team = match_details(match_id)
        print(f'Match: {home_team} vs {away_team}')

        # Get frame details
        period, minute, second = get_frame_details(match_id, frame_id)
        if period == 1:
            half = 'first'
        elif period == 2:
            half = 'second'
        print(f'Time: {minute}:{second} {half} half')

        # Get and display prompt details and response
        prompt = prompting_details(match_id, frame_id)
        response = prompt_generation(prompt)
        print(response)

# Entry point of the script
if __name__ == "__main__":
    main()
