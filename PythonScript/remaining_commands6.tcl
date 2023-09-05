mkdir -p LabelFlipAttack5Agents
python3.8 main.py --epochs 150 --agents 20 --batch-size 128 --results-file Attack20Agents --attack --attack-type LabelFlip
exec mv Attack20Agents.json LabelFlipAttack5Agents
echo "HERE: Finished 10 Agents - Trustworthy"

