import pickle
from object import *


def check_highscore(score):
    highscores = read_highscores()
    if highscores[-1] < score:
        return True
    return False

def store_highscore(score):

    highscores = read_highscores()
    for index in range(len(highscores)):
        if highscores[index] < score:
            highscores.insert(index,score)
            highscores.pop(-1)
            break

    # Serialize the list
    serialized_data = pickle.dumps(highscores)

    # Save the serialized data to a file
    with open('scores.pickle', 'wb') as file:
        file.write(serialized_data)

def read_highscores():
    # Load the serialized data from the file
    with open('scores.pickle', 'rb') as file:
        serialized_data = file.read()

    # Deserialize the data back into a list
    deserialized_highscores = pickle.loads(serialized_data)

    return deserialized_highscores

def get_pos(score):
    highscores = read_highscores()
    if score == 0:
        return -1
    for i in range(len(highscores)):
        if score == highscores[i]:
            return i

def reset_highscores():
    highscores = [0,0,0,0,0]

    # Serialize the list
    serialized_data = pickle.dumps(highscores)

    # Save the serialized data to a file
    with open('scores.pickle', 'wb') as file:
        file.write(serialized_data)

def insert_scores(obj_list,curr_score):

    if check_highscore(curr_score):
        new_highscore_text = txt_obj("NEW HIGHSCORE")
        new_highscore_text.color = (0, 0, 0) , (255, 255, 255)
        new_highscore_text.x = SCREEN_WIDTH / 2 - 140  # score text is repositioned
        new_highscore_text.y = SCREEN_HEIGHT / 2 - 150
        obj_list.append(new_highscore_text)

    label = txt_obj("HIGHSCORES")
    store_highscore(curr_score)
    label.y = 200
    label.x = 140
    obj_list.append(label)
    curr_index = get_pos(curr_score)
    highscores = read_highscores()
    for i in range(len(highscores)):
        score = txt_obj(str(highscores[i]))
        score.y = 250 + 40 * i
        score.x = 175
        if curr_index == i:
           score.color = (0, 0, 0) , (255, 255, 255)
        obj_list.append(score)


