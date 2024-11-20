"""A script to combine multiple wav files into a single wav file.
It sorts the files by name before appending the audio one by one.
Meant to be used when filenames bear a timestamp."""
import wave
import os

file_dir = input('Enter directory path of wav files: ')

files = os.listdir(file_dir)

files_sorted = sorted(files)

new_file_name = input('Enter new file name: ')
rate = None
sample_width = None
n_channels = None
with wave.open(os.path.join(file_dir, new_file_name), 'wb') as f_write:
    for filename in files_sorted:
        if filename.endswith('.wav'):
            with wave.open(os.path.join(file_dir,filename), 'rb') as f_read:

                # Checks
                if rate is None:
                    rate = f_read.getframerate()
                    sample_width = f_read.getsampwidth()
                    n_channels = f_read.getnchannels()
                    f_write.setframerate(rate)
                    f_write.setsampwidth(sample_width)
                    f_write.setnchannels(n_channels)
                else:
                    try:
                        assert rate == f_read.getframerate()
                        assert sample_width == f_read.getsampwidth()
                        assert n_channels == f_read.getnchannels()
                    except AssertionError:
                        raise ValueError('Rate mismatch')

                curr_file_audio = f_read.readframes(f_read.getnframes())
                f_write.writeframes(curr_file_audio)
                print(f'Added {filename}')
