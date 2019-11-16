import matplotlib.pyplot as plt
import random
import string

def plot_spectogram(audio_data, frame_rate, output_path):
    data1D = audio_data[:,0]
    fig, ax = plt.subplots(1)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.axis('off')
    pxx, freqs, bins, im = ax.specgram(x=data1D, Fs=frame_rate, noverlap=384, NFFT=512)
    ax.axis('off')
    fig.savefig(output_path, dpi=300, frameon='false')
    plt.close(fig)

def randomStringDigits(stringLength=6):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))
