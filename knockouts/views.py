from django.shortcuts import render, redirect

# Define the initial games
R16_GAMES = [
    ("Spain", "Georgia"),
    ("Germany", "Denmark"),
    ("Portugal", "Slovenia"),
    ("France", "Belgium"),
    ("Romania", "Netherlands"),
    ("Austria", "Turkey"),
    ("England", "Slovakia"),
    ("Switzerland", "Italy")
]

def tournament_view(request, round_name):
    if request.method == 'POST':
        # Collect the winners based on the form submission
        winners = [request.POST['winners' + str(idx)] for idx in range(len(request.session.get(f'{round_name}_games', [])))]
        request.session[round_name + '_winners'] = winners
        next_round = {'R16': 'QF', 'QF': 'SF', 'SF': 'F', 'F': 'results'}.get(round_name, 'R16')
        return redirect('tournament', round_name=next_round)

    # Initialize games for the first round or pair up winners for subsequent rounds
    if round_name == 'R16':
        request.session[f'{round_name}_games'] = R16_GAMES
    else:
        previous_winners = request.session.get(f'{round_name}_winners', [])
        games = list(zip(previous_winners[::2], previous_winners[1::2])) if previous_winners else []
        request.session[f'{round_name}_games'] = games

    games = request.session.get(f'{round_name}_games', [])
    return render(request, f'knockouts/{round_name.lower()}.html', {'games': games, 'round_name': round_name})

