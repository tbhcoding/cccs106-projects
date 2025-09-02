# basic_calculator.py
# CCCS 106 - Week 1 Lab Exercise
# Interactive Calculator with Enhanced Features

def display_header():
    """Display the calculator header because we're fancy like that."""
    print("=" * 50)
    print("FANCY CALCU NI BLESSIE ⋆𐙚₊˚⊹♡")
    print("=" * 50)

def get_number(prompt):
    """Get a valid number from user input because humans are terrible at typing."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Oops! That's not a number, silly goose! Try again:")

def perform_calculations(num1, num2):
    """Perform all basic arithmetic operations like a mathematical wizard."""
    results = {
        'addition': num1 + num2,
        'subtraction': num1 - num2,
        'multiplication': num1 * num2,
        'division': num1 / num2 if num2 != 0 else None,
        'power': num1 ** num2,
        'modulo': num1 % num2 if num2 != 0 else None
    }
    return results

def display_results(num1, num2, results):
    """Display calculation results like we're presenting at a math Olympics."""
    print("\n" + "=" * 50)
    print("BEHOLD! THE MATHEMATICAL WIZARDRY:")
    print("=" * 50)
    
    # Basic operations
    print(f"Addition:       {num1:8.2f} + {num2:8.2f} = {results['addition']:10.2f}")
    print(f"Subtraction:    {num1:8.2f} - {num2:8.2f} = {results['subtraction']:10.2f}")
    print(f"Multiplication: {num1:8.2f} x {num2:8.2f} = {results['multiplication']:10.2f}")
    
    # Division with error handling
    if results['division'] is not None:
        print(f"Division:       {num1:8.2f} / {num2:8.2f} = {results['division']:10.2f}")
    else:
        print(f"Division:       {num1:8.2f} / {num2:8.2f} = NOPE! Can't divide by zero, Captain!")
    
    # Additional operations
    print(f"Power:          {num1:8.2f} ^ {num2:8.2f} = {results['power']:10.2f}")
    
    if results['modulo'] is not None:
        print(f"Modulo:         {num1:8.2f} % {num2:8.2f} = {results['modulo']:10.2f}")
    else:
        print(f"Modulo:         {num1:8.2f} % {num2:8.2f} = Zero says NO WAY to modulo!")

def display_statistics(num1, num2):
    """Display additional statistical information because we're overachievers."""
    print("\n" + "-" * 50)
    print("BONUS ROUND - RANDOM MATH FACTS:")
    print("-" * 50)
    print(f"Bigger number:   {max(num1, num2):10.2f}  (The winner!)")
    print(f"Smaller number:  {min(num1, num2):10.2f}  (The underdog)")
    print(f"Average:         {(num1 + num2) / 2:10.2f}  (Perfectly balanced)")
    print(f"Difference:      {abs(num1 - num2):10.2f}  (How far apart they are)")
    
    # Number properties
    print(f"\nNumber Personality Test:")
    print(f"   First number is:  {'Happy (positive)' if num1 > 0 else 'Sad (negative)' if num1 < 0 else 'Confused (zero)'}")
    print(f"   Second number is: {'Happy (positive)' if num2 > 0 else 'Sad (negative)' if num2 < 0 else 'Confused (zero)'}")

def main():
    """Main calculator function that does all the heavy lifting."""
    try:
       
        display_header()
        
        print("Feed me two numbers and watch the magic happen:")
        num1 = get_number("First number (your favorite):  ")
        num2 = get_number("Second number (the sidekick): ")
        
        results = perform_calculations(num1, num2)
        
        display_results(num1, num2, results)
        display_statistics(num1, num2)
        
        print("\n" + "=" * 50)
        print("Ta-da! Math has been successfully mathed!")
        
    except KeyboardInterrupt:
        print("\n\nWhoa there! Someone got impatient and hit Ctrl+C!")
    except Exception as e:
        print(f"\nUh oh! Something went bonkers: {e}")
    finally:
        print("\nThanks for letting me show off my arithmetic skills!")
        print("Come back anytime for more number-crunching fun!")
        print("=" * 50)

# Run the calculator
if __name__ == "__main__":
    main()