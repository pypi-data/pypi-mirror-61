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
Copyright 2014-2020 Yevhenii Prokopalo, Anthony Larcher
"""

import logging
import numpy
import pickle
import torch
import torch.optim as optim
import torch.multiprocessing as mp
from torchvision import transforms
from collections import OrderedDict
from .xsets import XvectorMultiDataset, StatDataset, VoxDataset
from .xsets import FrequencyMask, CMVN, TemporalMask
from ..bosaris import IdMap
from ..statserver import StatServer
from torch.utils.data import DataLoader

__license__ = "LGPL"
__author__ = "Anthony Larcher"
__copyright__ = "Copyright 2015-2020 Anthony Larcher"
__maintainer__ = "Anthony Larcher"
__email__ = "anthony.larcher@univ-lemans.fr"
__status__ = "Production"
__docformat__ = 'reS'


# logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def get_lr(optimizer):
    for param_group in optimizer.param_groups:
        return param_group['lr']


def split_file_list(batch_files, num_processes):
    # Cut the list of files into args.num_processes lists of files
    batch_sub_lists = [[]] * num_processes
    x = [ii for ii in range(len(batch_files))]
    for ii in range(num_processes):
        batch_sub_lists[ii - 1] = [batch_files[z + ii] for z in x[::num_processes] if (z + ii) < len(batch_files)]
    return batch_sub_lists


class Xtractor(torch.nn.Module):
    """
    Class that defines an x-vector extractor based on 5 convolutional layers and a mean standard deviation pooling
    """
    def __init__(self, spk_number, dropout):
        super(Xtractor, self).__init__()
        self.frame_conv0 = torch.nn.Conv1d(30, 512, 5, dilation=1)
        self.frame_conv1 = torch.nn.Conv1d(512, 512, 3, dilation=2)
        self.frame_conv2 = torch.nn.Conv1d(512, 512, 3, dilation=3)
        self.frame_conv3 = torch.nn.Conv1d(512, 512, 1)
        self.frame_conv4 = torch.nn.Conv1d(512, 3 * 512, 1)
        self.seg_lin0 = torch.nn.Linear(3 * 512 * 2, 512)
        self.dropout_lin0 = torch.nn.Dropout(p=dropout)
        self.seg_lin1 = torch.nn.Linear(512, 512)
        self.dropout_lin1 = torch.nn.Dropout(p=dropout)
        self.seg_lin2 = torch.nn.Linear(512, spk_number)
        #
        self.norm0 = torch.nn.BatchNorm1d(512)
        self.norm1 = torch.nn.BatchNorm1d(512)
        self.norm2 = torch.nn.BatchNorm1d(512)
        self.norm3 = torch.nn.BatchNorm1d(512)
        self.norm4 = torch.nn.BatchNorm1d(3 * 512)
        self.norm6 = torch.nn.BatchNorm1d(512)
        self.norm7 = torch.nn.BatchNorm1d(512)
        #
        self.activation = torch.nn.LeakyReLU(0.2)

    def produce_embeddings(self, x):
        """

        :param x:
        :return:
        """
        frame_emb_0 = self.norm0(self.activation(self.frame_conv0(x)))
        frame_emb_1 = self.norm1(self.activation(self.frame_conv1(frame_emb_0)))
        frame_emb_2 = self.norm2(self.activation(self.frame_conv2(frame_emb_1)))
        frame_emb_3 = self.norm3(self.activation(self.frame_conv3(frame_emb_2)))
        frame_emb_4 = self.norm4(self.activation(self.frame_conv4(frame_emb_3)))

        mean = torch.mean(frame_emb_4, dim=2)
        std = torch.std(frame_emb_4, dim=2)
        seg_emb = torch.cat([mean, std], dim=1)

        embedding_a = self.seg_lin0(seg_emb)
        return embedding_a

    def forward(self, x):
        """

        :param x:
        :return:
        """
        seg_emb_0 = self.produce_embeddings(x)
        # batch-normalisation after this layer
        seg_emb_1 = self.norm6(self.activation(seg_emb_0))
        # new layer with batch Normalization
        seg_emb_2 = self.norm7(self.activation(self.seg_lin1(self.dropout_lin1(seg_emb_1))))
        # No batch-normalisation after this layer
        result = self.activation(self.seg_lin2(seg_emb_2))
        return result

    def extract(self, x):
        """
        Extract x-vector given an input sequence of features

        :param x:
        :return:
        """
        embedding_a = self.produce_embeddings(x)
        embedding_b = self.seg_lin1(self.norm6(self.activation(embedding_a)))

        return embedding_a, embedding_b

    def init_weights(self):
        """
        Initialize the x-vector extract weights and biaises
        """
        torch.nn.init.normal_(self.frame_conv0.weight, mean=-0.5, std=0.1)
        torch.nn.init.normal_(self.frame_conv1.weight, mean=-0.5, std=0.1)
        torch.nn.init.normal_(self.frame_conv2.weight, mean=-0.5, std=0.1)
        torch.nn.init.normal_(self.frame_conv3.weight, mean=-0.5, std=0.1)
        torch.nn.init.normal_(self.frame_conv4.weight, mean=-0.5, std=0.1)
        torch.nn.init.xavier_uniform(self.seg_lin0.weight)
        torch.nn.init.xavier_uniform(self.seg_lin1.weight)
        torch.nn.init.xavier_uniform(self.seg_lin2.weight)

        torch.nn.init.constant(self.frame_conv0.bias, 0.1)
        torch.nn.init.constant(self.frame_conv1.bias, 0.1)
        torch.nn.init.constant(self.frame_conv2.bias, 0.1)
        torch.nn.init.constant(self.frame_conv3.bias, 0.1)
        torch.nn.init.constant(self.frame_conv4.bias, 0.1)
        torch.nn.init.constant(self.seg_lin0.bias, 0.1)
        torch.nn.init.constant(self.seg_lin1.bias, 0.1)
        torch.nn.init.constant(self.seg_lin2.bias, 0.1)


def xtrain(args):
    """
    Initialize and train an x-vector on a single GPU

    :param args:
    :return:
    """
    # If we start from an existing model
    if not args.init_model_name == '':
        # Load the model
        logging.critical("*** Load model from = {}/{}".format(args.model_path, args.init_model_name))
        model_file_name = '/'.join([args.model_path, args.init_model_name])
        model = torch.load(model_file_name)
        model.train()
    else:
        # Initialize a first model and save to disk
        model = Xtractor(args.class_number, args.dropout)
        model.train()

    if torch.cuda.device_count() > 1:
        print("Let's use", torch.cuda.device_count(), "GPUs!")
        model = torch.nn.DataParallel(model)

    model.cuda()

    # Split the training data in train and cv
    total_seg_df = pickle.load(open(args.batch_training_list, "rb"))

    speaker_dict = {}
    tmp = total_seg_df.speaker_id.unique()
    tmp.sort()
    for idx, spk in enumerate(tmp):
        speaker_dict[spk] = idx
    pickle.dump(speaker_dict, open("spk_dictionary.pkl", "wb"))

    cv_portion = 0.007
    idx = numpy.arange(len(total_seg_df))
    numpy.random.shuffle(idx)
    train_seg_df = total_seg_df.iloc[idx[:int((1 - cv_portion) * len(idx))]].reset_index()
    cv_seg_df = total_seg_df.iloc[idx[int((1 - cv_portion) * len(idx)):]].reset_index()

    current_model_file_name = "initial_model"
    torch.save(model.state_dict(), current_model_file_name)

    optimizer = torch.optim.SGD([
        {'params': model.module.frame_conv0.parameters(), 'weight_decay': args.l2_frame},
        {'params': model.module.frame_conv1.parameters(), 'weight_decay': args.l2_frame},
        {'params': model.module.frame_conv2.parameters(), 'weight_decay': args.l2_frame},
        {'params': model.module.frame_conv3.parameters(), 'weight_decay': args.l2_frame},
        {'params': model.module.frame_conv4.parameters(), 'weight_decay': args.l2_frame},
        {'params': model.module.seg_lin0.parameters(), 'weight_decay': args.l2_seg},
        {'params': model.module.seg_lin1.parameters(), 'weight_decay': args.l2_seg},
        {'params': model.module.seg_lin2.parameters(), 'weight_decay': args.l2_seg}
    ],
        lr=args.lr, momentum=0.9)

    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min')

    for epoch in range(1, args.epochs + 1):
        # Process one epoch and return the current model
        model = train_epoch(model, epoch, train_seg_df, speaker_dict, optimizer, args)

        # Add the cross validation here
        accuracy, val_loss = cross_validation(args, model, cv_seg_df, speaker_dict)
        logging.critical("*** Cross validation accuracy = {} %".format(accuracy))

        # Decrease learning rate according to the scheduler policy
        scheduler.step(val_loss)

        # return the file name of the new model
        base_name = "model"
        if not args.init_model_name == "":
            base_name = args.init_model_name
        current_model_file_name = "{}/{}_{}_epoch_{}".format(args.model_path, base_name, args.expe_id, epoch)
        torch.save(model, current_model_file_name)


def train_epoch(model, epoch, train_seg_df, speaker_dict, optimizer, args):
    """

    :param model:
    :param epoch:
    :param train_seg_df:
    :param speaker_dict:
    :param optimizer:
    :param args:
    :return:
    """
    device = torch.device("cuda:0")

    torch.manual_seed(args.seed)

    train_transform = []
    if not args.train_transformation == '':
        trans = args.train_transformation.split(',')
        for t in trans:
            if "CMVN" in t:
                train_transform.append(CMVN())
            if "FrequencyMask" in t:
                a = int(t.split("-")[0].split("(")[1])
                b = int(t.split("-")[1].split(")")[0])
                train_transform.append(FrequencyMask(a, b))
            if "TemporalMask" in t:
                a = int(t.split("(")[1].split(")")[0])
                train_transform.append(TemporalMask(a))
    train_set = VoxDataset(train_seg_df, speaker_dict, 500, transform=transforms.Compose(train_transform),
                           spec_aug_ratio=args.spec_aug, temp_aug_ratio=args.temp_aug)
    train_loader = DataLoader(train_set, batch_size=args.batch_size, shuffle=True, num_workers=15)

    criterion = torch.nn.CrossEntropyLoss()

    accuracy = 0.0
    for batch_idx, (data, target, _, __) in enumerate(train_loader):
        target = target.squeeze()
        optimizer.zero_grad()
        output = model(data.to(device))
        loss = criterion(output, target.to(device))
        loss.backward()
        optimizer.step()
        accuracy += (torch.argmax(output.data, 1) == target.to(device)).sum()

        if batch_idx % args.log_interval == 0:
            logging.critical('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}\tAccuracy: {:.3f}'.format(
                epoch, batch_idx + 1, train_loader.__len__(),
                       100. * batch_idx / train_loader.__len__(), loss.item(),
                       100.0 * accuracy.item() / ((batch_idx + 1) * args.batch_size)))
    return model


# def cross_validation(args, model):
#
#     with open(args.cross_validation_list, 'r') as fh:
#         cross_validation_list = [l.rstrip() for l in fh]
#     cv_loader = XvectorMultiDataset(cross_validation_list, args.batch_path)
#
#     model.eval()
#     device = torch.device("cuda:0")
#     model.to(device)
#
#     accuracy = 0.0
#     bi = 0
#     for batch_idx, (data, target) in enumerate(cv_loader):
#         output = model(data.to(device))
#         accuracy += (torch.argmax(output.data, 1) == target.to(device)).sum()
#         bi = batch_idx
#     return 100. * accuracy.cpu().numpy() / ((bi + 1) * args.batch_size)


def cross_validation(args, model, cv_seg_df, speaker_dict):
    """

    :param args:
    :param model:
    :param cv_seg_df:
    :return:
    """
    cv_transform = []
    if not args.cv_transformation == '':
        trans = args.cv_transformation.split(',')
        for t in trans:
            if "CMVN" in t:
                cv_transform.append(CMVN())
            if "FrequencyMask" in t:
                a = t.split(",")[0].split("(")[1]
                b = t.split(",")[1].split("(")[0]
                cv_transform.append(FrequencyMask(a, b))
            if "TemporalMask" in t:
                a = t.split(",")[0].split("(")[1]
                cv_transform.append(TemporalMask(a, b))
    cv_set = VoxDataset(cv_seg_df, speaker_dict, 500, transform=transforms.Compose(cv_transform),
                        spec_aug_ratio=args.spec_aug, temp_aug_ratio=args.temp_aug)
    cv_loader = DataLoader(cv_set, batch_size=args.batch_size, shuffle=False, num_workers=15)
    model.eval()
    device = torch.device("cuda:0")
    model.to(device)

    accuracy = 0.0
    criterion = torch.nn.CrossEntropyLoss()

    for batch_idx, (data, target, _, __) in enumerate(cv_loader):
        target = target.squeeze()
        output = model(data.to(device))
        accuracy += (torch.argmax(output.data, 1) == target.to(device)).sum()

    loss = criterion(output, target.to(device))

    return 100. * accuracy.cpu().numpy() / ((batch_idx + 1) * args.batch_size), loss


def xtrain_asynchronous(args):
    """
    Initialize and train an x-vector in asynchronous manner

    :param args:
    :return:
    """
    # Initialize a first model and save to disk
    model = Xtractor(args.class_number, args.dropout)
    current_model_file_name = "initial_model"
    torch.save(model.state_dict(), current_model_file_name)

    for epoch in range(1, args.epochs + 1):
        current_model_file_name = train_asynchronous_epoch(epoch, args, current_model_file_name)

        # Add the cross validation here
        accuracy = cross_asynchronous_validation(args, current_model_file_name)
        print("*** Cross validation accuracy = {} %".format(accuracy))

        # Decrease learning rate after every epoch
        args.lr = args.lr * 0.9
        print("        Decrease learning rate: {}".format(args.lr))


def train_asynchronous_epoch(epoch, args, initial_model_file_name):
    """
    Process one training epoch using an asynchronous implementation of the training

    :param epoch:
    :param args:
    :param initial_model_file_name:
    :return:
    """
    # Compute the megabatch number
    with open(args.batch_training_list, 'r') as fh:
        batch_file_list = [l.rstrip() for l in fh]

    # Shorten the batch_file_list to be a multiple of

    megabatch_number = len(batch_file_list) // (args.averaging_step * args.num_processes)
    megabatch_size = args.averaging_step * args.num_processes
    print("Epoch {}, number of megabatches = {}".format(epoch, megabatch_number))

    current_model = initial_model_file_name

    # For each sublist: run an asynchronous training and averaging of the model
    for ii in range(megabatch_number):
        print('Process megabatch [{} / {}]'.format(ii + 1, megabatch_number))
        current_model = train_asynchronous(epoch,
                                           args,
                                           current_model,
                                           batch_file_list[megabatch_size * ii: megabatch_size * (ii + 1)],
                                           ii,
                                           megabatch_number)  # function that split train, fuse and write the new model
    return current_model


def train_asynchronous(epoch, args, initial_model_file_name, batch_file_list, megabatch_idx, megabatch_number):
    """
    Process one mega-batch of data asynchronously, average the model parameters across
    subrocesses and return the updated version of the model

    :param epoch:
    :param args:
    :param initial_model_file_name:
    :param batch_file_list:
    :param megabatch_idx:
    :param megabatch_number:
    :return:
    """
    # Split the list of files for each process
    sub_lists = split_file_list(batch_file_list, args.num_processes)

    #
    output_queue = mp.Queue()
    # output_queue = multiprocessing.Queue()

    processes = []
    for rank in range(args.num_processes):
        p = mp.Process(target=train_asynchronous_worker,
                       args=(rank, epoch, args, initial_model_file_name, sub_lists[rank], output_queue)
                       )
        # We first train the model across `num_processes` processes
        p.start()
        processes.append(p)

    # Average the models and write the new one to disk
    asynchronous_model = []
    for ii in range(args.num_processes):
        asynchronous_model.append(dict(output_queue.get()))

    for p in processes:
        p.join()

    av_model = Xtractor(args.class_number, args.dropout)
    tmp = av_model.state_dict()

    average_param = dict()
    for k in list(asynchronous_model[0].keys()):
        average_param[k] = asynchronous_model[0][k]

        for mod in asynchronous_model[1:]:
            average_param[k] += mod[k]

        if 'num_batches_tracked' not in k:
            tmp[k] = torch.FloatTensor(average_param[k] / len(asynchronous_model))

    # return the file name of the new model
    current_model_file_name = "{}/model_{}_epoch_{}_batch_{}".format(args.model_path, args.expe_id, epoch,
                                                                     megabatch_idx)
    torch.save(tmp, current_model_file_name)
    if megabatch_idx == megabatch_number:
        torch.save(tmp, "{}/model_{}_epoch_{}".format(args.model_path, args.expe_id, epoch))

    return current_model_file_name


def train_asynchronous_worker(rank, epoch, args, initial_model_file_name, batch_list, output_queue):
    """


    :param rank:
    :param epoch:
    :param args:
    :param initial_model_file_name:
    :param batch_list:
    :param output_queue:
    :return:
    """
    model = Xtractor(args.class_number, args.dropout)
    model.load_state_dict(torch.load(initial_model_file_name))
    model.train()

    torch.manual_seed(args.seed + rank)
    train_loader = XvectorMultiDataset(batch_list, args.batch_path)

    device = torch.device("cuda:{}".format(rank))
    model.to(device)

    optimizer = optim.Adam([{'params': model.frame_conv0.parameters(), 'weight_decay': args.l2_frame},
                            {'params': model.frame_conv1.parameters(), 'weight_decay': args.l2_frame},
                            {'params': model.frame_conv2.parameters(), 'weight_decay': args.l2_frame},
                            {'params': model.frame_conv3.parameters(), 'weight_decay': args.l2_frame},
                            {'params': model.frame_conv4.parameters(), 'weight_decay': args.l2_frame},
                            {'params': model.seg_lin0.parameters(), 'weight_decay': args.l2_seg},
                            {'params': model.seg_lin1.parameters(), 'weight_decay': args.l2_seg},
                            {'params': model.seg_lin2.parameters(), 'weight_decay': args.l2_seg}
                            ], lr=args.lr)

    criterion = torch.nn.CrossEntropyLoss()

    accuracy = 0.0
    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()
        output = model(data.to(device))
        loss = criterion(output, target.to(device))
        loss.backward()
        optimizer.step()

        accuracy += (torch.argmax(output.data, 1) == target.to(device)).sum()

        if batch_idx % args.log_interval == 0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}\tAccuracy: {:.3f}'.format(
                epoch, batch_idx + 1, train_loader.__len__(),
                100. * batch_idx / train_loader.__len__(), loss.item(),
                100.0 * accuracy.item() / ((batch_idx + 1) * args.batch_size)))

    model_param = OrderedDict()
    params = model.state_dict()

    for k in list(params.keys()):
        model_param[k] = params[k].cpu().detach().numpy()
    output_queue.put(model_param)


def cross_asynchronous_validation(args, current_model_file_name):
    """

    :param args:
    :param current_model_file_name:
    :return:
    """
    with open(args.cross_validation_list, 'r') as fh:
        cross_validation_list = [l.rstrip() for l in fh]
        sub_lists = split_file_list(cross_validation_list, args.num_processes)

    #
    output_queue = mp.Queue()

    processes = []
    for rank in range(args.num_processes):
        p = mp.Process(target=cv_asynchronous_worker,
                       args=(rank, args, current_model_file_name, sub_lists[rank], output_queue)
                       )
        # We first evaluate the model across `num_processes` processes
        p.start()
        processes.append(p)

    # Average the models and write the new one to disk
    result = []
    for ii in range(args.num_processes):
        result.append(output_queue.get())

    for p in processes:
        p.join()

    # Compute the global accuracy
    accuracy = 0.0
    total_batch_number = 0
    for bn, acc in result:
        accuracy += acc
        total_batch_number += bn
    
    return 100. * accuracy / (total_batch_number * args.batch_size)


def cv_asynchronous_worker(rank, args, current_model_file_name, batch_list, output_queue):
    model = Xtractor(args.class_number, args.dropout)
    model.load_state_dict(torch.load(current_model_file_name))
    model.eval()

    cv_loader = XvectorMultiDataset(batch_list, args.batch_path)

    device = torch.device("cuda:{}".format(rank))
    model.to(device)

    accuracy = 0.0
    for batch_idx, (data, target) in enumerate(cv_loader):
        output = model(data.to(device))
        accuracy += (torch.argmax(output.data, 1) == target.to(device)).sum()
    output_queue.put((cv_loader.__len__(), accuracy.cpu().numpy()))


def extract_idmap(args, device_id, segment_indices, fs_params, idmap_name, output_queue):
    """
    Function that takes a model and an idmap and extract all x-vectors based on this model
    and return a StatServer containing the x-vectors
    """
    # device = torch.device("cuda:{}".format(device_ID))
    device = torch.device('cpu')

    # Create the dataset
    tmp_idmap = IdMap(idmap_name)
    idmap = IdMap()
    idmap.leftids = tmp_idmap.leftids[segment_indices]
    idmap.rightids = tmp_idmap.rightids[segment_indices]
    idmap.start = tmp_idmap.start[segment_indices]
    idmap.stop = tmp_idmap.stop[segment_indices]

    segment_loader = StatDataset(idmap, fs_params)

    # Load the model
    model_file_name = '/'.join([args.model_path, args.model_name])
    model = Xtractor(args.class_number, args.dropout)
    model.load_state_dict(torch.load(model_file_name))
    model.eval()

    # Get the size of embeddings
    emb_a_size = model.seg_lin0.weight.data.shape[0]
    emb_b_size = model.seg_lin1.weight.data.shape[0]

    # Create a Tensor to store all x-vectors on the GPU
    emb_1 = numpy.zeros((idmap.leftids.shape[0], emb_a_size)).astype(numpy.float32)
    emb_2 = numpy.zeros((idmap.leftids.shape[0], emb_b_size)).astype(numpy.float32)
    emb_3 = numpy.zeros((idmap.leftids.shape[0], emb_b_size)).astype(numpy.float32)
    emb_4 = numpy.zeros((idmap.leftids.shape[0], emb_b_size)).astype(numpy.float32)
    emb_5 = numpy.zeros((idmap.leftids.shape[0], emb_b_size)).astype(numpy.float32)
    emb_6 = numpy.zeros((idmap.leftids.shape[0], emb_b_size)).astype(numpy.float32)

    # Send on selected device
    model.to(device)

    # Loop to extract all x-vectors
    for idx, (model_id, segment_id, data) in enumerate(segment_loader):
        logging.critical('Process file {}, [{} / {}]'.format(segment_id, idx, segment_loader.__len__()))

        if list(data.shape)[2] < 20:
            pass
        else:
            seg_1, seg_2, seg_3, seg_4, seg_5, seg_6 = model.extract(data.to(device))
            emb_1[idx, :] = seg_1.detach().cpu()
            emb_2[idx, :] = seg_2.detach().cpu()
            emb_3[idx, :] = seg_3.detach().cpu()
            emb_4[idx, :] = seg_4.detach().cpu()
            emb_5[idx, :] = seg_5.detach().cpu()
            emb_6[idx, :] = seg_6.detach().cpu()

    output_queue.put((segment_indices, emb_1, emb_2, emb_3, emb_4, emb_5, emb_6))


def extract_parallel(args, fs_params):
    """

    :param args:
    :param fs_params:
    :return:
    """
    emb_a_size = 512
    emb_b_size = 512

    idmap = IdMap(args.idmap)

    x_server_1 = StatServer(idmap, 1, emb_a_size)
    x_server_2 = StatServer(idmap, 1, emb_b_size)
    x_server_3 = StatServer(idmap, 1, emb_b_size)
    x_server_4 = StatServer(idmap, 1, emb_b_size)
    x_server_5 = StatServer(idmap, 1, emb_b_size)
    x_server_6 = StatServer(idmap, 1, emb_b_size)

    x_server_1.stat0 = numpy.ones(x_server_1.stat0.shape)
    x_server_2.stat0 = numpy.ones(x_server_2.stat0.shape)
    x_server_3.stat0 = numpy.ones(x_server_3.stat0.shape)
    x_server_4.stat0 = numpy.ones(x_server_4.stat0.shape)
    x_server_5.stat0 = numpy.ones(x_server_5.stat0.shape)
    x_server_6.stat0 = numpy.ones(x_server_6.stat0.shape)

    # Split the indices
    mega_batch_size = idmap.leftids.shape[0] // args.num_processes

    logging.critical("Number of sessions to process: {}".format(idmap.leftids.shape[0]))

    segment_idx = []
    for ii in range(args.num_processes):
        segment_idx.append(
            numpy.arange(ii * mega_batch_size, numpy.min([(ii + 1) * mega_batch_size, idmap.leftids.shape[0]])))

    for idx, si in enumerate(segment_idx):
        logging.critical("Number of session on process {}: {}".format(idx, len(si)))

    # Extract x-vectors in parallel
    output_queue = mp.Queue()

    processes = []
    for rank in range(args.num_processes):
        p = mp.Process(target=extract_idmap,
                       args=(args, rank, segment_idx[rank], fs_params, args.idmap, output_queue)
                       )
        # We first train the model across `num_processes` processes
        p.start()
        processes.append(p)

    # Get the x-vectors and fill the StatServer
    for ii in range(args.num_processes):
        indices, seg_1, seg_2, seg_3, seg_4, seg_5, seg_6 = output_queue.get()
        x_server_1.stat1[indices, :] = seg_1
        x_server_2.stat1[indices, :] = seg_2
        x_server_3.stat1[indices, :] = seg_3
        x_server_4.stat1[indices, :] = seg_4
        x_server_5.stat1[indices, :] = seg_5
        x_server_6.stat1[indices, :] = seg_6

    for p in processes:
        p.join()

    return x_server_1, x_server_2, x_server_3, x_server_4, x_server_5, x_server_6


def extract_embeddings(args):
    """

    :param args:
    :param device_id:
    :param fs_params:
    :return:
    """
    device = torch.device("cuda:0")

    # Load the model
    logging.critical("*** Load model from = {}/{}".format(args.model_path, args.init_model_name))
    model_file_name = '/'.join([args.model_path, args.init_model_name])
    model = torch.load(model_file_name)
    model = torch.nn.DataParallel(model)
    model.eval()
    model.to(device)

    # Get the list of files
    total_seg_df = pickle.load(open(args.batch_training_list, "rb"))

    speaker_dict = {}
    tmp = total_seg_df.speaker_id.unique()
    tmp.sort()
    for idx, spk in enumerate(tmp):
        speaker_dict[spk] = idx

    extract_transform = [CMVN(), ]
    extract_set = VoxDataset(total_seg_df, speaker_dict, None, transform=transforms.Compose(extract_transform),
                             spec_aug_ratio=args.spec_aug, temp_aug_ratio=args.temp_aug)
    extract_loader = DataLoader(extract_set, batch_size=1, shuffle=False, num_workers=5)

    #CREER UN TENSEUR DE LA BONNE TAILLE POUR STOCKER LES X-VECTEURS

    for batch_idx, (data, target, _, __) in enumerate(extract_loader):
        print("extrait x-vecteur numero {}".format(batch_idx))
        embedding = model.produce_embeddings(data.to(device))
        #REMPLIR LE TENSEUR AVEC LE NOUVEAU X-VECTEUR

    #FAIRE CORRESPONDRE LES SPK_ID AVEC LES X-VECTEURS
    #RENVOYER LE TENSEUR DE X-VECTEURS SUR LE CPU OU L ECRTIRE SUR LE DISQUE
