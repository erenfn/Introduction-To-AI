import os
import sys
import copy
import numpy as np

FLAG = 'FLAG'
SMALL = 1e-15
tag_count_dict = {}
transition_dict = {}
tag_to_word_dict = {}
transition_count_dict = {}
tags_set = {}

end_pun = {'.', '?', '!'}
quotes = {'\'', '\"'}

def tag(training_list, test_file, output_file):
    print("Tagging the file.")

    sentences = parse_test(test_file)
    print_sentence(sentences)
    for training in training_list:
        read_input(training)
    f = open(output_file, 'w')
    sys.stdout = f
    main_out = sys.stdout
    for sentence in sentences:
       viterbi(sentence)

    sys.stdout = main_out
    f.close()

def print_sentence(sentences: list):
    main_out = sys.stdout
    f = open('output.txt', 'w')
    sys.stdout = f
    for sentence in sentences:
        for word in sentence:
            print(word, end=' ')
        print()

    sys.stdout = main_out
    f.close()

def parse_test(test_file) -> list[list[str]]:
    with open(test_file) as f2:
        lines = f2.readlines()
        sentences = []
        sentence = []
        backup_sentence = []
        previous = None

        for line in lines:
            sentence.append(line.strip())
            if line.strip() in end_pun:
                backup_sentence = copy.deepcopy(sentence)
                sentences.append(sentence)
                sentence = []
            elif line.strip() in quotes and previous in end_pun:
                backup_sentence.append(line.strip())
                sentences.pop()
                sentences.append(backup_sentence)
                backup_sentence = []
                sentence = []
            previous = line.strip()
        return sentences

def viterbi(E: list):
    tags = list(tags_set.keys())
    tag_count = len(tags)
    prob = np.empty([len(E), tag_count])
    prev = np.empty([len(E), tag_count])

    initial = transition_dict['start']

    # Determine values for time step 0
    for i in range(tag_count):
        if tags[i] in initial.keys():
            initial_prob = initial[tags[i]] / transition_count_dict['start']
        else:
            initial_prob = 0
        if tags[i] in tag_to_word_dict.keys():
            if E[0] in tag_to_word_dict[tags[i]].keys():
                tag_prob = tag_to_word_dict[tags[i]][E[0]] / tag_count_dict[tags[i]]
            else:
                tag_prob = 0
        else:
            tag_prob = 0
        prob[0, i] = initial_prob * tag_prob
        prev[0, i] = SMALL
    # For time steps 1 to length(E)-1,
    # find each current state's most likely prior state x.
    for t in range(1, len(E)):
        for i in range(tag_count):
            x = FLAG
            max_value = SMALL
            if tags[i] in transition_dict.keys():
                previous = transition_dict[tags[i]]
                for y in range(tag_count):
                    try:
                        tag = previous[tags[y]] / transition_count_dict[tags[i]]
                    except KeyError:
                        tag = 0
                    value = prob[t - 1, y] * tag
                    if x == FLAG or max_value < value:
                        x = y
                        max_value = value
            if tags[i] in tag_to_word_dict.keys():
                if E[t] in tag_to_word_dict[tags[i]].keys():
                    tag_prob2 = tag_to_word_dict[tags[i]][E[t]] / tag_count_dict[tags[i]]
                else:
                    tag_prob2 = SMALL
            else:
                tag_prob2 = SMALL
            prob[t, i] = max_value * tag_prob2
            prev[t, i] = x
    states = []
    amax = np.argmax(prob, axis=0)[len(E) - 1]
    states.append(amax)
    for t in range(len(E)-1, 0, -1):
        states.append(prev[t][amax])
        amax = int(prev[t][amax])

    states.reverse()
    for t in range(len(E)):
        if E[t] not in quotes and E[t] not in end_pun and E[t] != ',':
            print(E[t], ':', tags[int(states[t])])
        elif E[t] in quotes:
            print(E[t], ':', 'PUQ')
        else:
            print(E[t], ':', 'PUN')


def read_input(training_list: str):

    previous = 'start'

    with open(training_list) as f:
        lines = f.readlines()
        num_puq = 0
        backup = None
        for line in lines:
            splitted = line.split(' : ')
            tag = splitted[1].strip()
            word = splitted[0]

            if word == '\"':
                num_puq += 1

            # do the tag to word dict
            if tag not in tag_to_word_dict.keys():
                tag_to_word_dict[tag] = {}
                tag_to_word_dict[tag][word] = 1
            else:
                if word not in tag_to_word_dict[tag].keys():
                    tag_to_word_dict[tag][word] = 1
                else:
                    tag_to_word_dict[tag][word] += 1

            # do the tag count dict
            if tag not in tag_count_dict.keys():
                tag_count_dict[tag] = 1
            else:
                tag_count_dict[tag] += 1

            # do the transition dict
            if word == '\"' and num_puq % 2 == 0 and backup not in transition_dict.keys():
                
                transition_dict[backup] = {}
                transition_dict[backup][tag] = 1
                # do transition count dict
                if backup not in transition_count_dict.keys():
                    transition_count_dict[backup] = 1
                else:
                    transition_count_dict[backup] += 1
            elif word == '\"' and num_puq % 2 == 0 and backup in transition_dict.keys():
                
                if tag in transition_dict[backup]:
                    transition_dict[backup][tag] += 1
                else:
                    transition_dict[backup][tag] = 1
                # do transition count dict
                if backup not in transition_count_dict.keys():
                    transition_count_dict[backup] = 1
                else:
                    transition_count_dict[backup] += 1
            else:
                if previous not in transition_dict.keys():
                    transition_dict[previous] = {}
                    transition_dict[previous][tag] = 1
                else:
                    if tag in transition_dict[previous]:
                        transition_dict[previous][tag] += 1
                    else:
                        transition_dict[previous][tag] = 1
                # do transition count dict
                if previous not in transition_count_dict.keys():
                    transition_count_dict[previous] = 1
                else:
                    transition_count_dict[previous] += 1

            # check end of sentence
            if word == '.' or word == '?' or word == '!':
                previous = 'start'
                backup = tag
            elif (word == '\"' or word == '\'') and num_puq % 2 == 0 and backup is not None:
                previous = 'start'
                backup = None
            else:
                previous = tag
            if tag not in tags_set.keys():
                tags_set[tag] = len(tags_set)

if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]
    # Start the training and tagging operation.
    tag(training_list, test_file, output_file)
