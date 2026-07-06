def get_valid_period_years():
    """
    Generates a standardized list of valid years for the system.
    Covers historical data and long-term projections (2010 through 2035).
    """
    start_year = 2010
    end_year = 2035
    
    # We add 1 to the end_year because the Python range function 
    # stops just before the last number.
    valid_years = list(range(start_year, end_year + 1))
    
    return valid_years

# --- Test the output ---
if __name__ == "__main__":
    years = get_valid_period_years()
    print(f"Successfully generated {len(years)} years.")
    print(f"Supported range: {years[0]} to {years[-1]}")
    # Example of how you might use this for validation:
    # if user_input_year not in years:
    #     print("Error: Year out of bounds.")