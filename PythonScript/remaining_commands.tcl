mkdir -p LabelFlipAttack5Agents
python3.8 main.py --epochs 150 --agents 3 --batch-size 128 --results-file Attack3Agents --attack --attack-type LabelFlip
exec mv Attack3Agents.json LabelFlipAttack5Agents
echo "HERE: Finished 10 Agents - Trustworthy"

