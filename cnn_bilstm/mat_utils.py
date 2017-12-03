import os
from glob import glob

from scipy.io import loadmat
import joblib
import numpy as np

def make_data_from_matlab_spects(data_dir):
    """makes data_dict just like utils.make_data, but
    loads spectrograms and labeled timebin vectors generated in matlab

    takes as a command line argument the name of the directory with the .mat files

    Each .mat file contains:
        s : ndarray
            the spectrogram
        f : ndarray
            vector of values at bin centers for frequencies in spectrogram
        t : ndarray
            vector of values for bin centers for times in spectrogram
        labels : ndarray
            vector of same length as t where each value is a label for that time bin
    containing the spectrograms.
    """
    if not os.path.isdir(data_dir):
        raise ValueError(f'{data_dir} is not recognized as a directory')
    else:
        os.chdir(data_dir)

    spect_files = glob('*.mat')

    spects = []
    spect_files_used = []
    all_time_bins = []
    labeled_timebins = []

    for counter, spect_file in enumerate(train_spect_files):
        print(f'loading {spect_file}')
        mat_dict = loadmat(spect_file, squeeze_me=True)

        if spect_file == 'train_keys.mat':
            continue

        if 's' not in mat_dict:
            print(f'Did not find a spectrogram in {spect_file}. Skipping this file.')
            continue

        if 'freq_bins' not in locals() and 'time_bins' not in locals():
            freq_bins = mat_dict['f']
            time_bins = mat_dict['t']
            timebin_dur = np.around(np.mean(np.diff(time_bins)), decimals=3)
        else:
            assert np.array_equal(mat_dict['f'], freq_bins)
            curr_file_timebin_dur = np.around(np.mean(np.diff(mat_dict['t'])),
                                              decimals=3)
            assert curr_file_timebin_dur == timebin_dur


        spect = mat_dict['s']
        labels = mat_dict['labels']
        # number of freq. bins should equaL number of rows
        assert mat_dict['f'].shape[-1] == spect.shape[0]
        # number of time bins should equal number of columns
        assert mat_dict['t'].shape[-1] == spect.shape[1]
        spects.append(spect)
        all_time_bins.append(time_bins)

        assert labels.shape[-1] == mat_dict['t'].shape[-1]
        labeled_timebins.append(labels)

        spect_files_used.append(spect)

    data_dict = {'spects': spects,
                 'filenames': spect_files_used,
                 'freq_bins': freq_bins,
                 'time_bins': all_time_bins,
                 'labeled_timebins': labeled_timebins,
                 'timebin_dur': timebin_dur,
                 'spect_params': None,
                 'labels_mapping': None}
    }

    print(f'saving data dictionary in {data_dir}')
    joblib.dump(data_dict, 'data_dict')


def convert_train_keys_to_txt(train_keys_path):
    """get train_keys cell array out of .mat file, convert to list of str, save as .txt
    """
    train_spect_files = loadmat(train_keys_path,
                                squeeze_me=True)['train_keys'].tolist()
    txt_filename = os.path.join(os.path.head(train_keys_path),
                                'training_filenames')
    with open(txt_filename, 'w') as fileobj:
        fileobj.writelines(train_spect_files)