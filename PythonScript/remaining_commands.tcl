mkdir -p LabelFlipAttack5Agents
python3.9 main.py --epochs 100 --agents 5 --batch-size 128 --results-file Attack5Agents --attack --attack-type LabelFlip --delayed-attack 15
exec mv Attack5Agents.json LabelFlipAttack5Agents
echo "HERE: Finished 10 Agents - Trustworthy"

