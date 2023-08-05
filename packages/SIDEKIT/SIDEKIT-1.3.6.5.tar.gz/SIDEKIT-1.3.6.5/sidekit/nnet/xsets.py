# -*- coding: utf-8 -*-
#
# This file is part of SIDEKIT.
#
# SIDEKIT is a python package for speaker verification.
# Home page: http://www-lium.univ-lemans.fr/sidekit/
#
# SIDEKIT is a python package for speaker verification.
# Home page: http://www-lium.univ-lemans.fr/sidekit/
#
# SIDEKIT is free software: you can redistribute it and/or modify
# it under the terms of the GNU LLesser General Public License as
# published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# SIDEKIT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with SIDEKIT.  If not, see <http://www.gnu.org/licenses/>.

"""
Copyright 2014-2020 Anthony Larcher

The authors would like to thank the BUT Speech@FIT group (http://speech.fit.vutbr.cz) and Lukas BURGET
for sharing the source code that strongly inspired this module. Thank you for your valuable contribution.
"""

import h5py
import numpy
import pandas
import pickle
import random
import torch

from torch.utils.data import Dataset
from ..frontend.io import read_dataset_percentile
from ..features_server import FeaturesServer




__license__ = "LGPL"
__author__ = "Anthony Larcher"
__copyright__ = "Copyright 2015-2020 Anthony Larcher"
__maintainer__ = "Anthony Larcher"
__email__ = "anthony.larcher@univ-lemans.fr"
__status__ = "Production"
__docformat__ = 'reStructuredText'


def read_batch(batch_file):
    """
    :param batch_file:
    :return:
    """
    with h5py.File(batch_file, 'r') as h5f:
        data = read_dataset_percentile(h5f, 'data')
        label = h5f['label'][()]

        # Normalize and reshape
        data = data.reshape((len(label), data.shape[0] // len(label), data.shape[1])).transpose(0, 2, 1)
        for idx in range(data.shape[0]):
            m = data[idx].mean(axis=0)
            s = data[idx].std(axis=0)
            data[idx] = (data[idx] - m) / s
        return data, label


class XvectorDataset(Dataset):
    """
    Object that takes a list of files from a file and initialize a Dataset
    """
    def __init__(self, batch_list, batch_path):
        with open(batch_list, 'r') as fh:
            self.batch_files = [batch_path + '/' + l.rstrip() for l in fh]
            self.len = len(self.batch_files)

    def __getitem__(self, index):
        data, label = read_batch(self.batch_files[index])
        return torch.from_numpy(data).type(torch.FloatTensor), torch.from_numpy(label.astype('long'))

    def __len__(self):
        return self.len


class XvectorMultiDataset(Dataset):
    """
    Object that takes a list of files as a Python List and initialize a DataSet
    """
    def __init__(self, batch_list, batch_path):
        self.batch_files = [batch_path + '/' + l for l in batch_list]
        self.len = len(self.batch_files)

    def __getitem__(self, index):
        data, label = read_batch(self.batch_files[index])
        return torch.from_numpy(data).type(torch.FloatTensor), torch.from_numpy(label.astype('long'))

    def __len__(self):
        return self.len


class StatDataset(Dataset):
    """
    Object that initialize a Dataset from an sidekit.IdMap
    """
    def __init__(self, idmap, fs_param):
        self.idmap = idmap
        self.fs = FeaturesServer(**fs_param)
        self.len = self.idmap.leftids.shape[0]

    def __getitem__(self, index):
        data, _ = self.fs.load(self.idmap.rightids[index])
        data = (data - data.mean(0)) / data.std(0)
        data = data.reshape((1, data.shape[0], data.shape[1])).transpose(0, 2, 1).astype(numpy.float32)
        return self.idmap.leftids[index], self.idmap.rightids[index], torch.from_numpy(data).type(torch.FloatTensor)

    def __len__(self):
        return self.len


class VoxDataset(Dataset):
    """

    """
    def __init__(self, segment_df, speaker_dict, duration=500, transform = None, spec_aug_ratio=0.5, temp_aug_ratio=0.5):
        """

        :param segment_df:
        :param speaker_dict:
        :param duration:
        :param transform:
        :param spec_aug_ratio:
        :param temp_aug_ratio:
        """
        self.segment_list = segment_df

        self.speaker_dict = speaker_dict

        self.len = len(self.segment_list)
        self.duration = duration
        self.transform = transform
        tmp = numpy.zeros(self.len, dtype=bool)
        tmp[:int(self.len * spec_aug_ratio)] = 1
        numpy.random.shuffle(tmp)

        tmp2 = numpy.zeros(self.len, dtype=bool)
        tmp2[:int(self.len * temp_aug_ratio)] = 1
        numpy.random.shuffle(tmp2)

        self.spec_aug = tmp
        self.temp_aug = tmp2

    def __getitem__(self, index):
        """

        :return:
        """
        fh = h5py.File(self.segment_list.loc[index].hdf5_file, 'r')
        feature_size = fh[self.segment_list.session_id[index]].shape[1]

        start = int(self.segment_list.start[index])
        data = read_dataset_percentile(fh, self.segment_list.session_id[index]).T

        if not self.duration is None:
            if data.shape[1] < start + self.duration:
                print("Problem {}, {}".format(data.shape, start+ self.duration))
            data = data[:, start:start + self.duration]
            label = self.speaker_dict[self.segment_list.speaker_id[index]]

        else:
            label = self.segment_list.speaker_id[index]
        fh.close()

        spec_aug = False
        temp_aug = False
        if self.transform:
            data, label, spec_aug, temp_aug = self.transform((data, label, self.spec_aug[index], self.temp_aug[index]))

        if self.duration is not None:
            label = torch.from_numpy(numpy.array([label, ]).astype('long'))

        return torch.from_numpy(data).type(torch.FloatTensor), label, spec_aug, temp_aug

    def __len__(self):
        """

        :param self:
        :return:
        """
        return self.len



class CMVN(object):
    """Crop randomly the image in a sample.

    Args:
        output_size (tuple or int): Desired output size. If int, square crop
            is made.
    """
    def __init__(self):
        pass

    def __call__(self, sample):
        m = sample[0].mean(axis=0)
        s = sample[0].std(axis=0)
        data = (sample[0] - m) / s
        return data, sample[1], sample[2], sample[3]


class FrequencyMask(object):
    """Crop randomly the image in a sample.

    Args:
        output_size (tuple or int): Desired output size. If int, square crop
            is made.
    """
    def __init__(self, max_size, feature_size):
        self.max_size = max_size
        self.feature_size = feature_size

    def __call__(self, sample):
        data = sample[0]
        if sample[2]:
            size = numpy.random.randint(1, self.max_size)
            f0 = numpy.random.randint(0, self.feature_size - self.max_size)
            data[f0:f0+size, :] = 10.
        return data, sample[1], sample[2], sample[3]


class TemporalMask(object):
    """Crop randomly the image in a sample.

    Args:
        output_size (tuple or int): Desired output size. If int, square crop
            is made.
    """
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, sample):
        data = sample[0]
        if sample[3]:
            size = numpy.random.randint(1, self.max_size)
            t0 = numpy.random.randint(0, sample[0].shape[1] - self.max_size)
            data[:, t0:t0+size] = 10.
        return data, sample[1], sample[2], sample[3]

