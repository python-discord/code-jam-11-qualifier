from qualifier.qualifier import Quote, VariantMode, run_command

def main():
    print("Starting the Test")
    print(f"Modes available are: {VariantMode.NORMAL}, {VariantMode.UWU}, {VariantMode.PIGLATIN}")
    
    #piglatin_quote = Quote("Hello", VariantMode.PIGLATIN)
    #print(piglatin_quote._create_variant())


    # Test the `quote` command
    run_command('quote "Hello world"')
    
    # Test the `quote uwu` command
    run_command('quote uwu "Let us laze about in Usher\'s Rolls Royce"')
    
    # Test the `quote piglatin` command
    run_command('quote piglatin "Hello world"')
    
    # Test the `quote list` command
    run_command('quote list')

if __name__ == "__main__":
    main()
