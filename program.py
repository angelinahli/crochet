from numpy.random import choice

## data

colors = [
    {"category": "green", "name": "forest green"},
    {"category": "green", "name": "moss"},
    {"category": "blue", "name": "purpley blue"}, 
    {"category": "blue", "name": "dark sky blue"},
    {"category": "red", "name": "pure red"},
    {"category": "red", "name": "red blend"},
    {"category": "white", "name": "pure white"},
    {"category": "white", "name": "speckled off white"},
    {"category": "white", "name": "speckled cream"},
    {"category": "grey", "name": "light grey"},
    {"category": "grey", "name": "dark grey"}
]

available_colors = [c for c in colors]

color_sequence = [] # current sequence of colors chosen

## program

def run(max_length=20):
    """
    Introduces itself, chooses a sequence of colors until the color_sequence
    lenth is `max_length` long OR a step fails to execute, then prints the
    sequence of colors chosen to the user.
    @return None
    """
    print("Welcome to a simple program to help you crochet!")
    step_executed = step()
    while step_executed and len(color_sequence) < max_length:
        step_executed = step()
    print("Your final color sequence:")
    print([c["name"] for c in color_sequence])

def step():
    """
    Chooses a color, notifies the user, stores the color in memory, and
    inquires whether the color is depleted after the user is done with one
    round of crocheting.
    @return (boolean) True if step was executed successfully, False otherwise
    """
    new_color = get_new_color(color_sequence, available_colors)
    if new_color == None:
        return False

    print("***********")
    print("Your next color is:", new_color["name"])
    color_sequence.append(new_color)
    depleted = input(
            "Did you finish using this color? Please enter " +
            "'True' or 'False' ") == "True"
    if depleted:
        available_colors.remove(new_color)
    return True

def get_new_color(
        current_sequence, available_colors, 
        newness=0.75, memory=3):
    """
    Given a sequence of already chosen colors, will select a new
    color, with the following rules:
    (1) will only choose colors that are available
    (2) will choose a color that has a category different from
        the last category of color chosen
    (3) will choose with P(`newness`) a color with a category different
        from the last `memory` colors in the sequence
    @return (dict) color chosen; None if no color is possible
    """
    candidates = get_possible_colors(current_sequence, available_colors)
    if len(candidates) == 0:
        return None

    last_categories = set(c["category"] for c in color_sequence[-memory:])
    num_new = len(
        list(c for c in candidates if c["category"] not in last_categories))
    weights = []
    for c in candidates:
        if c["category"] not in last_categories:
            weights.append( newness / num_new )
        else:
            weights.append( (1 - newness) / (len(candidates) - num_new) )

    chosen_color = choice(candidates, 1, weights)[0]
    return chosen_color

def get_possible_colors(current_sequence, available_colors):
    """
    @return (list[str]) possible colors given the current sequence
    """
    if len(current_sequence) == 0: 
        return available_colors
    last_category = current_sequence[-1]["category"]
    return [c for c in available_colors if last_category != c["category"]]

if __name__ == "__main__":
    run()
