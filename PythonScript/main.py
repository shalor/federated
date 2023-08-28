from __future__ import print_function
import argparse
import copy
import os
import json
import statistics

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import math
from torchvision import datasets, transforms
from torch.optim.lr_scheduler import StepLR


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout(0.25)
        self.dropout2 = nn.Dropout(0.5)
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        output = F.log_softmax(x, dim=1)
        return output


def train(args, model, device, train_loader, optimizer, epoch, agent, attacking_agent, train_loader_size):
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        if batch_idx < agent * train_loader_size or batch_idx > (agent + 1) * train_loader_size:
            continue
        if args.attack and agent == attacking_agent and epoch >= args.delayed_attack:
            if args.attack_type == "Randomized":
                return
            elif args.attack_type == "LabelFlip":
                # Flipping rules: 1->3 ; 3->7 ; 7->9; 9->2 ; 2->4 ; 4->5 ; 5->8 ; 8->6 ; 6->0 ; 0->1
                previous_target = target.clone()
                target[previous_target == 1] = 3
                target[previous_target == 2] = 4
                target[previous_target == 3] = 7
                target[previous_target == 4] = 5
                target[previous_target == 5] = 8
                target[previous_target == 6] = 0
                target[previous_target == 7] = 9
                target[previous_target == 8] = 6
                target[previous_target == 9] = 2
                target[previous_target == 0] = 1

            elif args.attack_type == "ConstantOutput":
                previous_target = target
                target = torch.ones(target.size()) * 9
                target = target.type_as(previous_target)
            else:
                os.error("Unsupported attack type was inserted, aborting...")
                os._exit(1)

        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % args.log_interval == 0 and args.print_train:
            print('Agent {}, Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                agent, epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))
            if args.dry_run:
                break


def test(model, device, test_loader, epoch, results_dic):
    model.eval()
    test_loss = 0
    correct = 0
    results_dic["Epoch{} target".format(epoch)] = []
    results_dic["Epoch{} pred".format(epoch)] = []
    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += F.nll_loss(output, target, reduction='sum').item()  # sum up batch loss
            pred = output.argmax(dim=1, keepdim=True)  # get the index of the max log-probability
            results_dic["Epoch{} target".format(epoch)].append(target.tolist())
            results_dic["Epoch{} pred".format(epoch)].append(pred.tolist())
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)

    print('\nJoint model, Test set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))


def main():
    # Training settings
    parser = argparse.ArgumentParser(description='PyTorch MNIST Example')
    parser.add_argument('--batch-size', type=int, default=64, metavar='N',
                        help='input batch size for training (default: 64)')
    parser.add_argument('--test-batch-size', type=int, default=1000, metavar='N',
                        help='input batch size for testing (default: 1000)')
    parser.add_argument('--epochs', type=int, default=14, metavar='N',
                        help='number of epochs to train (default: 14)')
    parser.add_argument('--lr', type=float, default=1.0, metavar='LR',
                        help='learning rate (default: 1.0)')
    parser.add_argument('--gamma', type=float, default=0.7, metavar='M',
                        help='Learning rate step gamma (default: 0.7)')
    parser.add_argument('--no-cuda', action='store_true', default=False,
                        help='disables CUDA training')
    parser.add_argument('--no-mps', action='store_true', default=True,
                        help='disables macOS GPU training')
    parser.add_argument('--dry-run', action='store_true', default=False,
                        help='quickly check a single pass')
    parser.add_argument('--seed', type=int, default=1, metavar='S',
                        help='random seed (default: 1)')
    parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                        help='how many batches to wait before logging training status')
    parser.add_argument('--save-model', action='store_true', default=False,
                        help='For Saving the current Model')
    parser.add_argument('--print-model', action='store_true', default=False,
                        help='Print model parameters')
    parser.add_argument('--print-train', action='store_true', default=False,
                        help='Print debug print while training')
    parser.add_argument('--agents', type=int, default=2, metavar='N',
                        help='Number of agents (default: 1)')
    parser.add_argument('--attack', action='store_true', default=False,
                        help='Choose if to implement an attack')
    parser.add_argument('--attack-strength', type=int, default=0, metavar='N',
                        help='Attack coefficient for the agent')
    parser.add_argument('--delayed-attack', type=int, default=0, metavar='N',
                        help='Insert the attack with a delay')
    parser.add_argument('--attack-type', default="", metavar='STRING',
                        help='Insert an attack type')
    parser.add_argument('--results-file', default="results_dictionary", metavar='STRING',
                        help='Insert an attack type')
    parser.add_argument('--allow-detection', action='store_true', default=False,
                        help='Apply attacker detection algorithm')
    args = parser.parse_args()
    use_cuda = not args.no_cuda and torch.cuda.is_available()
    use_mps = not args.no_mps and torch.backends.mps.is_available()
    torch.manual_seed(args.seed)

    if use_cuda:
        device = torch.device("cuda")
    elif use_mps:
        device = torch.device("mps")
    else:
        device = torch.device("cpu")

    train_kwargs = {'batch_size': args.batch_size}
    test_kwargs = {'batch_size': args.test_batch_size}
    if use_cuda:
        cuda_kwargs = {'num_workers': 1,
                       'pin_memory': True,
                       'shuffle': True}
        train_kwargs.update(cuda_kwargs)
        test_kwargs.update(cuda_kwargs)

    transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    dataset1 = datasets.MNIST('../data', train=True, download=True,
                       transform=transform)
    dataset2 = datasets.MNIST('../data', train=False,
                       transform=transform)
    train_loader = torch.utils.data.DataLoader(dataset1,**train_kwargs)
    test_loader = torch.utils.data.DataLoader(dataset2, **test_kwargs)

    dic = {}
    results_dic = {}

    if args.attack_type != "":
        args.attack = True

    if args.attack:
        attacking_agent = 0
    else:
        attacking_agent = -1

    joint_model = Net().to(device)

    for agent in range(args.agents):
        dic["model{0}".format(agent)] = Net().to(device)
        dic["prev_model{0}".format(agent)] = Net().to(device)
        dic["optimizer{0}".format(agent)] = optim.Adadelta(dic["model{0}".format(agent)].parameters(), lr=args.lr)
        dic["scheduler{0}".format(agent)] = StepLR(dic["optimizer{0}".format(agent)], step_size=1, gamma=args.gamma)
    attack_coefficient = 0
    for epoch in range(1, args.epochs + 1):

        if args.attack and epoch >= args.delayed_attack:
            # Set attacking agent as agent 0
            active_attacker = 0
            # Set attack coefficient to be taken
            if args.attack_strength != 0:
                attack_coefficient = args.attack_strength
            else:
                attack_coefficient =  math.sqrt((epoch + 1 - args.delayed_attack))
                attack_coefficient = attack_coefficient if attack_coefficient < 6 else 6
                print("Epoch {}, Attack delay: {}, Coefficient is: {}".format(epoch, args.delayed_attack, attack_coefficient))

        # Prior to training, need to keep the local models data for the attack detection process
        for agent in range(args.agents):
            if use_cuda:
                dic["model{0}".format(agent)].conv1.cuda()
                dic["model{0}".format(agent)].conv2.cuda()
                dic["model{0}".format(agent)].fc1.cuda()
                dic["model{0}".format(agent)].fc2.cuda()
                dic["prev_model{0}".format(agent)].conv1.cuda()
                dic["prev_model{0}".format(agent)].conv2.cuda()
                dic["prev_model{0}".format(agent)].fc1.cuda()
                dic["prev_model{0}".format(agent)].fc2.cuda()
            dic["prev_model{0}".format(agent)].conv1.weight.data = dic["model{0}".format(agent)].conv1.weight.data.clone()
            dic["prev_model{0}".format(agent)].conv2.weight.data = dic["model{0}".format(agent)].conv2.weight.data.clone()
            dic["prev_model{0}".format(agent)].fc1.weight.data = dic["model{0}".format(agent)].fc1.weight.data.clone()
            dic["prev_model{0}".format(agent)].fc2.weight.data = dic["model{0}".format(agent)].fc2.weight.data.clone()

        # Perform training for each agent
        print("Running epoch {} out of {}.".format(epoch,args.epochs))
        train_loader_length = math.floor(len(train_loader.dataset) / args.agents / args.batch_size)
        for agent in range(args.agents):
            print("Running training on agent {}.".format(agent))
            train(args, dic["model{0}".format(agent)], device, train_loader, dic["optimizer{0}".format(agent)], epoch, agent, attacking_agent, train_loader_length)
            # test(dic["model{0}".format(agent)], device, test_loader)
            dic["scheduler{0}".format(agent)].step()

        # Reset the joint model parameters in each epoch
        for p in joint_model.parameters():
            if p.requires_grad:
                # print(p.name, p.data)
                p.data = torch.zeros(p.size())

        if args.attack_type == "Randomized" and epoch >= args.delayed_attack:
            print("Current attacking agent is {}, running a randomized attack.".format(active_attacker))
            for p in dic["model{0}".format(active_attacker)].parameters():
                if p.requires_grad:
                    # print(p.name, p.data)
                    p.data = args.attack_strength * torch.randn(p.size())

        # Update the join model parameters with each agent parameters

        attack_detected = 0
        assumed_attacker_agent = -1
        delta = 1e6

        norm_list = []
        for agent in range(args.agents):
            agent_coefficient = 1
            if args.attack and epoch >= args.delayed_attack:
                #agent_coefficient = 1
                if agent == attacking_agent:
                    agent_coefficient = attack_coefficient
            else:
                continue
            if use_cuda:
                dic["prev_model{0}".format(agent)].conv1.cuda()
                dic["prev_model{0}".format(agent)].conv2.cuda()
                dic["prev_model{0}".format(agent)].fc1.cuda()
                dic["prev_model{0}".format(agent)].fc2.cuda()
                dic["model{0}".format(agent)].conv1.cuda()
                dic["model{0}".format(agent)].conv2.cuda()
                dic["model{0}".format(agent)].fc1.cuda()
                dic["model{0}".format(agent)].fc2.cuda()

            dic["agent{0}_conv1_norm".format(agent)] = agent_coefficient * (dic["model{0}".format(agent)].conv1.weight.data - dic["prev_model{0}".format(agent)].conv1.weight.data).norm()
            dic["agent{0}_conv2_norm".format(agent)] = agent_coefficient * (dic["model{0}".format(agent)].conv2.weight.data - dic["prev_model{0}".format(agent)].conv2.weight.data).norm()
            dic["agent{0}_fc1_norm".format(agent)] = agent_coefficient * (dic["model{0}".format(agent)].fc1.weight.data - dic["prev_model{0}".format(agent)].fc1.weight.data).norm()
            dic["agent{0}_fc2_norm".format(agent)] = agent_coefficient * (dic["model{0}".format(agent)].fc2.weight.data - dic["prev_model{0}".format(agent)].fc2.weight.data).norm()

            if args.allow_detection:
                dic["agent{0}_norm".format(agent)] = torch.tensor([dic["agent{0}_conv1_norm".format(agent)].tolist(),dic["agent{0}_conv2_norm".format(agent)].tolist(),dic["agent{0}_fc1_norm".format(agent)].tolist(),dic["agent{0}_fc2_norm".format(agent)].tolist()]).norm()
                # dic["agent{0}_norm".format(agent)] = torch.cat([dic["agent{0}_conv1_norm".format(agent)],dic["agent{0}_conv2_norm".format(agent)],dic["agent{0}_fc1_norm".format(agent)],dic["agent{0}_fc2_norm".format(agent)]]).norm()
                norm_list.append(dic["agent{0}_norm".format(agent)].tolist())
                print("Agent{} - norm = {}".format(agent, dic["agent{0}_norm".format(agent)]))

        if args.allow_detection and (epoch >= args.delayed_attack):
            delta = statistics.median(norm_list)
            print("Epoch {}: Current delta (median) is: {}".format(epoch, delta))

        for agent in range(args.agents):
            #if args.allow_detection and (epoch >= args.delayed_attack) and (dic["agent{0}_norm".format(agent)].tolist()) > delta * math.sqrt(args.agents)):
            if args.allow_detection and (epoch >= args.delayed_attack) and (abs(dic["agent{0}_norm".format(agent)].tolist() - delta) > delta * math.sqrt(args.agents)):
                attack_detected = 1
                print("Detected an attacker: {}".format(agent))
                if assumed_attacker_agent != -1:
                    print("Found multiple attackers: {}, {}".format(assumed_attacker_agent, agent))
                assumed_attacker_agent = agent

        if attack_detected:
            trustworthy_agents_amount = args.agents - 1
        else:
            trustworthy_agents_amount = args.agents

        for agent in range(args.agents):
            if agent == assumed_attacker_agent:
                continue
            # agent_coefficient is used for randomized attack only, other attacks are using the attackers' trained model
            agent_coefficient = 1
            if args.attack and epoch >= args.delayed_attack:
                if agent == attacking_agent:
                    agent_coefficient = attack_coefficient
                    print("Current attacking agent is {}, coefficient is {}.".format(agent, agent_coefficient))

            if use_cuda:
                joint_model.conv1.cuda()
                joint_model.conv2.cuda()
                joint_model.fc1.cuda()
                joint_model.fc2.cuda()
            joint_model.conv1.weight.data = joint_model.conv1.weight.data + agent_coefficient * (dic["model{0}".format(agent)].conv1.weight.data) / trustworthy_agents_amount
            joint_model.conv2.weight.data = joint_model.conv2.weight.data + agent_coefficient * (dic["model{0}".format(agent)].conv2.weight.data) / trustworthy_agents_amount
            joint_model.fc1.weight.data = joint_model.fc1.weight.data + agent_coefficient * (dic["model{0}".format(agent)].fc1.weight.data) / trustworthy_agents_amount
            joint_model.fc2.weight.data = joint_model.fc2.weight.data + agent_coefficient * (dic["model{0}".format(agent)].fc2.weight.data) / trustworthy_agents_amount

        # Send the updated params to the agents, keep the previous transmission
        for agent in range(args.agents):
            dic["model{0}".format(agent)].conv1.weight.data = joint_model.conv1.weight.data.clone()
            dic["model{0}".format(agent)].conv2.weight.data = joint_model.conv2.weight.data.clone()
            dic["model{0}".format(agent)].fc1.weight.data = joint_model.fc1.weight.data.clone()
            dic["model{0}".format(agent)].fc2.weight.data = joint_model.fc2.weight.data.clone()

            # dic["model{0}".format(agent)] = copy.deepcopy(joint_model)

        test(joint_model, device, test_loader, epoch, results_dic)
        # print(results_dic)
        # correct += pred.eq(target.view_as(pred)).sum().item()

        if args.save_model:
            torch.save(joint_model.state_dict(), "mnist_cnn.pt")

        if args.print_model:
            for p in dic["model{0}".format(agent)].parameters():
                if p.requires_grad:
                    print(p.name, p.data)
                    # print(p.size())

        if epoch % 10 == 0 or epoch == args.epochs:
            print("Finished Running epoch {}, printing results dictionary to file.".format(epoch))
            file_name = "{}.json".format(args.results_file)
            with open(file_name, "w") as fp:
                json.dump(results_dic, fp)
            print("Finished printing results dictionary to file after epoch {}.".format(epoch))
            torch.save(joint_model.state_dict(), "joint_model.pt")


if __name__ == '__main__':
    main()
