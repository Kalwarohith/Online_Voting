from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "secret_key"  # Required for flash messages

# Predefined political parties
political_parties = ["Party A", "Party B", "Party C", "Party D"]

# Initialize the votes dictionary
votes = {
    "Party A": 0,
    "Party B": 0,
    "Party C": 0,
    "Party D": 0
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add_candidate", methods=["GET", "POST"])
def add_candidate():
    if request.method == "POST":
        voter_id = request.form["voter_id"]
        candidate_name = request.form["candidate_name"]
        flash(f"Candidate '{candidate_name}' with Voter ID '{voter_id}' added successfully!")
        return redirect(url_for("index"))

    return render_template("add_candidate.html")


@app.route("/cast_vote", methods=["GET", "POST"])
def cast_vote():
    if request.method == "POST":
        voter_id = request.form["voter_id"]
        selected_party = request.form["selected_party"]

        # Check if the selected party is valid
        if selected_party in political_parties:
            # Update the vote count
            votes[selected_party] += 1
            flash(f"Vote cast successfully for {selected_party}!")
        else:
            flash("Invalid party selection!")
        return redirect(url_for("index"))
    return render_template("cast_vote.html", political_parties=political_parties)


@app.route("/results")
def results():
    # Sort the vote counts in descending order
    sorted_votes = sorted(votes.items(), key=lambda x: x[1], reverse=True)

    # Check for tie between parties
    top_votes = sorted_votes[0][1]  # Get the highest vote count
    top_parties = [party for party, vote_count in sorted_votes if vote_count == top_votes]

    if len(top_parties) > 1:
        top_party = f"The parties with the highest votes are: {', '.join(top_parties)} with {top_votes} votes (Tie)"
    else:
        top_party = f"The party with the highest votes is: {top_parties[0]} with {top_votes} votes"

    return render_template("results.html", candidates=sorted_votes, top_party=top_party)


if __name__ == "__main__":
    app.run(debug=True)
