mkdir -p LabelFlipAttack5Agents
python3.8 main.py --epochs 150 --agents 10 --batch-size 128 --results-file Attack10AgentsStr2 --attack --attack-type LabelFlip --attack-strength 2
exec mv Attack10AgentsStr2.json LabelFlipAttack5Agents
echo "HERE: Finished 10 Agents - Trustworthy"

