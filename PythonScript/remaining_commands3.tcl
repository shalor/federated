mkdir -p LabelFlipAttack5Agents
python3.8 main.py --epochs 150 --agents 7 --batch-size 128 --results-file Attack7Agents --attack --attack-type LabelFlip
exec mv Attack7Agents.json LabelFlipAttack5Agents
echo "HERE: Finished 10 Agents - Trustworthy"

