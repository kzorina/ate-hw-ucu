#!/usr/bin/env python2
#encoding: UTF-8

import ConfigParser
import ate

config = ConfigParser.ConfigParser()
config.readfp(open('config.ini'))

txt_dir=config.get('main', 'txt_dir')
dataset_dir=config.get('main', 'dataset_dir')

# ate.compose_datasets(txt_dir, dataset_dir, increment_size=20, increment_strategy='time-asc')
# ate.compose_datasets(txt_dir, dataset_dir, increment_size=20, increment_strategy='time-desc')
# ate.compose_datasets(txt_dir, dataset_dir, increment_size=20, increment_strategy='random')
ate.compose_datasets(txt_dir, dataset_dir, increment_size=20, increment_strategy='time-bidir')

