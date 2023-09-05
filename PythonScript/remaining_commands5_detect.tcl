mkdir -p LabelFlipAttack5Agents
python3.8 main.py --epochs 150 --agents 15 --batch-size 128 --results-file Attack15AgentsDetection --attack --attack-type LabelFlip --allow-detection
exec mv Attack15AgentsDetection.json LabelFlipAttack5Agents
echo "HERE: Finished 10 Agents - Trustworthy"

