mkdir -p ConstantOutputAttack5Agents
python3.8 main.py --epochs 150 --agents 20 --batch-size 128 --results-file Attack20AgentDetect --attack --attack-type ConstantOutput --allow-detection
exec mv Attack20AgentDetect.json ConstantOutputAttack5Agents
echo "HERE: Finished 10 Agents - Trustworthy"

