mkdir -p ConstantOutputAttack5Agents
python3.8 main.py --epochs 150 --agents 10 --batch-size 128 --results-file Attack10AgentsDetect --attack --attack-type ConstantOutput --allow-detection
exec mv Attack10AgentsDetect.json ConstantOutputAttack5Agents
echo "HERE: Finished 10 Agents - Trustworthy"

