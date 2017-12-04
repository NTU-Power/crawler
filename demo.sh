#!/usr/bin/env sh

python3 NTU-Map-crawler/crawl_NTU_Map.py
python3 -m src.demoCrawler
python3 src/outputCSV.py
