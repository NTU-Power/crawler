#!/usr/bin/env sh

python3 -m NTU-Map-crawler.crawl_NTU_Map
python3 -m src.demoCrawler
python3 -m src.outputCSV
python3 -m src.saveMapping
