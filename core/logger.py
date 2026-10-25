# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime

def get_logger(name="CompetitorAgent"):
    # 建立日志文件夹
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs", "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # 避免重复添加 handler
    if not logger.handlers:
        # 控制台输出
        console_handler = logging.StreamHandler()
        console_format = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt='%H:%M:%S')
        console_handler.setFormatter(console_format)
        
        # 文件输出
        file_handler = logging.FileHandler(os.path.join(log_dir, f"agent_{datetime.now().strftime('%Y%m%d')}.log"), encoding='utf-8')
        file_format = logging.Formatter('%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s')
        file_handler.setFormatter(file_format)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
    return logger