# AlphaDoge
MCTS based Go game agent    

#### Quick Start 

```
pip3 install requirements.txt
python3 main.py  
```


#### Dependencies:

* numpy
* tensorflow
* scipy
* PyQt5
* sgf  (only used by training)


#### Screenshot:
![game](https://github.com/VainF/AlphaDoge/blob/master/screenshot/game.png)  

#### dataset  
CGOS 9x9 dataset: [download](http://www.yss-aya.com/cgos/9x9/archive.html)  
Try mkdir CGOS9x9 and put compressed files under ./CGOS9x9

#### files:
* main.py : program entry
* go.py : basic go game environment
* game.py : game logic
* mcts.py : MCTS implementation
* strategies.py : MCTS player
* model.py : neural network implementation
* PVNet.py : interface for neural networks
* Opponents : interface of Go agent (QThread)
* selfplay.py : RL
* train_dual_net.py : train
* utils : utilities
* merge_dataset.py : merge data files
* dataLoader.py : SGF reader
* process_dataset.sh : uncompress
* trainSL.sh : supervised learning
* trainRL.sh : reinforced learning
* requirements.txt : requirements
* checkpoints : pretrained model


