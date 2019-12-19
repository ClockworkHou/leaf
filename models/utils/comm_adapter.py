'''Adacomm: communication adapter'''
import copy
import math

from .config import Config
from .logger import Logger

L = Logger()
logger = L.get_logger()

# Adapt communication interval after a fixed period
class CommAdapter():
	def __init__(self, cfg: Config, _interval = 1, _min_ddl = 10):
		self.timer = 0
		self.interval = _interval*cfg.round_ddl[0]
		self.num_epochs = cfg.num_epochs
		self.deadline = cfg.round_ddl[0]
		self.min_deadline = _min_ddl
		self.pre_loss = -1
		self.loss = -1

	def adapt(self):
		logger.info("Comm Adapter: timer:{}, interval:{}".format(self.timer,self.interval))
		if(self.timer >= self.interval):
			logger.info("Comm Adapter: pre_loss:{}, loss:{}".format(self.pre_loss,self.loss))
			if self.pre_loss != -1 and self.loss != -1 and self.pre_loss > self.loss:	
				nxt_num_epochs = (float(self.loss/self.pre_loss)**0.5)*float(self.num_epochs)
				
				if nxt_num_epochs > 1.0:
					nxt_num_epochs = math.ceil(nxt_num_epochs)
				
				self.deadline = int(max(
					self.deadline*float(nxt_num_epochs/self.num_epochs),
					self.min_deadline

				))
				self.num_epochs = nxt_num_epochs

			self.update_loss()
			self.timer = 0
		logger.info("Comm Adapter: set num_epochs: {}, deadline: {}".format(self.num_epochs, self.deadline))
		return self.num_epochs, self.deadline

	def update_loss(self):
		self.pre_loss = self.loss
		self.loss = -1

	def collect_info(self, simulate_time, _loss):
		self.loss = _loss
		self.timer += simulate_time


