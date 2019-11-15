import matplotlib.pyplot as plt

def plot_spectogram(audio_data, frame_rate, output_path):
    data1D = audio_data[:, 0]
    fig, ax = plt.subplots(1)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.axis('off')
    pxx, freqs, bins, im = ax.specgram(x=data1D, Fs=rate, noverlap=384, NFFT=512)
    ax.axis('off')
    fig.save(output_path, dpi=300, frameon='false')
    plt.close(fig)
