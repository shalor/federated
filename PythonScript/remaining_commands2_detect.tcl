mkdir -p ConstantOutputAttack5Agents
python3.8 main.py --epochs 150 --agents 5 --batch-size 128 --results-file Attack5AgentsDetect --attack --attack-type ConstantOutput --allow-detection
exec mv Attack5AgentsDetect.json ConstantOutputAttack5Agents
echo "HERE: Finished 10 Agents - Trustworthy"

