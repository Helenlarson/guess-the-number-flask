from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route("/", methods=["GET", "POST"])
def index():
    if "secret_number" not in session:
        session["secret_number"] = random.randint(1, 10)  # pode mudar pra 100 se quiser
        session["attempts"] = 0

    message = None

    if request.method == "POST":
        guess_str = request.form.get("guess", "").strip()

        if not guess_str.isdigit():
            message = "Please enter a valid number."
        else:
            session["attempts"] += 1  # conta tentativa só quando é número válido
            guess = int(guess_str)
            secret = session["secret_number"]

            if guess < secret:
                message = "Too low! Try again."
            elif guess > secret:
                message = "Too high! Try again."
            else:
                message = f"Congratulations! You've guessed the number {secret} in {session['attempts']} attempts."

    # ✅ IMPORTANTE: sempre retornar uma resposta (GET ou POST)
    return render_template("index.html", message=message, attempts=session.get("attempts", 0))


# (deixe reset comentado por enquanto, ok)
@app.route("/reset", methods=["POST"])
def reset():
    session.pop("secret_number", None)
    session.pop("attempts", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
