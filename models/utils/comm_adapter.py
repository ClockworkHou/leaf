'''Adacomm: communication adapter'''
import copy
import math

from .config import Config
from .logger import Logger

L = Logger()
logger = L.get_logger()

# Adapt communication interval after a fixed period
class CommAdapter():
	def __init__(self, cfg: Config, _interval = 100, _min_ddl = 15):
		self.timer = 0
		self.interval = _interval*cfg.round_ddl[0]
		self.num_epochs = cfg.num_epochs
		self.deadline = cfg.round_ddl[0]
		self.min_deadline = _min_ddl
		self.pre_loss = 100
		self.loss = -1.0
		self.loss_list = []

	def adapt(self):
		logger.info("Comm Adapter: timer:{}, interval:{}".format(self.timer,self.interval))
		
		if(self.timer >= self.interval):
			if len(self.loss_list) > 0:
				self.loss = float(sum(self.loss_list))/float(len(self.loss_list))
			logger.info("Comm Adapter: pre_loss:{}, loss:{}".format(self.pre_loss,self.loss))
			nxt_num_epochs = float(self.num_epochs/2.0)
			if self.pre_loss != -1 and self.loss != -1:	
				nxt_num_epochs = max(
					nxt_num_epochs,
					(float(self.loss/self.pre_loss)**0.5)*float(self.num_epochs)
				)
				
				if nxt_num_epochs > 1.0:
					nxt_num_epochs = math.ceil(nxt_num_epochs)
					if nxt_num_epochs >= self.num_epochs:
						nxt_num_epochs = math.ceil(float(self.num_epochs)/2.0)
				else:
					nxt_num_epochs = float(self.num_epochs)/2.0
						
				self.deadline = int(max(
					math.ceil(float(self.deadline*0.8)),
					self.min_deadline
				))
				self.num_epochs = nxt_num_epochs

			self.update_record()
			
		logger.info("Comm Adapter: set num_epochs: {}, deadline: {}".format(self.num_epochs, self.deadline))
		return self.num_epochs, self.deadline

	def update_record(self):
		self.pre_loss = self.loss
		self.loss_list.clear()
		self.loss = -1
		self.timer = 0

	def collect_info(self, simulate_time, _loss):
		self.loss_list.append(_loss)
		self.timer += simulate_time


