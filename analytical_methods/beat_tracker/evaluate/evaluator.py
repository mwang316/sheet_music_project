# We will be evaluating using the algorithm as described here https://www.music-ir.org/mirex/wiki/2006:Audio_Beat_Tracking.

import librosa, sys, getopt
import numpy as np

def main(argv):
    inputfile = ''
    truthfile = ''
    try:
        opts, args = getopt.getopt(argv,'hi:t:',['ifile=','tfile='])

    except getopt.GetoptError:
        print('try \'evaluator.py -i <inputfile> -t <truthfile>\'')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('try \'evaluator.py -i <inputfile> -t <truthfile>\'')
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-t', '--tfile'):
            truthfile = arg

    if inputfile == '':
        print('Need to to specify an input file. Try \'evaluator.py -i <inputfile> -t <truthfile>\'')
        sys.exit()

    if truthfile == '':
        print('Need to to specify a truth file. Try \'evaluator.py -i <inputfile> -t <truthfile>\'')
        sys.exit()

    input_impulse = parse_beat_file(inputfile)[0]
    truth_impulses = parse_beat_file(truthfile)

    total_score = 0
    max_annotation_score = 0
    annotator_index = 0

    for truth_impulse in truth_impulses:
        impulse_index = np.where(truth_impulse==1)[0]
        # as proposed in the above website, error window will be arbitrarily set as 1/5 an annotated beat
        window = round(0.2 * np.median(impulse_index[1:] - impulse_index[:-1]))
        # normalization factor is the maximum number of impulses in either annotation or input
        normalization_factor = max(np.sum(truth_impulse), np.sum(input_impulse))
        # initial score without factoring the allowed error window
        min_size = min(len(input_impulse), len(truth_impulse))
        annotation_score = np.sum(input_impulse[:min_size] * truth_impulse[:min_size])


        for delay in range(1, window + 1):
            # shifting input impulses
            min_size = min(len(input_impulse) - delay, len(truth_impulse))
            annotation_score += np.sum(input_impulse[delay:min_size + delay] * truth_impulse[:min_size])

            #shifting truth impulses
            min_size = min(len(input_impulse), len(truth_impulse) - delay)
            annotation_score += np.sum(input_impulse[:min_size] * truth_impulse[delay:min_size + delay])

        annotation_score /= normalization_factor
        total_score += annotation_score

        annotator_index += 1
        print(f'Annotation score {annotator_index}: {annotation_score}')
        max_annotation_score = max(max_annotation_score, annotation_score)

    total_score /= len(truth_impulses)
    print(f'Total score: {total_score}')
    print(f'Max annotation score: {max_annotation_score}')

# returns a list of numpy arrays representing the impulse train for each annotation in the file
def parse_beat_file(file):
    out = []
    with open(file, 'r') as f:
        for line in f:
            beat_annotation = np.array(line.split('\t')).astype(float)
            print(beat_annotation)
            impulse_train = np.zeros(round(beat_annotation[-1] * 100) + 1)
            for beat in beat_annotation:
                impulse_train[round(beat * 100)] = 1
            # cutting out first 5 seconds, as done in the mirex competition, since some annotators needed time to adjust to song
            out.append(impulse_train[500:])

    return out

if __name__ == "__main__":
    main(sys.argv[1:])
