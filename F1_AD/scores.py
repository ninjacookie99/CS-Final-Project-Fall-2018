import F1_AD.pyd

file = open("highscores.txt","a")
score = str(game.score)

file.write(score)

file.close()
