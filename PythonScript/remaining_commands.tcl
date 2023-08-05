python3.9 main.py --epochs 100 --agents 10 --attack --batch-size 128 --attack-type ConstantOutput --delayed-attack 15 --allow-detection

exec mv results_dictionary.json DifferentSizesConstantOutput/Detection10Agents.json

python3.9 main.py --epochs 100 --agents 10 --batch-size 128

exec mv results_dictionary.json DifferentSizesConstantOutput/Trustworthy10Agents.json
