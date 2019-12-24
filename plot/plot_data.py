import json
import numpy as np
import matplotlib.pyplot as plt

def create_x(size, rank):
    x = []
    for i in range(2 * size + 1):
        m = i - size
        row = [m**j for j in range(rank)]
        x.append(row) 
    x = np.mat(x)
    return x

def savgol(data, window_size, rank):
    m = int((window_size - 1) / 2)
    odata = data[:]
    for i in range(m):
        odata.insert(0,odata[0])
        odata.insert(len(odata),odata[len(odata)-1])
    x = create_x(m, rank)
    b = (x * (x.T * x).I) * x.T
    a0 = b[m]
    a0 = a0.T
    ndata = []
    for i in range(len(data)):
        y = [odata[i + j] for j in range(window_size)]
        y1 = np.mat(y) * a0
        y1 = float(y1)
        ndata.append(y1)
    return ndata


def Plot(name, mode, filter = False):       
    loss = json.loads(open(name + '_training_loss.json').read())
    time = json.loads(open(name + '_training_time.json').read())
    if name[0:3] == 'ada':
        num_epochs = json.loads(open(name+'_training_num_epochs.json').read())
    total_round = len(loss)
    tsum = 0
    tsum_com = 0
    total_time = []
    total_com_ratio = []
    for i in range(total_round):
        tsum += time[i]['time']
        tsum_com += time[i]['time'] - time[i]['train_time']
        total_time.append(tsum)
        total_com_ratio.append(float(tsum_com) / tsum)
    if(filter):
        loss = savgol(loss,51,5)
    if mode == "loss":
        plt.plot(total_time, loss, linewidth = 0.5, label = name)
    if mode == "ratio":
        plt.plot(total_time, total_com_ratio, linewidth = 1, label = name)
    if mode == "epoch":
        plt.plot(total_time, num_epochs, linewidth = 0.5, label = name)
    return


def main():
    fig_loss = plt.figure(figsize = (12, 6))
    plt.title("training loss")
    plt.xlabel("total time")
    plt.ylabel("training loss")
    Plot('ada2000', 'loss')
    Plot('ada4000','loss')
    Plot('bsln1', 'loss')
    Plot('bsln8', 'loss')
    plt.legend()
    plt.savefig('loss.png')

    fig_loss_filtered = plt.figure(figsize = (12, 12))
    plt.title("training loss")
    plt.xlabel("total time")
    plt.ylabel("training loss")
    Plot('ada2000', 'loss',1)
    Plot('ada4000','loss',1)
    Plot('bsln1', 'loss',1)
    Plot('bsln8', 'loss',1)
    plt.legend()
    plt.savefig('loss_filter.png')
    

    fig_ratio = plt.figure(figsize = (12, 6))
    plt.title("communication ratio")
    plt.xlabel("total time")
    plt.ylabel("communication ratio")
    Plot('ada2000', 'ratio')
    Plot('ada4000','ratio')
    Plot('bsln1', 'ratio')
    Plot('bsln8', 'ratio')
    plt.legend()
    plt.savefig('ratio.png')

    fig_epoch = plt.figure(figsize = (8, 4))
    plt.title('num epochs')
    plt.xlabel('total time')
    plt.ylabel('num epochs')
    Plot('ada2000', 'epoch')
    Plot('ada4000','epoch')
    plt.savefig('num_epochs.png')



if __name__ == '__main__':
    main()