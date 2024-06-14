#!/usr/bin/env python3

import json
import pickle

from scraper import Scraper

def save(blocks, fn):
    with open(fn, 'wb') as f:
        pickle.dump(blocks, f)

def scrape_blocks(start_bn, end_bn, scraper):
    blocks = []
    for bn in range(start_bn, end_bn + 1):
        block = scraper.eth_getBlockByNumber(hex(bn))
        blocks.append(block)
    return blocks

def get_blocks(start_bn, end_bn, scraper, fn):
    blocks = scrape_blocks(start_bn, end_bn, scraper)
    save(blocks, fn)

if __name__ == '__main__':
    start_bn = 19976901
    end_bn = 19976910
    scraper = Scraper()
    get_blocks(start_bn, end_bn, scraper, 'blocks.pkl')