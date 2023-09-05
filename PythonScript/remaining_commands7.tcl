mkdir -p LabelFlipAttack5Agents
python3.8 main.py --epochs 150 --agents 50 --batch-size 128 --results-file Attack50Agents --attack --attack-type LabelFlip
exec mv Attack15Agents.json LabelFlipAttack50Agents
echo "HERE: Finished 10 Agents - Trustworthy"

