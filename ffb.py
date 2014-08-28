#!/usr/bin/python
# -*- coding: utf-8 -*-

from operator import attrgetter
from collections import namedtuple
Player = namedtuple("Player", ['rank', 'name', 'team', 'bye', 'posrank', 'auction'])
CombinedPlayer = namedtuple("CombinedPlayer", ['rank', 'name', 'team', 'bye', 'stdrank', 'pprrank', 'stdposrank', 'pprposrank','stdauction', 'pprauction', 'auction'])

#combine std and ppr lists. average the rank and auction values, order by average rank
def combine_lists(std_data, ppr_data):
    players = []
    for name in ppr_data:
        ppr = ppr_data[name]
        std = Player(400,ppr.name,ppr.team,ppr.bye,'NA',0) 
        if name in std_data:
            std = std_data[name]

        avg_rank = float(std.rank + ppr.rank) / float(2)
        avg_auction = float(std.auction + ppr.auction) / float(2)
        players.append(CombinedPlayer(avg_rank,name,ppr.team, ppr.bye, std.rank, ppr.rank, std.posrank, ppr.posrank, std.auction, ppr.auction, avg_auction))

    return sorted(players, key=attrgetter('rank'))

#print the combined list to stdout in csv format
def print_combined(players):
    print "AVG_RANK,AUCTION,NAME,TEAM,BYE,PPR_RANK,STD_RANK,PPR_POSRANK,STD_POSRANK,PPR_AUCTION,STD_AUCTION"
    for p in players:
        print p.rank,',',p.auction,',',p.name,',',p.team,',',p.bye,',',p.pprrank,',',p.stdrank,',',p.pprposrank,',',p.stdposrank,',',p.pprauction,',',p.stdauction 
        
#read players from a csv format file
def parse_players(file_path):
    file_location = file_path.strip()
    input_data_file = open(file_location, 'r')
    input_data = ''.join(input_data_file.readlines())
    input_data_file.close()
    lines = input_data.split('\n')
    firstLine = lines[0].split(',')
    item_count = len(lines)-1
    players = {}

    for i in range(1, item_count):
        line = lines[i]
        parts = line.split(',')
        rank = int(parts[0])
        name = str(parts[1])
        team = str(parts[2])
        bye = int(parts[3])
        posrank = str(parts[4])
        auction = int(parts[5])
        p = Player(rank,name,team,bye,posrank,auction)
        players[p.name] = p

    return players

import sys

if __name__ == '__main__':
    if len(sys.argv) > 2:
        std_path = sys.argv[1].strip()
        std_data = parse_players(std_path)
        ppr_path = sys.argv[2].strip()
        ppr_data = parse_players(ppr_path)
        combined = combine_lists(std_data, ppr_data)
        print_combined(combined)
    else:
        print 'This bitch requires an two input files.  Please select a std.csv and a ppr.csv, mothafucka.'
        print 'python ffb.py <std.csv. <ppr.csv>'

