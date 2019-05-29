#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import argparse
import json
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from numpy.random import multivariate_normal
import requests

# cookies = {
#     #'__cfduid': 'd5322ed8aff8f670be0782de50fde8d231557177073',
#     'referer_cookie': 'www.smartcat.ai',
#     #'uid': 'rB8AFFzQoWiIpRdsC8JYAg==',
#     'has_js': '1',
#     'tz': '0',
# }

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0',
#     'Accept': 'application/json, text/plain, */*',
#     'Accept-Language': 'en-US,en;q=0.5',
#     'Referer': 'https://www.smartcat.ai/',
#     'Content-Type': 'application/json;charset=utf-8',
#     'DNT': '1',
#     'Connection': 'keep-alive',
#     'TE': 'Trailers',
# }

# params = (
#     ('isNewSearchByUser', 'true'),
#     ('inAssignmentMode', 'false'),
#     #('random_lha53ft', ''),
# )

# data = '{accountId:null,searchString:,namePrefix:null,withoutAnyServices:false,withoutSpecifiedService:false,withPortfolio:false,searchMode:0,daytime:false,skip:0,limit:50,sortMode:1,restrictToUserIds:null,excludeUserIds:null,includeAllServices:false,serviceType:1,specializations:[],minRate:null,maxRate:null,specializationKnowledgeLevels:[],rateRangeCurrency:1,sourceLanguageId:9,targetLanguageId:12,expandLanguages:false,onlyNativeSpeakers:false}'
# data = '{"accountId":null,"searchString":,"namePrefix":null,"withoutAnyServices":false,"withoutSpecifiedService":false,"withPortfolio":false,"searchMode":0,"daytime":false,"skip":0,"limit":50,"sortMode":1,"restrictToUserIds":null,"excludeUserIds":null,"includeAllServices":false,"serviceType":1,"specializations":[],"minRate":null,"maxRate":null,"specializationKnowledgeLevels":[],"rateRangeCurrency":1,"sourceLanguageId":9,"targetLanguageId":12,"expandLanguages":false,"onlyNativeSpeakers":false}'


#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('https://www.smartcat.ai/proxycat/api/freelancers/?isNewSearchByUser=false&inAssignmentMode=false&random_lha53ft=', headers=headers, cookies=cookies, data=data)


def main(args):
#    response = requests.post("https://www.smartcat.ai/proxycat/api/freelancers/", headers=headers, params=params, data=data)
#    response = requests.post('https://www.smartcat.ai/proxycat/api/freelancers/?isNewSearchByUser=false&inAssignmentMode=false&random_lha53ft=', headers=headers, cookies=cookies, data=data)
    json_response = json.load(args.infile)

    rates = []
    volumes = []

    for vendor in json_response["results"]:
        if vendor["translatedWordCount"] >= args.word_limit:
            rates.append(vendor["matchedService"]["pricePerUnit"])
            volumes.append(vendor["translatedWordCount"]+1)

    print (rates, len(rates))
    fig, axes = plt.subplots(nrows=2, ncols=2)
    axes[0,0].hist(rates, bins=20, range=(0,0.16))
    axes[1,1].hist(np.log10(volumes), bins=20, orientation="horizontal")
    axes[0,1].hist(rates, bins=20, weights=volumes, range=(0,0.16), density=True, histtype="stepfilled")
    # axes[2,2].set_title("Rate vs Volume Distribution")
    # axes[1,1].set_xlabel("Rate [$/word]")
    # axes[1,1].set_ylabel("Volume [log10(words)]")
    counts, xedges, yedges, im = axes[1,0].hist2d(rates, np.log10(volumes), range=((0,0.16),(0,7)))
    # plt.colorbar(im)
    axes[0,0].set_title("Rate [$/word]")
    axes[1,0].set_ylabel("Volume [log10(words)]")
    
    plt.savefig(args.outfile)
    plt.clf()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--infile', dest='infile',
        type=argparse.FileType('r', encoding='UTF-8'),
        nargs='?',
        default=sys.stdin,
        help='Input file'
    )
    parser.add_argument(
        '-o', '--outfile', dest='outfile',
        help='Output file'
    )
    parser.add_argument(
        "-w", "--word_limit", dest="word_limit",
        type=int,
        nargs="?",
        default=-1,
        help="Minimum number of words translated by a translator to be included"
    )
    main(parser.parse_args())
